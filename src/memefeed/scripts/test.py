"""
Test cases for reddit_etl.py script.
"""
from django.test import TestCase
from .reddit_etl import RedditETL
import httpretty

class RedditETLTest(TestCase):
    """
    Testing ETL process
    """

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def mock_reddit_top_posts(self):
        # TODO: Mock for each subreddit
        httpretty.register_uri(
            httpretty.GET,
            "https://", # reddit.json for top posts
            body='{...}'
        )

    def test_load_post_valid_post(self):
        pass

    def test_load_post_post_is_none(self):
        pass

    def test_load_post_duplicate_author(self):
        pass

    def test_load_post_duplicate_subreddit(self):
        pass

    def test_load_post_duplicate_submission(self):
        pass

    def test_load_post_EOM(self):
        pass

    def test_load_post_invalid_map_func(self):
        pass

    def test_transform_top_posts_valid_format(self):
        """
        Given a valid input from Reddit.top_posts, correctly
        """
        pass

    def test_reddit_etl_duplicate_run(self):
        pass

    def test_reddit_client_init(self):
        pass