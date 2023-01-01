"""
Util helpers for reddit_etl.py
"""

import praw
import pytz
from datetime import datetime
import bleach

# Getattr wrapper functions for author, subreddit foreign key in Submission
def author_getattr(submission: praw.models.Submission, field_to_get: str) -> str:
    return getattr(submission, field_to_get).name


def subreddit_getattr(submission: praw.models.Submission, field_to_get: str) -> str:
    return getattr(submission, field_to_get).display_name


def unix_timestamp_getattr(submission: praw.models.Submission, field_to_get: str) -> datetime:
    datetime_utc = datetime.utcfromtimestamp(getattr(submission, field_to_get))
    return pytz.utc.localize(datetime_utc)

def filter_null_getattr_list(submission: praw.models.Submission, field_to_get: str):
    attr = getattr(submission, field_to_get)
    return attr if attr is not None else {}

def filter_null_getattr_str(submission: praw.models.Submission, field_to_get: str):
    attr = getattr(submission, field_to_get)
    return attr if attr is not None else ""

def filter_null_getattr_list_bleach(submission: praw.models.Submission, field_to_get: str):
    attr = getattr(submission, field_to_get)
    if attr is not None:
        attr = bleach.clean(attr)
    return attr if attr is not None else {}

def filter_getattr_media_metadata_image_url_list(submission: praw.models.Submission, media_metadata: str):
    """
    Get the media metadata if the submission has it, otherwise return [].
    Used to retain metadata for galeries
    """
    # TODO: Make mgiration in Submissions and implement in scripts/reddit_etl.py
    if media_metadata != "media_metadata":
        return []
    urls = []
    try:
        attr = getattr(submission, media_metadata)
        for k, v in attr.items():
            url = v['p'][0]['u']
            url = url.split("?")[0].replace("preview","i")
            urls.append(url)
    except AttributeError:
        urls = []
    finally:
        return urls
