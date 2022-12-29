from django.test import TestCase
from scripts.reddit_etl import RedditETL
import sentry_sdk
from reddit.forms import SearchForm
from reddit.models import Author, Subreddit, Submission
# Create your tests here.

# Also testing some of the behaviour in `src\memefeed\scripts\test.py`
class AuthorTest(TestCase):  
    pass

class SubredditTest(TestCase):
    pass

class SubmissionTest(TestCase):
    pass

class SubmissionSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL()
        sentry_sdk.init(dsn="")
        # Set up data for the whole TestCase
        ids = [
            "t3_zvn17h",
            "t3_zvms2j",
            "t3_zvmrlj",
            "t3_tqbf9w",
            "t3_vj1p48",
            "t3_sphocx",
        ]
        test_data = cls.instance.reddit.info(ids)
        cls.instance._transform_top_submissions(test_data)

    def test_search_exact_title_match(self):
        """
        Test search by exact title returns a result
        """
        # Title corresponding to submission id=zvms2j
        exact_title = "First post on test_memefeed"
        form = SearchForm({
            "q": exact_title
        })
        if form.is_valid():
            self.assertIsNotNone(form.cleaned_data)
            self.assertEquals(len(form.cleaned_data), 1)


    def test_search_filter_by_subreddit(self):
        """
        Test search by specific subreddit
        """
        # Title corresponding to submission id=zvms2j
        subreddit = "test_memefeed"
        form = SearchForm({
            "subreddit": subreddit
        })
        if form.is_valid():
            self.assertIsNotNone(form.cleaned_data)
            # Check len is 3
            self.assertEquals(len(form.cleaned_data), 3)

    def test_search_filter_by_author(self):
        """
        Test search by specific author
        """
        # Title corresponding to submission id=zvms2j
        author = "YinnerstonMemefeed"
        form = SearchForm({
            "author": author
        })
        if form.is_valid():
            self.assertIsNotNone(form.cleaned_data)
            # Check len is 2
            self.assertEqual(len(form.cleaned_data), 2)

    def test_search_by_invalid_title(self):
        """
        Test search for a title that is not in the database returns no results
        """
        pass

    def test_search_by_invalid_subreddit(self):
        """
        Test search for a subreddit that is not in the database returns no results
        """
        pass

    def test_search_by_invalid_author(self):
        """
        Test search for a title that is not in the database returns no results
        """
        pass
