from django.urls import path

from .views import IndexView, SearchView, SearchResultsView

app_name = "reddit"
urlpatterns = [
    path('search/results', SearchResultsView.as_view(), name="search_results"),
    path('search/', SearchView.as_view(), name="compose_search"),
    path("", IndexView.as_view(), name="index"),
]
