from django import forms
from . import models


class SearchForm(forms.Form):

    title = forms.CharField(required=False)
    dish = forms.CharField(required=False)
    cooking_utensils = forms.ModelMultipleChoiceField(queryset=models.CookingUtensil.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)