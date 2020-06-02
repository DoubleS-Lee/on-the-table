from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404, render
from contents import models as content_models
from . import forms, models
from django.views.generic import FormView


class CreateReviewView(FormView):

    template_name = "contents/content_detail.html"
    form_class = forms.ReviewForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

'''
def create_review(request, content):
    post = get_object_or_404(content_models.Content, pk=content)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.users
            review.content = content
            review.save()
            return redirect(reverse("contents:detail", post.pk))
    
    else:
        form = forms.ReviewForm()
    return render(request, 'contents/content_detail.html', {'form':form},)
'''