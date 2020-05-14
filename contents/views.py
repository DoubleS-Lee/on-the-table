from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models, forms

class HomeView(ListView):

    """ HomeView Definition """

    model = models.Content
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "contents_group"

class ContentDetail(DetailView):

    """ ContentDetail Definition """

    model = models.Content

"""위에 class ContentDetail(DetailView)와 같은 기능

from django.http import Http404
from django.shortcuts import render

def content_detail(request, pk):
    try:
        content = models.Content.objects.get(pk=pk)
        return render(request, "contents/detail.html", {"content":content})
    except models.Content.DoesNotExist:
        raise Http404()
"""


def search(request):
    form = forms.SearchForm()
    return render(request, "contents/search.html", {"form": form})