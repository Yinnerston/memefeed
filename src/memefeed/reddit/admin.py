from django.contrib import admin
from .models import Author, Subreddit, Submission
# Register your models here.
admin.site.register(Author)
admin.site.register(Subreddit)
admin.site.register(Submission)