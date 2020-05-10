from django.db import models
from core import models as core_models

class Wishlist(core_models.TimeStampedModel):

    """ Wishlist Model Definition """

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    contents = models.ManyToManyField("contents.Content", blank=True)

    def __str__(self):
        return self.name

    def count_contents(self):
        return self.contents.count()

    #admin 패널에서 열의 제목을 바꾸고 싶을때
    count_contents.short_description = "Number of Contents"