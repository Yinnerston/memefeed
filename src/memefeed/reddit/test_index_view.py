"""
Test IndexView and index.html template
"""

from django.test import TestCase
from scripts.reddit_etl import RedditETL
# from reddit.forms import SearchForm
from reddit.models import Author, Subreddit, Submission
from http import HTTPStatus
import sentry_sdk

class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.instance = RedditETL()
        sentry_sdk.init(dsn="")

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

    def test_thumbnail_nsfw_ireddit_jpg_png(self):
        pass

    def test_thumbnail_nsfw_ireddit_gif(self):
        pass

    def test_thumbnail_nsfw_ireddit_gif(self):
        pass

    def test_thumbnail_nsfw_vreddit_video(self):
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

    def test_full_image_nsfw_ireddit_jpg_png(self):
        pass

    def test_full_image_nsfw_ireddit_gif(self):
        pass

    def test_full_image_nsfw_ireddit_gif(self):
        pass

    def test_full_image_nsfw_vreddit_video(self):
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
