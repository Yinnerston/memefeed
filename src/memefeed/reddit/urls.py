from django.urls import path

from .views import IndexView, SearchView, SearchResultsView, SubredditView, AuthorView
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

app_name = "reddit"
urlpatterns = [
    path(
        "subreddit/<str:subreddit_name>", SubredditView.as_view(), name="subreddit_view"
    ),
    path("author/<str:author_name>", AuthorView.as_view(), name="author_view"),
    path("search/results", SearchResultsView.as_view(), name="search_results"),
    path("search/", SearchView.as_view(), name="compose_search"),
    path("", cache_page(60 * 30)(IndexView.as_view()), name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
