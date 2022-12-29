from django.urls import path
from .views import SearchResultsView

from . import views

app_name = "reddit"
urlpatterns = [
    path('search/', SearchResultsView.as_view(), name="search_results"),
    path("", views.IndexView.as_view(), name="index"),
]
