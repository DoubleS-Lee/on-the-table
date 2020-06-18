from django import forms
from . import models


class SearchForm(forms.Form):

    title = forms.CharField(required=False)
    dish = forms.CharField(required=False)
    cooking_utensils = forms.ModelMultipleChoiceField(queryset=models.CookingUtensil.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        content = models.Content.objects.get(pk=pk)

        photo.content = content
        photo.save()

class CreateContentForm(forms.ModelForm):
    class Meta:
        model = models.Content
        fields = (
            "title",
            "dish",
            "description",
            "cuisine",
            "cooking_ingredients",
            "cooking_utensils",
            "tags",
        )
        labels = {
            'title': ('제목'),
        }
        
    def save(self, *args, **kwargs):
        content = super().save(commit=False)
        return content

class CreateContentForm(forms.ModelForm):
    class Meta:
        model = models.Content
        fields = (
            "title",
            "dish",
            "description",
            "cuisine",
            "cooking_ingredients",
            "cooking_utensils",
            "tags",
        )
        labels = {
            'title': ('제목'),
        }

    def save(self, *args, **kwargs):
        content = super().save(commit=False)
        return content