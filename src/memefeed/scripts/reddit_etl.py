"""
Extract daily top reddit submissions for each subreddit in SUBREDDITS_CSV.
"""
import praw
# import pmaw
from csv import reader
from re import match
import sentry_sdk
# import requests

from reddit.models import Author, Subreddit, Submission
from django.db import models

from itertools import zip_longest

# TODO:
# See if pushshift is comprehensive index (?)
# If it works for subreddit --> PUT into DB
# If it doesn't work --> Use reddit API
# Take IDS from pushshift --> batch read using reddit api
# bulk_create() to load into model
# Figure out how to do the foreign key3

# TODO: Pushshift is pretty unreliable
# Fix model transformation mapping `python manage.py shell < scripts/reddit_etl.py`
# Staging files (?)
# 

class RedditETL:
    """
    Class that ingests data from reddit and puts it into the submissiongres db.

    
    Functional dependencies:
    id -> title, author, score, url, domain, subreddit, over_18, is_self, is_video
    id -> shortlink (https://redd.it/{id})
    is_self -> selftext, is_self -> selftext_html
    is_video -> media, is_video -> media_embed, is_video -> secure_media, is_video -> thumbnail, is_video -? secure_media_embed
    subreddit -> subreddit_id (or other way around?)

    """

    # "id " + str(submission.id),
    # "title " + str(submission.title),
    # "author " + str(submission.author),
    # "score " + str(submission.score),
    # "url " + str(submission.url), # Otherwise a link to a url?
    # "domain " + str(submission.domain),
    # "subreddit " + str(submission.subreddit),
    # # "subreddit_id " + str(submission.subreddit_id),
    # "created_utc " + str(submission.created_utc),
    # "is_self " + str(submission.is_self),  # if True, only text
    # "is_video " + str(submission.is_video),  # If True, then video in media
    # "media " + str(submission.media),
    # "media_embed " + str(submission.media_embed),
    # "media_only " + str(submission.media_only),
    # "selftext " + str(submission.selftext),
    # "selftext_html " + str(submission.selftext_html),
    # "over_18 " + str(submission.over_18),  # if True, thumbnail is nsfw
    # "thumbnail " + str(submission.thumbnail),  # Either jpg url, nsfw or none
    # "secure_media " + str(submission.secure_media),
    # "secure_media_embed " + str(submission.secure_media_embed),


    CACHE_DIR = "./cache"
    SUBREDDITS_CSV = "scripts/data/subreddits.csv"
    
    # Dict mapping
    ACCEPTED_FIELDS = [
        "title",
        "author",
        "score",
        "url",
        "subreddit",
        "created_utc",
        "domain",
        "id",
        "is_self",
        "is_video",
        "media",
        "media_embed",
        "media_only",
        "selftext",
        "selftext_html",
        "over_18",
        "thumbnail",
        "secure_media",
        "secure_media_embed"
    ]
        
    # Map 
    AUTHOR_MAP = {"name":(getattr, "author"), "favourite": (None, False)}
    # [f.name for f in Author._meta.get_fields()]
    # [f.name for f in Subreddit._meta.get_fields()]
    SUBREDDIT_MAP = {"name":(getattr, "subreddit"), "favourite": (None, False)}
    SUBMISSION_MAP = {
        "title": (getattr, "title"),
        "score": (getattr, "score"),
        "url": (getattr, "url"),
        "created_utc": (getattr, "created_utc"),
        "domain": (getattr, "domain"),
        "id": (getattr, "id"),
        "is_self": (getattr, "is_self"),
        "is_video": (getattr, "is_video"),
        "media": (getattr, "media"),
        "media_embed": (getattr, "media_embed"),
        "media_only": (getattr, "media_only"),
        "selftext": (getattr, "selftext"),
        "selftext_html": (getattr, "selftext_html"),
        "nsfw": (getattr, "over_18"),
        "thumbnail": (getattr, "thumbnail"),
        "secure_media": (getattr, "secure_media"),
        "secure_media_embed": (getattr, "secure_media_embed"),
        # Foreign keys
        "author": (getattr, "author"),
        "subreddit": (getattr, "subreddit"),
    }
    MODEL_MAPPINGS = {
        "AUTHOR": AUTHOR_MAP,
        "SUBREDDIT": SUBREDDIT_MAP,
        "SUBMISSION": SUBMISSION_MAP 
    }
    
    
    # TODO: Remove in production alongside usage in extract()
    # N_submissionS_PER_SUBREDDIT = 50

    def __init__(self):
        # Auth information is contained in praw.ini file. See setup.md
        self.reddit = praw.Reddit("memefeedbot")
        # Comment this out if you need
        self.reddit.read_only = True
        # TODO: Potentially used to backfill data (?)
        # self.pushshift = pmaw.PushshiftAPI(praw=self.reddit)
        # Sentry monitoring:
        # TODO: Isn't this already handled by django app?
        sentry_sdk.init(
            dsn="https://ef5d88ef4fe1411f8a626d67f8ee3317@o4504333010731009.ingest.sentry.io/4504365878673408",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
        )

    def __load_submission(self, submission: praw.models.Submission):
        """
        Build dictionary that applies map_func to each value.
        """
        # Only take submissions in input
        if type(submission) is not praw.models.Submission:
            sentry_sdk.capture_message("Attempted to load non praw.models.Submission type in " 
            + self.__class__.__name__
            + "with" + self.__class__.__load_submission.__name__
            + str(submission))
            return {}
        foreign_key_dependencies = {}
        created_model = {}
        for model_name, model in RedditETL.MODEL_MAPPINGS.items():
            # Convert submission to the corresponding dict for django model **kwargs
            output_model = {}
            for k, v in model.items():
                map_func, attr_val = v
                if map_func is not None:
                    output_model[k] = map_func(submission, attr_val)
                else:
                    output_model[k] = attr_val
            # To avoid race condition? TODO: Do i need to save() author, subreddit before submission?
            # Convert Dict to django model
            if model_name == "AUTHOR":
                output_model["name"] = output_model["name"].name
                created_model = Author(**output_model)
                foreign_key_dependencies["author"] = {
                    "submission": created_model
                }
            elif model_name == "SUBREDDIT":
                output_model["name"] = output_model["name"].display_name
                created_model = Subreddit(**output_model)
                foreign_key_dependencies["subreddit"] = {
                    "submission": created_model
                }
            elif model_name == "SUBMISSION":
                # TODO: Does this create duplicates (?)
                output_model["subreddit"] = foreign_key_dependencies["subreddit"]["submission"]
                output_model["author"] = foreign_key_dependencies["author"]["submission"]
                created_model = Submission(**output_model)
            # Save models so they can be accessed by foreign key
            created_model.save()
        return created_model

    def __transform_top_submissions(self, top_submissions):
        """
        Transform top submissions to (author: Author, subreddit: dict, submission: dict)
         for model processing.
        """
        transformed_submissions = [
            self.__load_submission(submission)
            for submission in top_submissions
        ]
        return transformed_submissions

        # filtered_attributes_list = [(self.__load_submission(submission, model) for model_name, model in RedditETL.MODEL_MAPPINGS.items()) for submission in top_submissions]
        # Return transposed filtered_attributes_list
        # return list(map(list, zip_longest(*filtered_attributes_list, fillvalue=None)))


    def extract(self):
        """
        Extracts the top N_submissionS_PER_SUBREDDIT from each subreddit in SUBREDDITS_CSV
        """
        submissions = []
        with open(RedditETL.SUBREDDITS_CSV, newline="") as subreddits_csv:
            subreddit_reader = reader(subreddits_csv)
            for row in subreddit_reader:
                # Prune invalid strings / validate strings according to reddit subreddit naming convention
                valid_subreddits_in_row = [
                    sr for sr in row if match("^[A-Za-z0-9_]{3,21}$", sr)
                ]
                # Iterate over subreddits

                for subreddit in valid_subreddits_in_row:
                    top_submissions = []
                    try:
                        # Get top N submissions daily from each subreddit in the list
                        top_submissions = self.reddit.subreddit(subreddit).top(
                            time_filter="day",
                            limit=5 # TODO: REMOVE THIS
                        )

                        # {k:v for k, v in submission if k in RedditETL.ACCEPTED_FIELDS}
                        transformed_submissions = self.__transform_top_submissions(top_submissions)
                        # transformed_submissions = [submission for submission in top_submissions]
                    except praw.exceptions.PRAWException as err:
                        # On error, report to Sentry
                        sentry_sdk.capture_exception(err)
                    else:
                        # TODO: Join subreddit --> Subreddit model
                        # TODO: Join author --> author model
                        # TODO: Batch load to submissiongres
                        submissions += transformed_submissions  
        # Transpose list
        transpose = list(map(list, zip_longest(*submissions, fillvalue=None)))
        print("LEN TRANSPOSE", len(transpose))
        for i in transpose:
            print("LEN I", len(i))
            print(i)
            
        return transpose



    def load(self, submissions):
        """
        Batch load into submissiongres and join with related data models
        """
        # TODO: Change this func as bulk_create doesn't work with models using foreign keys
        # submissions is a list [ [Authors..], [Subreddits..], [Submissions..]]
        authors, subreddits, submissions = submissions
        Author.objects.bulk_create(authors)
        Subreddit.objects.bulk_create(subreddits)
        Submission.objects.bulk_create(submissions)

    def run_pipeline(self):
        """
        Run ETL pipeline.
        """
        # self.get_daily_submissions("anime_irl")
        res = self.extract()
        # Transform does nothing right now as transform functionality is in extract
        res = self.load(res)


RedditETL().run_pipeline()
# Considerations:
# Failure recovery --> Responses are cached, should I retry until finished?
# What about rate limits?
