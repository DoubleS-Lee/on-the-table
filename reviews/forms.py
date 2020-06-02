from django import forms
from contents import models as c_models
from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ("review",)
        widgets = {
            "review": forms.TextInput(attrs={"placeholder": "댓글작성"}),
        }

    def save(self):
        review = super().save(commit=False)
        return review