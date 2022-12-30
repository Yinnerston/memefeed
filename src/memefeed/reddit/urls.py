from django.urls import path

from .views import IndexView, SearchView, SearchResultsView, ParallelismView

app_name = "reddit"
urlpatterns = [
    path("parallelism", ParallelismView.as_view(), name="parallelism"),
    path('search/results', SearchResultsView.as_view(), name="search_results"),
    path('search/', SearchView.as_view(), name="compose_search"),
    path("", IndexView.as_view(), name="index"),
]
