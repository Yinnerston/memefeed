"""
Util helpers for reddit_etl.py
"""

import praw
import pytz
from datetime import datetime

# Getattr wrapper functions for author, subreddit foreign key in Submission
def author_getattr(submission: praw.models.Submission, field_to_get: str):
    return getattr(submission, field_to_get).name

def subreddit_getattr(submission: praw.models.Submission, field_to_get: str):
    return getattr(submission, field_to_get).display_name

def unix_timestamp_getattr(submission, field_to_get):
    datetime_utc = datetime.utcfromtimestamp(getattr(submission, field_to_get))
    return pytz.utc.localize(datetime_utc)

