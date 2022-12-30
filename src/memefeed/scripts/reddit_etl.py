"""
Extract daily top reddit submissions for each subreddit in SUBREDDITS_CSV.
Call this script in the manage.py shell from src/memefeed (/app in docker container)
"""
import praw

# import pmaw
from csv import reader
from re import match
import sentry_sdk

# import requests

from scripts.etl_utils import *
from reddit.models import Author, Subreddit, Submission
from django.db import DatabaseError, transaction
from django.core.exceptions import ObjectDoesNotExist


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

    # CACHE_DIR = "./cache"

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
        "secure_media_embed",
    ]

    # Mappings
    # Key: attribute name in Django model
    # Value: Tuple(
    #   function to apply to praw.models.Submission or None
    #   argument for above function or value that is attribute that is set in django model if function is None
    # )
    AUTHOR_MAP = {
        "name": (author_getattr, "author"),
        # "favourite": (None, False),
    }
    SUBREDDIT_MAP = {
        "name": (subreddit_getattr, "subreddit"),
        # "favourite": (None, False),
    }
    SUBMISSION_MAP = {
        "title": (getattr, "title"),
        "score": (getattr, "score"),
        "url": (getattr, "url"),
        "created_utc": (unix_timestamp_getattr, "created_utc"),
        "domain": (getattr, "domain"),
        "id": (getattr, "id"),
        "is_self": (getattr, "is_self"),
        "is_video": (getattr, "is_video"),
        "media_only": (getattr, "media_only"),
        "media": (filter_null_getattr_list, "media"),
        "media_embed": (filter_null_getattr_list, "media_embed"),
        "selftext": (filter_null_getattr_str, "selftext"),
        "selftext_html": (filter_null_getattr_list_bleach, "selftext_html"),
        "nsfw": (getattr, "over_18"),
        "thumbnail": (getattr, "thumbnail"),
        "secure_media": (filter_null_getattr_list, "secure_media"),
        "secure_media_embed": (filter_null_getattr_list, "secure_media_embed"),
        # Foreign keys
        "author": (author_getattr, "author"),
        "subreddit": (subreddit_getattr, "subreddit"),
    }
    MODEL_MAPPINGS = {
        "AUTHOR": AUTHOR_MAP,
        "SUBREDDIT": SUBREDDIT_MAP,
        "SUBMISSION": SUBMISSION_MAP,
    }


    def __init__(self, subreddits_csv="scripts/data/subreddits.csv"):
        # Auth information is contained in praw.ini file. See setup.md
        self.reddit = praw.Reddit("memefeedbot")
        self.reddit.read_only = True

        self.SUBREDDITS_CSV = subreddits_csv
        sentry_sdk.init(
            dsn="https://ef5d88ef4fe1411f8a626d67f8ee3317@o4504333010731009.ingest.sentry.io/4504365878673408",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
        )

    def _load_submission(self, submission: praw.models.Submission):
        """
        Build dictionary that applies map_func to each value.
        """
        # Only take submissions in input
        if type(submission) is not praw.models.Submission:
            sentry_sdk.capture_message(
                "Attempted to load non praw.models.Submission type in "
                + self.__class__.__name__
                + "with"
                + self.__class__._load_submission.__name__
                + str(submission)
            )
            return {}
        foreign_key_dependencies = {}
        obj = None
        created = None
        try:
            # Each Reddit post --> (Author, Subreddit, Submission) is atomic
            with transaction.atomic():
                for model_name, model in RedditETL.MODEL_MAPPINGS.items():                
                        # Convert submission to the corresponding dict for django model **kwargs
                        output_model = {}
                        for k, v in model.items():
                            map_func, attr_val = v
                            if map_func is not None:
                                output_model[k] = map_func(submission, attr_val)
                            else:
                                output_model[k] = attr_val
                        # use Try/Except with ObjectDoesNotExist because to avoid IntegrityError from unsanitized input
                        # Only the first iteration of a post is saved. Subsequent runs do not insert / update
                        # Convert output_model Dict to django model
                        obj = None
                        if model_name == "AUTHOR":
                            try:
                                obj = Author.objects.get(name=output_model["name"])
                            except ObjectDoesNotExist:
                                obj = Author.objects.create(**output_model)
                            foreign_key_dependencies["author"] = {
                                "submission": obj,  # Primary key of Author used by Submission
                            }
                        elif model_name == "SUBREDDIT":
                            try:
                                obj = Subreddit.objects.get(name=output_model["name"])
                            except ObjectDoesNotExist:
                                obj = Subreddit.objects.create(**output_model)
                            foreign_key_dependencies["subreddit"] = {
                                "submission": obj,  # Primary key of Subreddit used by Submission
                            }
                        elif model_name == "SUBMISSION":
                            output_model["subreddit"] = foreign_key_dependencies["subreddit"][
                                "submission"
                            ]
                            output_model["author"] = foreign_key_dependencies["author"][
                                "submission"
                            ]
                            try:
                                obj = Submission.objects.get(id=output_model["id"])
                            except ObjectDoesNotExist:
                                obj = Submission.objects.create(**output_model)
                        
        except DatabaseError as e:
            # Expected behaviour for a invalid post is to report , ignore it and add subsequent posts
            sentry_sdk.capture_exception(e)
        except Exception as e:
            sentry_sdk.capture_exception(e)
        return obj

    def _transform_top_submissions(self, top_submissions):
        """
        Apply transformation to each submission in top_submissions.
        Then load them into django postgres db.
        """
        transformed_submissions = [
            self._load_submission(submission) for submission in top_submissions
        ]
        return transformed_submissions

    def run_pipeline(self):
        """
        Extracts the top N_submissionS_PER_SUBREDDIT from each subreddit in SUBREDDITS_CSV
        """
        
        with open(self.SUBREDDITS_CSV, newline="") as subreddits_csv:
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
                            time_filter="day"
                        )

                        # {k:v for k, v in submission if k in RedditETL.ACCEPTED_FIELDS}
                        self._transform_top_submissions(
                            top_submissions
                        )
                        # transformed_submissions = [submission for submission in top_submissions]
                    except praw.exceptions.PRAWException as err:
                        # On error, report to Sentry
                        sentry_sdk.capture_exception(err)

# Considerations:
# Failure recovery --> Responses are cached, should I retry until finished?
# What about rate limits?
