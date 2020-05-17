from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
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

"""위에 class ContentDetail(DetailView)와 같은 기능을 하는 메소드

from django.http import Http404
from django.shortcuts import render

def content_detail(request, pk):
    try:
        content = models.Content.objects.get(pk=pk)
        return render(request, "contents/detail.html", {"content":content})
    except models.Content.DoesNotExist:
        raise Http404()
"""

class SearchView(View):

    """ SearchView Definition """

    model = models.Content

    def get(self, request):

        title = request.GET.get("title")
        dish = request.GET.get("dish")
        cooking_utensils = request.GET.get("cooking_utensils")

        search_word = {title, dish, cooking_utensils}

        if search_word:
        
            #내가 검색조건을 입력하고 검색 버튼을 눌렀을때
            #이미 입력했던 조건들이 사라지지 않게 하는 코드
            form = forms.SearchForm(request.GET)

            if form.is_valid():

                title = form.cleaned_data.get("title")
                dish = form.cleaned_data.get("dish")
                cooking_utensils = form.cleaned_data.get("cooking_utensils")
                
                filter_args = {}
                #filter_args에서 contains를 쓸건지 exact를 쓸건지 아니면 다른걸 쓸건지는
                #https://docs.djangoproject.com/en/3.0/ref/models/querysets/ 에서 Field lookups에 가서 찾아보도록 한다
                if title is not None:
                    filter_args["title__icontains"] = title

                if dish is not None:
                    filter_args["dish__icontains"] = dish

                qs = models.Content.objects.filter(**filter_args).order_by("-created")
                
                filter_arg = {}
                if cooking_utensils is not None:
                    for cooking_utensil in cooking_utensils:
                        filter_arg["cooking_utensils"] = cooking_utensil
                        qs = qs.filter(**filter_arg).order_by("-created")
                else:
                    pass
                
                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                contents = paginator.get_page(page)

                get_copy = request.GET.copy()

                parameters = get_copy.pop('page', True) and get_copy.urlencode()

                return render(request, "contents/search.html", {"form": form, "contents": contents, "parameters":parameters})

        else:
            form = forms.SearchForm()
        return render(request, "contents/search.html", {"form": form})