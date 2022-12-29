# https://docs.djangoproject.com/en/4.1/topics/forms/
from django import forms

# Enumerated choices
sort_choices = [(1, "relevence"), (2, "score"), (3, "new"), (4, "A-Z")]

class SearchForm(forms.Form):
    template_name = "search_form.html"
    q = forms.CharField(label="Search Term", max_length=300)
    # TODO: Migrate to forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=...)
    subreddit = forms.CharField(label="r/subreddit", max_length=21)
    author = forms.CharField(label="u/author", max_length=20)
    sort_by = forms.ChoiceField(choices=sort_choices)

    def make_results(self):
        pass
    

class IndexForm(SearchForm):
    q = forms.CharField(label="Search Term", max_length=300)

