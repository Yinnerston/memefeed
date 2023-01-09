"""
Test SearchForm, SearchResultsView and results.html template
"""

from django.test import TestCase
from scripts.reddit_etl import RedditETL

# from reddit.forms import SearchForm
from reddit.models import Author, Subreddit, Submission
from http import HTTPStatus
import sentry_sdk


class SearchFormTest(TestCase):
    """
    Test for the SearchForm
    And corresponding FormView SearchResultsView
    """

    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL(testing=True)
        sentry_sdk.init(dsn="")
        # Set up data for the whole TestCase
        cls.ids = [
            "t3_zzyds7",  # gif on test_memefeed
            "t3_zzydk5",  # png on test_memefeed
            "t3_zzycfr",  # jpg on test_memefeed
            "t3_104wtz7",  # png on u_YinnerstonTest
            "t3_104wtfy",  # jpg on u_YinnerstonTest
            "t3_10770f4",  # jpg on u_YinnerstonMemefeed
        ]
        test_data = cls.instance.reddit.info(fullnames=cls.ids)
        cls.instance._transform_top_submissions(test_data)

    def flatten_results_list(self, results_list):
        return sum(results_list, [])

    # Tests for Title
    def test_search_exact_title_match(self):
        """
        Test search by exact title returns a result
        """
        # Title corresponding to submission id=zvms2j
        exact_title = "Test JPG"
        response = self.client.get(
            "/reddit/search/results", data={"q": exact_title, "sort_by": 0}
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")

    def test_title_empty_query_string_returns_all_results(self):
        """
        Test empty query string returns all results.
        """
        response = self.client.get(
            "/reddit/search/results",
            data={
                "q": "",
                "sort_by": 0,
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check all submissions are present
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), len(self.ids))

    def test_search_by_invalid_title(self):
        """
        Test search for a title that is not in the database returns no results
        """
        response = self.client.get(
            "/reddit/search/results",
            data={
                "q": "hgdafghdfgasdgesfsadfsfdsdfvxcvxdfwsfzsdfcxdsdf",
                "sort_by": 0,
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "No submissions found")
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), 0)

    # Test search with filter by subreddit
    def test_search_filter_by_specific_subreddit(self):
        """
        Test search by specific subreddit
        """
        # Title corresponding to submission id=zvms2j
        response = self.client.get(
            "/reddit/search/results",
            data={"q": "", "sort_by": 0, "subreddit": "test_memefeed"},
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check all submissions are part of test_memefeed
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), 3)
        for result in results_list:
            self.assertEquals(result.subreddit.name, "test_memefeed")

    def test_search_filter_by_multiple_subreddit(self):
        """
        TODO:
        """
        response = self.client.get(
            "/reddit/search/results?q=&subreddit=test_memefeed&subreddit=u_YinnerstonTest&sort_by=0",
            # data={"q": "", "sort_by": 0, "subreddit": "test_memefeed"},
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check all submissions are part of test_memefeed
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), 5)

        for result in results_list:
            self.assertIn(result.subreddit.name, ["test_memefeed", "u_YinnerstonTest"])

    def test_search_by_invalid_subreddit(self):
        """
        Test search for a subreddit that is not in the database returns no results
        """
        response = self.client.get(
            "/reddit/search/results",
            data={"q": "", "sort_by": 0, "subreddit": "invalid_name"},
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "No submissions found")
        # Check all submissions are part of test_memefeed
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), 0)

    def test_search_filter_by_author(self):
        """
        Test search by specific author
        """
        # Title corresponding to submission id=zvms2j
        response = self.client.get(
            "/reddit/search/results",
            data={"q": "", "sort_by": 0, "author": "YinnerstonTest"},
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check all submissions were authored by YinnerstonTest
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), 5)
        for result in results_list:
            self.assertEquals(result.author.name, "YinnerstonTest")

    def test_search_by_invalid_author(self):
        """
        Test search for a title that is not in the database returns no results
        """
        response = self.client.get(
            "/reddit/search/results",
            data={"q": "", "sort_by": 0, "author": "SomeInvalidAuthor"},
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "No submissions found")
        # Check all submissions are part of test_memefeed
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), 0)

    # Test Sort
    def test_sort_by_relevance(self):
        # TODO: What should the relevance metric be? Favourites (?)
        pass

    def test_sort_by_score(self):
        """
        Sort the responses by score.
        """
        response = self.client.get(
            "/reddit/search/results",
            data={
                "q": "",
                "sort_by": 1,
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check that submissions are descending by score
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), len(self.ids))
        prev_score = None
        for result in results_list:
            if prev_score is not None:
                self.assertLess(result.score, prev_score)
                prev_score = result.score

    def test_sort_by_new(self):
        """
        Test sort submissions in response by new
        """
        response = self.client.get(
            "/reddit/search/results",
            data={
                "q": "",
                "sort_by": 2,
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check that submissions are descending by created_utc
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), len(self.ids))
        prev_time = None
        for result in results_list:
            if prev_time is not None:
                self.assertLess(result.created_utc, prev_time)
                prev_time = result.created_utc

    def test_sort_by_alphabetical(self):
        """
        Test submissions sorted by title
        """
        response = self.client.get(
            "/reddit/search/results",
            data={
                "q": "",
                "sort_by": 3,
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "No submissions found")
        # Check that submissions are descending by score
        results_list = self.flatten_results_list(response.context["results_list"])
        self.assertEqual(len(results_list), len(self.ids))
        prev_title = None
        for result in results_list:
            if prev_title is not None:
                self.assertLess(result.title, prev_title)
                prev_title = result.title
