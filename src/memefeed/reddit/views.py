from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from .forms import SearchForm
from .models import Submission, Subreddit

from datetime import date, datetime, timedelta

ITEMS_LEN = 20


class IndexView(generic.ListView):
    """
    View for index page.
    """

    template_name = "reddit/index.html"
    context_object_name = "top_submissions_list"
    paginate_by = 3

    def get_queryset(self):
        """
        Returns the top submissions by score in descending order.
        Top submissions are per week.
        The relevant 'day' for the recent top posts changes every day to make caching easier.
        Submissions are grouped into sub-lists of length = ITEMS_LEN
        """
        # Variable for how many submissions are displayed in a row in the index
        # TODO: Future sprint, implement video, galleries
        prev_week = datetime.today().replace(
            hour=23, minute=59, second=59
        ).astimezone() - timedelta(weeks=1)
        top_submissions = (
            Submission.objects.filter(
                Q(domain__icontains="imgur.com") | Q(domain="i.redd.it")
            )
            .filter(created_utc__gte=prev_week)
            .order_by("-score", "title")
        )
        return [
            top_submissions[i : i + ITEMS_LEN]
            for i in range(0, len(top_submissions), ITEMS_LEN)
        ]


class SearchView(FormView):
    """
    View that composes the search/query.
    Uses SearchForm from reddit/forms.py
    """

    template_name = "reddit/search_form.html"
    form_class = SearchForm
    success_url = "search/results"


class SearchResultsView(generic.ListView):
    """
    View that displays the results of a search.
    """

    template_name = "reddit/results.html"
    context_object_name = "results_list"
    model = Submission
    paginate_by = 3

    # TODO: Add form validation
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
        result_submissions = query.order_by(order).all()
        return [
            result_submissions[i : i + ITEMS_LEN]
            for i in range(0, len(result_submissions), ITEMS_LEN)
        ]


class SubredditView(IndexView):
    """
    Best posts all time on a subreddit.
    Same as search but just filter by subreddit
    """

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
