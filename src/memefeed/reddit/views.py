from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect

from .forms import IndexForm
from .models import Submission

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IndexForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IndexForm()

    return render(request, 'name.html', {'form': form})


class IndexView(generic.ListView):
    # TODO: Form with search query --> Pass filter in listview
    # Look at django filter by carlton gibsen
    # Add form validation
    # Q Object to do more complex filters
    template_name = "reddit/index.html"
    context_object_name = "top_submissions_list"        

    def get_queryset(self):
        """Return the last five published questions."""
        return Submission.objects.order_by("-score", "title")[:5]

class SearchResultsView(generic.ListView):
    template_name = "reddit/search.html"

    def get_queryset(self):
        return Submission.objects.filter()
