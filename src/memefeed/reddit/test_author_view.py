"""
Test author view
"""
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from scripts.reddit_etl import RedditETL
import sentry_sdk


class TestAuthorView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL(testing=True)
        sentry_sdk.init(dsn="")
        cls.ids = [
            "t3_107fhdp",  # Jpg by u/YinnerstonMemefeed
            "t3_107fsn7",  # Jpg by u/YinnerstonMemefeed
            "t3_100f2k6",  # Imgur by u/YinnerstonTest
            "t3_zzye6e",  # Jpg nsfw by u/YinnerstonTest
        ]
        test_data = cls.instance.reddit.info(fullnames=cls.ids)
        cls.instance._transform_top_submissions(test_data)

    def test_author_displays_correct_results(self):
        """
        Test the author displays the correct number of results
        """
        response = self.client.get(
            reverse("reddit:author_view", args=("YinnerstonMemefeed",))
        )
        # Check that there are 2 displayed submissions --> One row of 2 elements
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context["author"].name, "YinnerstonMemefeed")
        self.assertEquals(len(response.context["top_submissions_list"]), 1)
        self.assertEquals(len(response.context["top_submissions_list"][0]), 2)
        # Check that each submission belongs to the subreddit "test_memefeed"
        for submission in response.context["top_submissions_list"][0]:
            self.assertEquals(submission.author.name, "YinnerstonMemefeed")

    def test_invalid_author(self):
        """
        Test the author view displays no results for an invalid author.
        """
        response = self.client.get(
            reverse("reddit:author_view", args=("invalid_author",))
        )
        # Check that there are 0 displayed submissions
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "No submissions found")
        self.assertContains(response, "Invalid author name")
