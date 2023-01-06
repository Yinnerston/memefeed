from django.db import models
from math import floor
from django_prometheus.models import ExportModelOperationsMixin


class Author(ExportModelOperationsMixin("author"), models.Model):
    """
    Author of a submission.
    """

    name = models.CharField(primary_key=True, max_length=20)
    favourite = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Subreddit(ExportModelOperationsMixin("subreddit"), models.Model):
    """
    Subreddit.
    """

    name = models.CharField(primary_key=True, max_length=21)
    favourite = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Submission(ExportModelOperationsMixin("submission"), models.Model):
    """
    Submission made on a subreddit by an Author.
    """

    id = models.CharField("Reddit post's ID", max_length=10, primary_key=True)
    title = models.CharField("Title of a Reddit post", max_length=300)
    score = models.IntegerField("Upvotes")
    url = models.URLField("Submission URL")
    domain = models.CharField("Domain", max_length=50)
    created_utc = models.DateTimeField("Date the submission was created")
    # Submission Content / Media
    # TODO: Normalize media
    is_self = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    media_only = models.BooleanField(default=False)
    media = models.JSONField(default=dict, blank=True)
    media_embed = models.JSONField(default=dict)
    selftext = models.TextField(max_length=40000, default=str)
    selftext_html = models.TextField(default=str)  # TODO: Should this be binary?
    nsfw = models.BooleanField(default=False)
    thumbnail = models.URLField("Thumbnail URL")
    secure_media = models.JSONField(default=dict)
    secure_media_embed = models.JSONField(default=dict)
    # Foreign Keys
    subreddit = models.ForeignKey(Subreddit, models.CASCADE)
    author = models.ForeignKey(Author, models.CASCADE)


# TODO: Future sprint: Implement image server
class SubmissionFullImage(models.Model):
    """
    Full image relating to a submission.
    """

    submission = models.ForeignKey(Submission, models.CASCADE)
    image = models.ImageField(upload_to="submissions/full")
    image_ext = models.CharField("Image Extension E.G. jpg, png, gif", max_length=10)


# TODO: https://docs.djangoproject.com/en/4.1/topics/db/optimization/
# E.G. Cache queryset as a view

# TODO: Future sprint: Implement image server
class SubmissionThumbnailImage(models.Model):
    """
    Thumbnail image relating to a submission.
    """

    submission = models.ForeignKey(Submission, models.CASCADE)
    image = models.ImageField(upload_to="submissions/thumbs")
    image_ext = models.CharField("Image Extension E.G. jpg, png, gif", max_length=10)

    @property
    def span(self):
        """
        Get the most closely matching span of an image thumbnail for display in article.
        Based on image width:height ratio
        The span is a number between 1 and 3
        """
        span = floor(self.image.width / self.image.height)
        return max(min(span, 3), 1)
