from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField(blank=True, null=True)
    user = models.ForeignKey("users.User", related_name="reviews", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.ForeignKey("contents.Content", related_name="reviews", on_delete=models.CASCADE)

    #.을 사용하여 ForeignKey로 연결된 정보들을 타고 들어가서 admin 패널에 나타나게 할수있다
    def __str__(self):
        return f"{self.content.dish} - {self.content.user.nickname} - {self.review}"
    
    class Meta:
        ordering = ("-created",)
