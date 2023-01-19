"""
Test IndexView and index.html template
"""

from django.core.cache import cache
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from scripts.reddit_etl import RedditETL

# from reddit.forms import SearchForm
from reddit.models import Author, Subreddit, Submission
from http import HTTPStatus
import sentry_sdk
import urllib
from datetime import datetime, timedelta
from pytz import timezone


class IndexViewTest(TestCase):
    """
    # TODO: These tests test that the html is rendered.
    THEY DO NOT test if images are displayed correctly i.e. check for onerror in html elements.
    """

    tz = timezone("Australia/Sydney")
    curTime = datetime.now().astimezone(tz) - timedelta(minutes=10)

    def setCurTimeRecent(self, submission_obj: Submission):
        """
        Set the created_utc attribute of a submission to the 10 minutes before test init.
        """
        submission_obj.created_utc = IndexViewTest.curTime
        submission_obj.save()

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

    def tearDown(self):
        super().tearDown()
        cache.clear()

    def load_submission(self, id):
        """
        Load a single submission id=id into test database.
        Wrapper for RedditETL._load_submission(id)
        """
        submission = IndexViewTest.instance.reddit.submission(id)
        self.assertIsNotNone(submission)
        loaded_submission = IndexViewTest.instance._load_submission(submission)
        self.setCurTimeRecent(loaded_submission)
        return loaded_submission

    # Tests for image thumbnail
    def test_thumbnail_ireddit_jpg(self):
        """
        Test thumbnail correctly takes jpg data from reddit
        """
        jpg_submission = self.load_submission("zzycfr")
        # Check that jpg is loaded correctly
        response = self.client.get("", data={})
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
        response = self.client.get("", data={})
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
        response = self.client.get("", data={})
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
        response = self.client.get("", data={})
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

    def test_thumbnail_imgur_video(self):
        """
        Test imgur video link.
        """
        imgur_submission = self.load_submission("1016e0z")
        self.assertEqual(Submission.objects.count(), 1)
        # Check that video is loaded correctly
        response = self.client.get("", data={})
        self.assertEquals(response.status_code, HTTPStatus.OK)

        self.assertNotContains(response, "No submissions found")
        self.assertNotEqual(response.context["top_submissions_list"], [])
        index_imgur_submission = response.context["top_submissions_list"][0][0]
        self.assertEquals(imgur_submission, index_imgur_submission)
        # Check that the url can be opened
        self.assertEquals(
            urllib.request.urlopen(index_imgur_submission.url).getcode(), HTTPStatus.OK
        )
        # Check that that the video has been rendered
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
        response = self.client.get("", data={})
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


# class IndexViewSeleniumTest(LiveServerTestCase):
#     """
#     Selenium test case to simulate user actions like clicks and accessing next page.
#     """

#     @classmethod
#     def setUpTestData(cls):
#         """
#         First setup reddit data with by running:
#          src\memefeed\scripts\post_reddit_pagination_test_submissions.py
#         """
#         # Setup etl for whole class
#         cls.instance = RedditETL(testing=True)
#         sentry_sdk.init(dsn="")
#         # Set up data for the whole TestCase
#         cls.ids = [
#             "t3_107fh18",
#             "t3_107fh1j",
#             "t3_107fh1v",
#             "t3_107fh26",
#             "t3_107fh2n",
#             "t3_107fh2y",
#             "t3_107fh3g",
#             "t3_107fh3q",
#             "t3_107fh3z",
#             "t3_107fh46",
#             "t3_107fh4c",
#             "t3_107fh4k",
#             "t3_107fh58",
#             "t3_107fh5g",
#             "t3_107fh5q",
#             "t3_107fh5y",
#             "t3_107fh68",
#             "t3_107fh6b",
#             "t3_107fh6i",
#             "t3_107fh6r",
#             "t3_107fh72",
#             "t3_107fh7c",
#             "t3_107fh7q",
#             "t3_107fh83",
#             "t3_107fh8s",
#             "t3_107fh94",
#             "t3_107fh9j",
#             "t3_107fha0",
#             "t3_107fhac",
#             "t3_107fhaq",
#             "t3_107fhb3",
#             "t3_107fhbd",
#             "t3_107fhbm",
#             "t3_107fhbv",
#             "t3_107fhc3",
#             "t3_107fhce",
#             "t3_107fhcq",
#             "t3_107fhd3",
#             "t3_107fhdd",
#             "t3_107fhdp",
#         ]

#         test_data = cls.instance.reddit.info(fullnames=cls.ids)
#         cls.instance._transform_top_submissions(test_data)

#     # Tests for full image
#     def test_full_image_ireddit_jpg_png(self):
#         jpg_submission = self.load_submission("zzycfr")
#         png_submission = self.load_submission("zzydk5")
#         # Get full screen of
#         response = self.client.get("", data={})

#     def test_full_image_ireddit_gif(self):
#         jpg_submission = self.load_submission("zzyds7")

#     def test_full_image_vreddit_video(self):
#         # TODO: Future Sprint
#         pass

#     def test_full_image_vreddit_video(self):
#         # TODO: Future Sprint
#         pass

#     def test_full_image_imgur(self):
#         pass

#     # Covers nsfw data for full image
#     def test_full_image_nsfw_ireddit_jpg_png(self):
#         pass

#     # Tests for pagination
#     def test_pagination_submission_count(self):
#         """
#         Test the default number of records per page.
#         """
#         pass

#     def test_pagination_next_prev_button(self):
#         """
#         Test the pagination nnext & prev button is correctly displayed and working.
#         """
#         pass

#     def test_pagination_correct_num_pages(self):
#         """
#         Test the pagination displays the correct number of pages.
#         """
#         pass
