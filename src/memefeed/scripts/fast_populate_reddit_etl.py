"""
Quickly populate the database by getting entries with different granularities.
Use this to quickly populate the production db.
"""

from scripts.reddit_etl import RedditETL
from reddit.models import Submission
from csv import reader
import sentry_sdk
from re import match
import praw


def fast_populate():
    r = RedditETL()
    with open(r.SUBREDDITS_CSV, newline="") as subreddits_csv:
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
                    # Get top N submissions for this week and this year
                    yearly_top = r.reddit.subreddit(subreddit).top(time_filter="year")
                    weekly_top = r.reddit.subreddit(subreddit).top(time_filter="week")
                    r._transform_top_submissions(yearly_top)
                    r._transform_top_submissions(weekly_top)
                    # transformed_submissions = [submission for submission in top_submissions]
                except praw.exceptions.PRAWException as err:
                    # On error, report to Sentry
                    sentry_sdk.capture_exception(err)


fast_populate()
print(
    "Total number of submissions:",
    Submission.objects.count(),
)
