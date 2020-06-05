from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404, render
from contents import models as content_models
from . import forms, models
from django.views.generic import FormView

def CreateReviewView(request, content, *args, **kwargs):
        if request.method == 'POST':
            comment = models.Review()
            comment.review = request.POST['review']
            comment.content = content_models.Content.objects.get(pk=content) # id로 객체 가져오기        
            comment.user = request.user
            comment.save()
            return redirect(reverse("contents:detail", kwargs={"pk": content}))
        else :
            return redirect('core:home')