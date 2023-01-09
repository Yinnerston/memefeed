# https://docs.djangoproject.com/en/4.1/topics/forms/
from django import forms
from .models import Subreddit


class SearchForm(forms.Form):
    # Enumerated choices in the form of (sort_value, human_readable_value)
    sort_choices = [(0, "relevance"), (1, "score"), (2, "new"), (3, "A-Z")]
    # TODO: Implement relevance
    sort_choices_order_by = ["-score", "-score", "created_utc", "title"]
    subreddit_choices = [
        (subreddit, subreddit) for subreddit in Subreddit.objects.all()
    ]

    # Fields in the form
    template_name = "search_form.html"
    q = forms.CharField(label="Search Term", max_length=300, required=False)
    subreddit = forms.MultipleChoiceField(
        label="r/subreddit",
        widget=forms.CheckboxSelectMultiple,
        choices=subreddit_choices,
        required=False,
    )
    author = forms.CharField(label="u/author", max_length=20, required=False)
    sort_by = forms.ChoiceField(choices=sort_choices, initial="relevance")

    @staticmethod
    def get_order(sort_value: int):
        try:
            return SearchForm.sort_choices_order_by[int(sort_value)]
        except Exception:
            return SearchForm.sort_choices_order_by[0]
