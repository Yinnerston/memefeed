from django.contrib import admin
from .models import Author, Subreddit, Submission

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'favourite')
    search_fields = ['name', 'favourite']

@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ('name', 'favourite')
    search_fields = ['name', 'favourite']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subreddit', 'author', 'score', 'url')
    search_fields = ['title', 'subreddit__name', 'author__name']

