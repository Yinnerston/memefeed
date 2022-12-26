"""
Test cases for reddit_etl.py script.
"""
from django.test import TestCase
from .reddit_etl import RedditETL
from reddit.models import Author, Subreddit, Submission
import httpretty
import praw
import sentry_sdk

class RedditETLTest(TestCase):
    """
    Testing ETL process
    """

    def setUp(self):
        """
        Called automatically on startup by django test framework
        """
        self.test_instance = RedditETL()
        # Disable sending error messages to sentry whilst testing
        sentry_sdk.init(dsn="")

    def get_example_submission(self):
        """
        Returns a single example submission in the format returned by the 
        praw.Subreddit.top function
        """
        reddit = self.test_instance.reddit
        # Example on a different subreddit
        # self.test_instance.reddit.submission("zvms2j")
        return reddit.submission(id='zvly7g')


    @httpretty.activate(verbose=True, allow_net_connect=False)
    def mock_reddit_top_submissions(self):
        # TODO: Mock for each subreddit
        httpretty.register_uri(
            httpretty.GET,
            "https://", # reddit.json for top submissions
            body='{...}' # TODO:
        )

    def test_load_submission_valid_submission(self):
        """
        Test that a valid submission is loaded into the database.
        """
        submission = self.get_example_submission()
        
        # Load submission into db
        loaded_submission = self.test_instance.__load_submission(submission)
        # Check that Author is in database
        self.assertTrue(Author.objects.get(name=submission.author).exists())
        # Check that Subreddit is in database
        self.assertTrue(Subreddit.objects.get(name=submission.subreddit).exists())
        # Check that submission is in database
        self.assertTrue(Submission.objects.get(id=submission.id).exists())

    def test_load_submission_submission_is_none(self):
        submission = None # Some invalid submission
        # Load submission into db
        loaded_submission = self.test_instance.__load_submission(submission)
        self.assertIs(loaded_submission, {})
        # Check that Author is in database
        self.assertFalse(Author.objects.get(name=submission.author).exists())
        # Check that Subreddit is in database
        self.assertFalse(Subreddit.objects.get(name=submission.subreddit).exists())
        # Check that submission is in database
        self.assertFalse(Submission.objects.get(id=submission.id).exists())


    def test_load_submission_same_author_different_subreddits(self):
        """
        Test author isn't duplicated in db when two different submissions with the same
        author are added.
        """
        # Add two submissions by the same user on different subreddits
        # To the database
        submission = self.test_instance.reddit.submission("zvms2j")
        duplicate_author_submission = self.get_example_submission()
        submission_loaded_first = self.test_instance.__load_submission(submission)
        submission_loaded_second = self.test_instance.__load_submission(duplicate_author_submission)
        # Check that there's only one author saved
        self.assertTrue(Author.objects.get(name=submission.author).exists())
        self.assertEquals(Author.objects.count(), 1)
        # Check that there are two subreddits saved
        self.assertTrue(Subreddit.objects.get(name=submission.subreddit).exists())
        self.assertTrue(Subreddit.objects.get(name=duplicate_author_submission.subreddit).exists())
        self.assertEquals(Subreddit.objects.count(), 2)
        # Check that there are two submissions saved
        self.assertTrue(Submission.objects.get(id=submission.id).exists())
        self.assertEquals(Subreddit.objects.count(), 2)

    def test_load_submission_different_author_same_subreddit(self):
        """
        Test subreddit isn't duplicated in db when two different submissions with the same
        subreddit are added.
        """
        submission = self.test_instance.reddit.submission("zvms2j")
        different_author_same_subreddit_submission = self.test_instance.reddit.submission("zvn17h")
        submission_loaded_first = self.test_instance.__load_submission(submission)
        submission_loaded_second = self.test_instance.__load_submission(different_author_same_subreddit_submission)
        # Check there are two distinct authors
        self.assertTrue(Author.objects.get(name=submission.author).exists())
        self.assertTrue(Author.objects.get(name=different_author_same_subreddit_submission.author).exists())
        self.assertEquals(Author.objects.count(), 2)
        # Check there's only one subreddit saved
        self.assertTrue(Subreddit.objects.get(name=submission.subreddit).exists())
        self.assertEquals(Subreddit.objects.count(), 1)
        # Check there's two submissions
        self.assertTrue(Submission.objects.get(id=submission.id).exists())
        self.assertEquals(Subreddit.objects.count(), 2)


    def test_load_submission_duplicate_submission(self):
        """
        Check that the same submission loaded twice, only loads into the database once without duplication.
        """
        submission = self.get_example_submission()
        # Load same submission twice using __load_submission
        self.test_instance.__load_submission(submission)
        self.test_instance.__load_submission(submission)
        # Check that only one Author, Subreddit, Submission has been loaded 
        self.assertTrue(Author.objects.get(name=submission.author).exists())
        self.assertEquals(Author.objects.count(), 1)
        self.assertTrue(Subreddit.objects.get(name=submission.subreddit).exists())
        self.assertEquals(Subreddit.objects.count(), 1)
        self.assertTrue(Submission.objects.get(id=submission.id).exists())
        self.assertEquals(Subreddit.objects.count(), 1)

    def test_load_submission_EOM(self):
        """
        Test the behaviour when posts is too large to fit into memory
        """
        # TODO:
        pass

    def test_load_submission_invalid_map_func_plus_recovery(self):
        """
        Test that loading invalid models doesn't work.
        Test that the one atempted invalid insertion doesn't break the functionality.
        """
        # Define some invalid function
        def invalid_test_func(param):
            raise Exception("Expected Exception " + param)
        self.test_instance.AUTHOR_MAP["invalid"] = (invalid_test_func, "invalid_field")
        post = self.get_example_submission()
        self.test_instance.__load_submission(post)
        # Check that invalid model hasn't been loaded
        self.assertEquals(Author.objects.count(), 0)
        self.assertEquals(Subreddit.objects.count(), 0)
        self.assertEquals(Subreddit.objects.count(), 0)
        # Check that you can still perform valid inserts after failure
        self.test_instance.AUTHOR_MAP.pop("invalid")
        self.test_instance.__load_submission(post)
        self.assertEquals(Author.objects.count(), 1)
        self.assertEquals(Subreddit.objects.count(), 1)
        self.assertEquals(Subreddit.objects.count(), 1)

    def test_transform_top_submissions_valid_input(self):
        """
        Given a valid input from Reddit.top_submissions, correctly
        """
        submissions_list = self.test_instance.reddit.subreddit("funny").top(limit=1, time_filter="day")
        transformed = self.test_instance.__transform_top_submissions(submissions_list)
        self.assertEquals(Author.objects.count(), 1)
        self.assertEquals(Subreddit.objects.count(), 1)
        self.assertEquals(Subreddit.objects.count(), 1)

