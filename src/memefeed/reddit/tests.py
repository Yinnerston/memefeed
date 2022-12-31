from django.test import TestCase
from scripts.reddit_etl import RedditETL
from reddit.forms import SearchForm
from reddit.models import Author, Subreddit, Submission
from http import HTTPStatus
# Create your tests here.

# Also testing some of the behaviour in `src\memefeed\scripts\test.py`
class AuthorTest(TestCase):  
    pass

class SubredditTest(TestCase):
    pass

class SubmissionTest(TestCase):
    def test_image_span_from_url(self):
        # TODO: Future Sprint
        pass