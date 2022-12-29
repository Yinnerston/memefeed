# https://docs.djangoproject.com/en/4.1/topics/forms/
from django import forms
from .models import Subreddit

class SearchForm(forms.Form):
    # Enumerated choices
    sort_choices = [(0, "relevance"), (1, "score"), (2, "new"), (3, "A-Z")]
    subreddit_choices = zip(range(Subreddit.objects.count()), Subreddit.objects.all())

    # Fields in the form
    template_name = "search_form.html"
    q = forms.CharField(label="Search Term", max_length=300)
    subreddit = forms.MultipleChoiceField(label="r/subreddit", widget=forms.CheckboxSelectMultiple, choices=subreddit_choices, required=False)
    author = forms.CharField(label="u/author", max_length=20, required=False)
    sort_by = forms.ChoiceField(choices=sort_choices, initial="relevance")

    def make_results(self):
        pass
    

class HeaderForm(SearchForm):
    """
    Search bar in homepage
    """
    template_name = "header.html"
