import praw

# import pmaw
from csv import reader
from re import match
import sentry_sdk

# TODO: Define reddit submission model in reddit/models.py
# bulk_create() to load into model
# Figure out how to do the foreign key3


class RedditETL:
    """
    Class that ingests data from reddit and puts it into the postgres db.
    """

    CACHE_DIR = "./cache"
    SUBREDDITS_CSV = "data/subreddits.csv"
    # TODO: Remove in production alongside usage in extract()
    N_POSTS_PER_SUBREDDIT = 5

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

    def extract(self):
        """
        Extracts the top N_POSTS_PER_SUBREDDIT from each subreddit in SUBREDDITS_CSV
        """
        posts = []
        with open(RedditETL.SUBREDDITS_CSV, newline="") as subreddits_csv:
            subreddit_reader = reader(subreddits_csv)
            for row in subreddit_reader:
                # Prune invalid strings / validate strings according to reddit subreddit naming convention
                valid_subreddits_in_row = [
                    sr for sr in row if match("^[A-Za-z0-9_]{3,21}$", sr)
                ]
                # Iterate over subreddits

                for subreddit in valid_subreddits_in_row:
                    top_posts = []
                    try:
                        # Get top N posts daily from each subreddit in the list
                        top_posts = self.reddit.subreddit(subreddit).top(
                            time_filter="day", limit=RedditETL.N_POSTS_PER_SUBREDDIT
                        )
                    except praw.exceptions.PRAWException as err:
                        # On error, report to Sentry
                        sentry_sdk.capture_exception(err)
                    else:
                        # TODO: Join subreddit --> Subreddit model
                        # TODO: Join author --> author model
                        # TODO: Batch load to postgres
                        posts += top_posts
                    break

        return posts

    def transform(self, posts):
        """
        Transforms data in the form [(subreddit: string, top_posts: [..]), ..] to format stored in db
        """
        # TODO: Cache subreddit table (?) so you can map subreddit name to foreign key
        # TODO: Determine encoding format for media and each attribute?
        for post in posts:
            # TODO: Which fields to store?
            # Media fields --> media, video_only, media_only, etc.. ?
            # Id fields --> id, url,
            print(
                "title " + str(post.title),
                "author " + str(post.author),
                "id " + str(post.id),
                "score " + str(post.score),
                "url " + str(post.url),
                "domain " + str(post.domain),
                "subreddit " + str(post.subreddit),
                "subreddit_id " + str(post.subreddit_id),
                "created_utc " + str(post.created_utc),
                "category " + str(post.category),
                "content_categories " + str(post.content_categories),
                "discussion_type " + str(post.discussion_type),
                "is_self " + str(post.is_self),  # if True, only text
                "is_video " + str(post.is_video),  # If True, then video in media
                "media " + str(post.media),
                "media_embed " + str(post.media_embed),
                "media_only " + str(post.media_only),
                "selftext " + str(post.selftext),
                "selftext_html " + str(post.selftext_html),
                "over_18 " + str(post.over_18),  # if True, thumbnail is nsfw
                "thumbnail " + str(post.thumbnail),  # Either jpg url, nsfw or none
                "secure_media " + str(post.secure_media),
                "secure_media_embed " + str(post.secure_media_embed),
                sep="\n",
            )
            print("---")

    def load(self, res):
        """
        Batch load into postgres and join with related data models
        """
        return res

    def run_pipeline(self):
        """
        Run ETL pipeline.
        """
        res = self.extract()
        res = self.transform(res)
        res = self.load(res)


RedditETL().run_pipeline()
# Considerations:
# Failure recovery --> Responses are cached, should I retry until finished?
# What about rate limits?
