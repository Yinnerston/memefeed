from django.db import models

class Author(models.Model):
    """
    Author of a submission.
    """
    name = models.CharField(primary_key=True, max_length=20)
    favourite = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name

class Subreddit(models.Model):
    """
    Subreddit.
    """
    name = models.CharField(primary_key=True, max_length=21)
    favourite = models.BooleanField(default=False)

class Submission(models.Model):
    """
    Submission made on a subreddit by an Author.
    """
    id = models.CharField("Reddit post's ID", max_length=6, primary_key=True)
    title = models.CharField("Title of a Reddit post", max_length=300)
    score = models.IntegerField("Number of upvotes on a reddit post")
    url = models.URLField("Submission URL")
    domain = models.CharField("Domain", max_length=50)
    created_utc = models.DateTimeField("Date the submission was created")
    # Submission Content / Media
    # TODO: Normalize media
    is_self = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    media_only = models.BooleanField(default=False)
    media = models.JSONField(default=list, blank=True)
    media_embed = models.JSONField(default=list)
    selftext = models.TextField(max_length=40000)
    selftext_html = models.TextField()  # TODO: Should this be binary?
    nsfw = models.BooleanField(default=False)
    thumbnail = models.URLField("Thumbnail URL")
    secure_media = models.JSONField(default=list)
    secure_media_embed = models.JSONField(default=list)
    # Foreign Keys
    subreddit = models.ForeignKey(Subreddit, models.CASCADE)
    author = models.ForeignKey(Author, models.CASCADE)



