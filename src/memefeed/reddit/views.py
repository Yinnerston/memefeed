from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import SearchForm
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
    context_object_name = "top_submissions_list"

    def get_queryset(self):
        """
        Return the last five published questions.
        """
        return Submission.objects.order_by("-score", "title")[:5]

class ParallelismView(generic.TemplateView):
    template_name = "reddit/index-parallelism.html"


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
        order = SearchForm.get_order(sort_by)
        query = Submission.objects

        author = self.request.GET.get('author')
        if author is not None or author != '':
            # TODO: IS this validation good enought?
            query = query.filter(author=author)
        subreddit = self.request.GET.get('subreddit')
        # TODO:params in url are like: subreddit=0&subreddit=2&subreddit=4&subreddit=5&subreddit=6
        # And overwrite the preceding one. How to get these as a list?
            # TODO: Check out how form sends the request and see if i can overwrite it
            # Maybe look at init, applY(self, request) functions?
        return Submission.objects.filter(author=author, subreddit=subreddit, title__icontains=query).order_by(order)
