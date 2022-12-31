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
    def test_image_span_from_url(self):
        # TODO: Future Sprint
        pass

class IndexViewTest(TestCase):
    # Tests for image thumbnail    
    def test_thumbnail_ireddit_jpg(self):
        pass

    def test_thumbnaill_ireddit_png(self):
        pass

    def test_thumbnail_ireddit_gif(self):
        pass

    def test_thumbnail_ireddit_selftext(self):
        pass

    # TODO: Different video formats (?)
    def test_thumbnail_vreddit_video(self):
        pass
    
    def test_thumbnail_reddit_gallery(self):
        # TODO: Write test for full image after implementation
        pass

    def test_thumbnail_imgur(self):
        pass

    def test_thumbnail_misc(self):
        # TODO: Write test for full image after implementation
        pass

    def test_thumbnail_span_ratio_jpg_png(self):
        # TODO: Future Sprint
        pass

    def test_thumbnail_span_ratio_video(self):
        # TODO: Future Sprint
        pass

    # Tests for full image
    def test_full_image_ireddit_jpg_png(self):
        pass

    def test_full_image_ireddit_gif(self):
        pass

    def test_full_image_vreddit_video(self):
        pass

    def test_full_image_vreddit_video(self):
        pass

    def test_full_image_imgur(self):
        pass


    # Tests for pagination
    def test_pagination_submission_count(self):
        """
        Test the default number of records per page.
        """
        pass

    def test_pagination_next_prev_button(self):
        """
        Test the pagination nnext & prev button is correctly displayed and working.
        """
        pass

    def test_pagination_correct_num_pages(self):
        """
        Test the pagination displays the correct number of pages.
        """
        pass

class SearchFormTest(TestCase):
    """
    Test for the SearchForm
    And corresponding FormView SearchResultsView
    """
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
        test_data = cls.instance.reddit.info(cls.ids)
        cls.instance._transform_top_submissions(test_data)

    def flatten_results_list(self, results_list):
        return sum(results_list, [])


    # Tests for Title
    def test_search_exact_title_match(self):
        """
        Test search by exact title returns a result
        """
        # Title corresponding to submission id=zvms2j
        exact_title = "First post on test_memefeed"
        response = self.client.get("/reddit/search/results", data={
            "q": exact_title,
            "sort_by": 0
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )

    def test_title_empty_query_string_returns_all_results(self):
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
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), len(self.ids))

    def test_search_by_invalid_title(self):
        """
        Test search for a title that is not in the database returns no results
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "hgdafghdfgasdgesfsadfsfdsdfvxcvxdfwsfzsdfcxdsdf",
            "sort_by": 0,
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "No submissions found", html=True
        )
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 0)

    # Test search with filter by subreddit
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
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 3)
        for result in results_list:
            self.assertEquals(result.subreddit.name, "test_memefeed")
    
    def test_search_by_invalid_subreddit(self):
        """
        Test search for a subreddit that is not in the database returns no results
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 0,
            "subreddit": "invalid_name"
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "No submissions found", html=True
        )
        # Check all submissions are part of test_memefeed
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 0)

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
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 2)
        for result in results_list:
            self.assertEquals(result.author.name, "YinnerstonMemefeed")

    def test_search_by_invalid_author(self):
        """
        Test search for a title that is not in the database returns no results
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 0,
            "author":  "SomeInvalidAuthor"
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "No submissions found", html=True
        )
        # Check all submissions are part of test_memefeed
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 0)

    # Test Sort
    def test_sort_by_relevance(self):
        # TODO: What should the relevance metric be? Favourites (?)
        pass

    def test_sort_by_score(self):
        """ 
        Sort the responses by score.
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 1,
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )
        # Check that submissions are descending by score
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 6)
        prev_score = None
        for result in results_list:
            if prev_score is not None:
                self.assertLess(result.score, prev_score)
                prev_score = result.score

    def test_sort_by_new(self):
        """
        Test sort submissions in response by new
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 2,
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )
        # Check that submissions are descending by created_utc
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 6)
        prev_time = None
        for result in results_list:
            if prev_time is not None:
                self.assertLess(result.created_utc, prev_time)
                prev_time = result.created_utc

    def test_sort_by_alphabetical(self):
        """
        Test submissions sorted by title
        """
        response = self.client.get("/reddit/search/results", data={
            "q": "",
            "sort_by": 3,
        })
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, "No submissions found", html=True
        )
        # Check that submissions are descending by score
        results_list =  self.flatten_results_list(response.context['results_list'])
        self.assertEqual(len(results_list), 6)
        prev_title = None
        for result in results_list:
            if prev_title is not None:
                self.assertLess(result.title, prev_title)
                prev_title = result.title



# TODO: Django views / template testing