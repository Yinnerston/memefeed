from django.test import TestCase
from scripts.reddit_etl import RedditETL
import sentry_sdk
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
    pass

class SubmissionSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL()
        sentry_sdk.init(dsn="")
        # Set up data for the whole TestCase
        cls.ids = [
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
        response = self.client.get("/reddit/search/", data={
            "q": exact_title,
            "sort_by": 0
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )

    def test_search_filter_by_subreddit(self):
        """
        Test search by specific subreddit
        """
        # Title corresponding to submission id=zvms2j
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 0,
            "subreddit": "test_memefeed"
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )
        # Check all submissions are part of test_memefeed
        results_list =  response.context['results_list']
        self.assertEqual(len(results_list), 3)
        for result in results_list:
            self.assertEquals(result.subreddit.name, "test_memefeed")

    def test_search_filter_by_author(self):
        """
        Test search by specific author
        """
        # Title corresponding to submission id=zvms2j
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 0,
            "author":  "YinnerstonMemefeed"
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )
        # Check all submissions are part of test_memefeed
        results_list =  response.context['results_list']
        self.assertEqual(len(results_list), 2)
        for result in results_list:
            self.assertEquals(result.author.name, "YinnerstonMemefeed")

    def test_empty_query_string_returns_all_results(self):
        """
        Test empty query string returns all results.
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 0,
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )
        # Check all submissions are present
        results_list =  response.context['results_list']
        self.assertEqual(len(results_list), len(self.ids))

    def test_sort_by_relevance(self):
        pass

    def test_sort_by_score(self):
        pass

    def test_sort_by_new(self):
        pass

    def test_sort_by_alphabetical(self):
        pass

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


# TODO: Django views / template testing