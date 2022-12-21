import praw
import pmaw
from csv import reader
from re import match
import sentry_sdk


class RedditETL:
    """
    Class that ingests data from reddit and puts it into the postgres db.
    """
    CACHE_DIR = './cache'
    SUBREDDITS_CSV = 'data/subreddits.csv'
    # TODO: Remove in production alongside usage in extract()
    N_POSTS_PER_SUBREDDIT = 5

    def __init__(self):
        # Auth information is contained in praw.ini file. See setup.md
        self.reddit = praw.Reddit('memefeedbot')
        # Comment this out if you need
        self.reddit.read_only = True
        # TODO: Potentially used to backfill data (?)
        self.pushshift = pmaw.PushshiftAPI(praw=self.reddit)
        # Sentry monitoring:
        # TODO: Isn't this already handled by django app?
        sentry_sdk.init(
            dsn="https://ef5d88ef4fe1411f8a626d67f8ee3317@o4504333010731009.ingest.sentry.io/4504365878673408",

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0
        )



    def extract(self):
        with open(RedditETL.SUBREDDITS_CSV, newline='') as subreddits_csv:
            subreddit_reader = reader(subreddits_csv)
            for row in subreddit_reader:
                # Prune invalid strings / validate strings
                valid_subreddits_in_row = [sr for sr in row if match("^[A-Za-z0-9_]{3,21}$", sr)]
                # Iterate over subreddits
                for subreddit in valid_subreddits_in_row:
                    posts = []
                    error_msg = ''
                    try:
                        # Get top N posts daily from each subreddit in the list
                        posts = self.reddit.subreddit(subreddit).top(time_filter="day", limit=RedditETL.N_POSTS_PER_SUBREDDIT)
                    except praw.errors.HTTPException as err:
                        # On error, report to Sentry
                        sentry_sdk.capture_exception(err)
                    else:
                        for post in posts:  
                            print(post.title, post.score, post.author, post.id, post.url, post.selftext, post.media)
                            



    def transform(self):
        pass

    def load(self):
        pass



RedditETL().extract()
# Considerations:
# Failure recovery --> Responses are cached, should I retry until finished?
# What about rate limits?

