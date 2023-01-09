"""
Test compose search page.
"""
from django.test import TestCase
from scripts.reddit_etl import RedditETL
import sentry_sdk
from reddit.models import Subreddit


class SearchFormTest(TestCase):
    """
    Test search form and results
    """

    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL(testing=True)
        sentry_sdk.init(dsn="")
        cls.ids = [
            "t3_zzyds7",  # gif
            "t3_zzydk5",  # png
            "t3_zzycfr",  # jpg
            "t3_104wtz7",  # png on different subreddit
            "t3_104wtfy",  # jpg on different subreddit
        ]
        test_data = cls.instance.reddit.info(fullnames=cls.ids)
        cls.instance._transform_top_submissions(test_data)

    def test_multiple_subreddit_search(self):
        response = self.client.get("/reddit/search/", data={})
        # print(Subreddit.objects.all())
        # TODO:
