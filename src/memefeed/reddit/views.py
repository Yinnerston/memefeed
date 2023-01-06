from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from .forms import SearchForm
from .models import Submission, Subreddit

from datetime import datetime, timedelta

ITEMS_LEN = 20


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
    paginate_by = 3

    def get_queryset(self):
        """
        Returns the top submissions by score in descending order.
        Submissions are grouped into sub-lists of length = ITEMS_LEN
        """
        # Variable for how many submissions are displayed in a row in the index
        # TODO: Future sprint, implement video, galleries
        #  | Q(domain="v.redd.it")
        prev_day = datetime.today() - timedelta(days=1)
        top_submissions = (
            Submission.objects.filter(
                Q(domain__icontains="imgur.com") | Q(domain="i.redd.it")
            )
            .filter(
                Q(url__endswith=".jpg")
                | Q(url__endswith=".png")
                | Q(url__endswith=".gif")
            )
            .filter(created_utc__gte=prev_day)
            .order_by("-score", "title")
        )
        return [
            top_submissions[i : i + ITEMS_LEN]
            for i in range(0, len(top_submissions), ITEMS_LEN)
        ]


class SearchView(FormView):
    """
    View that composes the search/query.
    """

    template_name = "reddit/search_form.html"
    form_class = SearchForm
    success_url = "search/results"


class SearchResultsView(generic.ListView):
    """
    View that displays the results of a search
    """

    template_name = "reddit/results.html"
    context_object_name = "results_list"
    model = Submission
    paginate_by = 3

    def get_context_data(self, **kwargs):
        """
        Extra arguments passed to template
        """
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context

    def parse_subreddits_current_path(self):
        current_path = self.request.get_full_path()
        subreddits = [
            subreddit[10:]
            for subreddit in current_path.split("&")
            if subreddit.startswith("subreddit=")
        ]
        return subreddits

    def get_queryset(self):
        """
        Handles generation of results.
        """
        filtered_subreddits = self.parse_subreddits_current_path()
        title = self.request.GET.get("q")
        sort_by = self.request.GET.get("sort_by")
        order = SearchForm.get_order(int(sort_by))
        query = Submission.objects.filter(
            Q(domain="i.redd.it") | Q(domain="v.redd.it") | Q(domain="i.imgur.com")
        )
        if query:
            # Get specific title
            query = query.filter(title__icontains=title)
        author = self.request.GET.get("author")
        if author:
            # TODO: IS this validation good enought?
            query = query.filter(author=author)
        if filtered_subreddits:
            query = query.filter(subreddit__in=filtered_subreddits)
        # TODO:params in url are like: subreddit=0&subreddit=2&subreddit=4&subreddit=5&subreddit=6
        # And overwrite the preceding one. How to get these as a list?
        # TODO: Check out how form sends the request and see if i can overwrite it
        # Maybe look at init, applY(self, request) functions?
        result_submissions = query.order_by(order).all()
        return [
            result_submissions[i : i + ITEMS_LEN]
            for i in range(0, len(result_submissions), ITEMS_LEN)
        ]


class SubredditView(IndexView):
    template_name = "reddit/subreddit.html"
    context_object_name = "top_submissions_list"
    paginate_by = 3

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        _subreddit_name = kwargs.get("subreddit_name", None)
        try:
            self.subreddit = Subreddit.objects.get(name=_subreddit_name)
            self.subreddit_not_found = False
        except:
            self.subreddit = None
            self.subreddit_not_found = True

    def get_context_data(self, **kwargs):
        """
        Extra arguments passed to template
        """
        context = super(SubredditView, self).get_context_data(**kwargs)
        context["subreddit"] = self.subreddit
        context["subreddit_not_found"] = self.subreddit_not_found
        return context

    def get_queryset(self):
        """
        Returns the top submissions by score in descending order.
        Submissions are grouped into sub-lists of length = ITEMS_LEN
        """
        # Variable for how many submissions are displayed in a row in the index
        ITEMS_LEN = 20
        # TODO: Future sprint, implement video, galleries
        #  | Q(domain="v.redd.it")
        if not self.subreddit_not_found:
            subreddit_name = self.subreddit
            top_submissions = (
                Submission.objects.filter(subreddit=subreddit_name)
                .filter(Q(domain__icontains="imgur.com") | Q(domain="i.redd.it"))
                .order_by("-score", "title")
            )
            return [
                top_submissions[i : i + ITEMS_LEN]
                for i in range(0, len(top_submissions), ITEMS_LEN)
            ]
        else:
            return []
