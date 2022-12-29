from django.shortcuts import render
from django.views import generic
from .models import Submission

# Create your views here.
class IndexView(generic.ListView):
    template_name = "reddit/index.html"
    context_object_name = "top_submissions_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Submission.objects.order_by("-score", "title")[:5]
