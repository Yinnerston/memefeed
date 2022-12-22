import praw

# import pmaw
from csv import reader
from re import match
import sentry_sdk


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
                        posts.append((subreddit, top_posts))
        return posts

    def transform(self, posts_tuples):
        """
        Transforms data in the form [(subreddit: string, top_posts: [..]), ..] to format stored in db
        """
        # TODO: Cache subreddit table (?) so you can map subreddit name to foreign key
        # TODO: Determine encoding format for media and each attribute?
        for subreddit, posts in posts_tuples:
            for post in posts:
                # TODO: Which fields to store?
                # Media fields --> media, video_only, media_only, etc.. ?
                # Id fields --> id, url,
                print(
                    post.title,
                    post.score,
                    post.author,
                    subreddit,
                    post.id,
                    post.url,
                    post.selftext,
                    post.media,
                    post.flair,
                    post.thumbnail,
                )

    def load(self):
        """
        Batch load into postgres and join with related data models
        """
        pass

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
