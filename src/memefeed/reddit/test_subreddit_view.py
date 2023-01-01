from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from scripts.reddit_etl import RedditETL
import sentry_sdk

class TestSubredditView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL()
        sentry_sdk.init(dsn="")
        cls.ids = [
            "t3_zzye6e",    # jpg nsfw
            "t3_zzyds7",    # gif
            "t3_zzydk5",    # png
            "t3_zzycfr",    # Jpg
            "t3_100f2k6",   # Imgur
        ]
        test_data = cls.instance.reddit.info(fullnames=cls.ids)
        cls.instance._transform_top_submissions(test_data)

    def test_subreddit_displays_correct_results(self):
        """
        Test the subreddit displays the correct number of results
        """
        response = self.client.get(reverse('reddit:subreddit_view', args=("test_memefeed",)))
        # Check that there are 5 displayed submissions --> One row of 5 elements
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context["subreddit"].name, "test_memefeed")
        self.assertEquals(len(response.context["top_submissions_list"]), 1)
        self.assertEquals(len(response.context["top_submissions_list"][0]), 5)
        # Check that each submission belongs to the subreddit "test_memefeed"
        for submission in response.context["top_submissions_list"][0]:
            self.assertEquals(submission.subreddit.name, "test_memefeed")

    def test_invalid_subreddit(self):
        """
        Test the subreddit view displays no results for an invalid subreddit.
        """
        response = self.client.get(reverse('reddit:subreddit_view', args=("invalid_subreddit",)))
        # Check that there are 0 displayed submissions
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "No submissions found")
        self.assertContains(response, "Invalid subreddit name")