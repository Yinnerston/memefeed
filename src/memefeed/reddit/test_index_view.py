"""
Test IndexView and index.html template
"""

from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from scripts.reddit_etl import RedditETL

# from reddit.forms import SearchForm
from reddit.models import Author, Subreddit, Submission
from http import HTTPStatus
import sentry_sdk
import urllib


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup etl for whole class
        cls.instance = RedditETL(testing=True)
        sentry_sdk.init(dsn="")
        # Set up data for the whole TestCase
        # cls.ids = [
        #     "t3_zzye6e",    # jpg nsfw
        #     "t3_zzyds7",    # gif
        #     "t3_zzydk5",    # png
        #     "t3_zzycfr",    # Jpg
        #     "t3_zzyetg",    # Gallery
        #     "t3_100f2k6",   # Imgur
        # ]
        # test_data = cls.instance.reddit.info(fullnames=cls.ids)
        # cls.instance._transform_top_submissions(test_data)

    def load_submission(self, id):
        """
        Load a single submission id=id into test database.
        Wrapper for RedditETL._load_submission(id)
        """
        submission = IndexViewTest.instance.reddit.submission(id)
        self.assertIsNotNone(submission)
        return IndexViewTest.instance._load_submission(submission)

    # Tests for image thumbnail
    def test_thumbnail_ireddit_jpg(self):
        """
        Test thumbnail correctly takes jpg data from reddit
        """
        jpg_submission = self.load_submission("zzycfr")
        # Check that jpg is loaded correctly
        response = self.client.get("/reddit/", data={})
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(response.context["top_submissions_list"], [])
        index_jpg_submission = response.context["top_submissions_list"][0][0]
        self.assertEquals(jpg_submission, index_jpg_submission)
        # Check that the url can be opened
        self.assertEquals(
            urllib.request.urlopen(index_jpg_submission.url).getcode(), HTTPStatus.OK
        )
        # Check that that the jpg has been rendered
        self.assertContains(response, jpg_submission.title)

    def test_thumbnaill_ireddit_png(self):
        """
        Test thumbnail correctly takes png data from reddit.
        """
        png_submission = self.load_submission("zzydk5")
        # Check that jpg is loaded correctly
        response = self.client.get("/reddit/", data={})
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(response.context["top_submissions_list"], [])
        index_png_submission = response.context["top_submissions_list"][0][0]
        self.assertEquals(png_submission, index_png_submission)
        # Check that the url can be opened
        self.assertEquals(
            urllib.request.urlopen(index_png_submission.url).getcode(), HTTPStatus.OK
        )
        # Check that that the png has been rendered
        self.assertContains(response, png_submission.title)

    def test_thumbnail_ireddit_gif(self):
        """
        Test thumbnail correctly takes gif data from reddit.
        """
        gif_submission = self.load_submission("zzyds7")
        self.assertNotEquals(Submission.objects.count(), 0)
        # Check that jpg is loaded correctly
        response = self.client.get("/reddit/", data={})
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(response.context["top_submissions_list"], [])
        index_gif_submission = response.context["top_submissions_list"][0][0]
        self.assertEquals(gif_submission, index_gif_submission)
        # Check that the url can be opened
        self.assertEquals(
            urllib.request.urlopen(index_gif_submission.url).getcode(), HTTPStatus.OK
        )
        # Check that that the png has been rendered
        self.assertContains(response, gif_submission.title)

    def test_thumbnail_ireddit_selftext(self):
        pass

    # TODO: Different video formats (?)
    def test_thumbnail_vreddit_video(self):
        pass

    def test_thumbnail_reddit_gallery(self):
        # TODO: Write test for full image after implementation
        pass

    def test_thumbnail_imgur(self):
        """
        Test thumbnail correctly takes image data from imgur.
        """
        imgur_submission = self.load_submission("100f2k6")
        self.assertEqual(Submission.objects.count(), 1)
        # Check that jpg is loaded correctly
        response = self.client.get("/reddit/", data={})
        self.assertEquals(response.status_code, HTTPStatus.OK)

        self.assertNotContains(response, "No submissions found")
        self.assertNotEqual(response.context["top_submissions_list"], [])
        index_imgur_submission = response.context["top_submissions_list"][0][0]
        self.assertEquals(imgur_submission, index_imgur_submission)
        # Check that the url can be opened
        self.assertEquals(
            urllib.request.urlopen(index_imgur_submission.url).getcode(), HTTPStatus.OK
        )
        # Check that that the png has been rendered
        self.assertContains(response, imgur_submission.title)

    def test_thumbnail_misc(self):
        # TODO: Write test for full image after implementation
        pass

    def test_thumbnail_crosspost(self):
        # TODO: Future Sprint
        pass

    # Covers nsfw data for thumbnails
    def test_thumbnail_nsfw_ireddit_jpg_png(self):
        """
        Test thumbnail correctly takes image data from nsfw reddit post.
        """
        nsfw_submission = self.load_submission("zzye6e")
        # Check that jpg is loaded correctly
        response = self.client.get("/reddit/", data={})
        self.assertEquals(response.status_code, HTTPStatus.OK)
        index_nsfw_submission = response.context["top_submissions_list"][0][0]
        self.assertEquals(nsfw_submission, index_nsfw_submission)
        # Check that the url can be opened
        self.assertEquals(
            urllib.request.urlopen(index_nsfw_submission.url).getcode(), HTTPStatus.OK
        )
        # Check that that the png has been rendered
        self.assertContains(response, nsfw_submission.title)

    def test_thumbnail_span_ratio_jpg_png(self):
        # TODO: Future Sprint
        pass

    def test_thumbnail_span_ratio_video(self):
        # TODO: Future Sprint
        pass


def IndexViewSeleniumTest(LiveServerTestCase):
    """
    Selenium test case to simulate user actions like clicks and accessing next page.
    """
    # Tests for full image
    def test_full_image_ireddit_jpg_png(self):
        jpg_submission = self.load_submission("zzycfr")
        png_submission = self.load_submission("zzydk5")
        # Get full screen of
        response = self.client.get("/reddit/", data={})

    def test_full_image_ireddit_gif(self):
        jpg_submission = self.load_submission("zzyds7")

    def test_full_image_vreddit_video(self):
        # TODO: Future Sprint
        pass

    def test_full_image_vreddit_video(self):
        # TODO: Future Sprint
        pass

    def test_full_image_imgur(self):
        pass

    # Covers nsfw data for full image
    def test_full_image_nsfw_ireddit_jpg_png(self):
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
