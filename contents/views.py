from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView, TemplateView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms
from reviews import forms as review_forms
from django.forms import modelformset_factory


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Content
    paginate_by = 12
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
                
                paginator = Paginator(qs, 12, orphans=5)

                page = request.GET.get("page", 1)

                contents = paginator.get_page(page)

                get_copy = request.GET.copy()

                parameters = get_copy.pop('page', True) and get_copy.urlencode()

                return render(request, "contents/search.html", {"form": form, "contents": contents, "parameters": parameters})

        else:
            form = forms.SearchForm()
        return render(request, "contents/search.html", {"form": form})


class EditContentView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Content
    template_name = "contents/content_edit.html"
    fields = (
        "title",
        "dish",
        "description",
        "cuisine",
        "cooking_ingredients",
        "cooking_utensils",
        "tags",
    )

    def get_object(self, queryset=None):
        content = super().get_object(queryset=queryset)
        if content.user.pk != self.request.user.pk:
            raise Http404()
        return content


class ContentPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Content
    template_name = "contents/content_photos.html"

    def get_object(self, queryset=None):
        content = super().get_object(queryset=queryset)
        if content.user.pk != self.request.user.pk:
            raise Http404()
        return content

@login_required
def delete_photo(request, content_pk, photo_pk):
    user = request.user
    try:
        content = models.Content.objects.get(pk=content_pk)
        if content.user.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("contents:photos", kwargs={"pk": content_pk}))
    except models.Content.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "contents/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("file")

    def get_success_url(self):
        content_pk = self.kwargs.get("content_pk")
        return reverse("contents:photos", kwargs={"pk": content_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "contents/photo_create.html"
    fields = ("file")
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("contents:photos", kwargs={"pk": pk}))


# class CreateContentView(user_mixins.LoggedInOnlyView, FormView):

#     form_class = forms.CreateContentForm
#     template_name = "contents/content_create.html"

#     def form_valid(self, form):
#         content = form.save()
#         content.user = self.request.user
#         content.save()
#         #MtoM 데이터를 저장하게 해주는 코드
#         form.save_m2m()
#         messages.success(self.request, "Content Uploaded")
#         return redirect(reverse("contents:detail", kwargs={"pk": content.pk}))




@login_required
def CreateContentView(request):
    # modelformset_factory 함수 사용(extra로 최대 업로드할 수 있는 이미지 개수 설정)
    CreatePhotoFormSet = modelformset_factory(models.Photo, form=forms.CreatePhotoForm, min_num=1)

    if request.method == "POST":
        content_form = forms.CreateContentForm(request.POST, request.FILES)
        formset = CreatePhotoFormSet(request.POST, request.FILES, queryset=models.Photo.objects.none())
        #print(formset)
        # form validation
        if content_form.is_valid() and formset.is_valid():
            content_form = content_form.save(commit=False)
            content_form.user = request.user
            content_form.save()
            for form in formset.cleaned_data:
                # 유저가 모든 이미지들을 업로드하지 않았을 경우 crash 방지
                if form:
                    image = form['file']
                    photo = models.Photo(content=content_form, file=image)
                    photo.save()
            return redirect(reverse("core:home"))
        #else:
            #print(content_form.errors, formset.errors)
    else:
        # method가 POST가 아닌 경우
        content_form = forms.CreateContentForm()
        formset = CreatePhotoFormSet(queryset=models.Photo.objects.none())


    return render(request, 'contents/content_create.html', {'content_form':content_form, 'formset':formset})

@login_required
def delete_content(request, content_pk):
    user = request.user
    try:
        content = models.Content.objects.get(pk=content_pk)
        if content.user.pk != user.pk:
            messages.error(request, "Cant delete that content")
        else:
            models.Content.objects.filter(pk=content_pk).delete()
            messages.success(request, "Content Deleted")
        return redirect(reverse("core:home"))
    except models.Content.DoesNotExist:
        return redirect(reverse("core:home"))


class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_content_list.html'
    model = models.Content

    def get_queryset(self):
        return models.Content.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

