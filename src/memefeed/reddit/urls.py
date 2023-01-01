from django.urls import path

from .views import IndexView, SearchView, SearchResultsView, SubredditView
from django.conf import settings
from django.conf.urls.static import static

app_name = "reddit"
urlpatterns = [
    path('subreddit/<str:subreddit_name>', SubredditView.as_view(), name="subreddit_view"),
    path('search/results', SearchResultsView.as_view(), name="search_results"),
    path('search/', SearchView.as_view(), name="compose_search"),
    path("", IndexView.as_view(), name="index"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
