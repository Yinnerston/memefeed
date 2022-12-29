from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import IndexForm, SearchForm
from .models import Submission


class IndexView(generic.ListView):
    """
    View for index page.
    """
    # TODO: Form with search query --> Pass filter in listview
    # Look at django filter by carlton gibsen
    # Add form validation
    # Q Object to do more complex filters
    template_name = "reddit/index.html"
    form_class = IndexForm
    context_object_name = "top_submissions_list"        

    def get_queryset(self):
        """
        Return the last five published questions.
        """
        return Submission.objects.order_by("-score", "title")[:5]

class SearchView(FormView):
    """
    View that composes the search/query.
    """
    template_name = "reddit/search_form.html"
    form_class = SearchForm
    success_url = 'search/results'

class SearchResultsView(generic.ListView):
    """
    View that displays the results of a search
    """
    template_name = "reddit/results.html"
    context_object_name = "results_list"
    model = Submission
    # paginate_by = 50

    def get_queryset(self):
        """
        Handles generation of results.
        """
        query = self.request.GET.get('q')
        subreddit = self.request.GET.get('subreddit')
        author = self.request.GET.get('author')
        sort_by = self.request.GET.get('sort_by')
        return Submission.objects.filter(title__icontains=query)
