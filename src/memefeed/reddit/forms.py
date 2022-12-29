# https://docs.djangoproject.com/en/4.1/topics/forms/
from django import forms
from .models import Subreddit

class SearchForm(forms.Form):
    # Enumerated choices
    sort_choices = [(0, "relevence"), (1, "score"), (2, "new"), (3, "A-Z")]
    subreddit_choices = zip(range(Subreddit.objects.count()), Subreddit.objects.all())

    # Fields in the form
    template_name = "search_form.html"
    q = forms.CharField(label="Search Term", max_length=300)
    subreddit = forms.MultipleChoiceField(label="r/subreddit", widget=forms.CheckboxSelectMultiple, choices=subreddit_choices)
    author = forms.CharField(label="u/author", max_length=20)
    sort_by = forms.ChoiceField(choices=sort_choices)

    def make_results(self):
        pass
    

class IndexForm(SearchForm):
    q = forms.CharField(label="Search Term", max_length=300)

