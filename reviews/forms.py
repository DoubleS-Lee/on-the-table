'''
없어도 되는 코드
리뷰 폼 코드

from . import models
from django import forms

class ReviewForm(forms.ModelForm):
    #text = forms.TextInput(label = '댓글')

    class Meta:
        model = models.Review
        fields = ['review']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review'].label = "댓글"

'''