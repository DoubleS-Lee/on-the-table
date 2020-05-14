
from django import forms
from . import models


class SearchForm(forms.Form):

    title = forms.CharField(initial="Anywhere")
    cooking_utensils = forms.ModelChoiceField(queryset=models.CookingUtensil.objects.all())