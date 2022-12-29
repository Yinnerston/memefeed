from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import HeaderForm, SearchForm
from .models import Submission

def HeaderView(FormView):
    template_name = "reddit/header.html"
    form_class = HeaderForm
    success_url = 'search/results'

class IndexView(generic.ListView):
    """
    View for index page.
    """
    # TODO: Form with search query --> Pass filter in listview
    # Look at django filter by carlton gibsen
    # Add form validation
    # Q Object to do more complex filters
    template_name = "reddit/index.html"
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

    def get_context_data(self, **kwargs):
        """
        Extra arguments passed to template
        """
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        """
        Handles generation of results.
        """
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')
        subreddit = self.request.GET.get('subreddit')
        author = self.request.GET.get('author')

        return Submission.objects.filter(title__icontains=query)
