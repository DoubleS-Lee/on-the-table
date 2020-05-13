from django.shortcuts import render
from . import models

def all_contents(request):
    all_contents = models.Content.objects.all()
    return render(request, "contents/home.html", context={"potato": all_contents})
