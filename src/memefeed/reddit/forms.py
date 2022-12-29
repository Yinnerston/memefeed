# https://docs.djangoproject.com/en/4.1/topics/forms/
from django import forms

class IndexForm(forms.Form):
    q = forms.CharField(label="Index", max_length=50)

class SearchForm(forms.Form):
    q = forms.CharField(label="Search", max_length=50)