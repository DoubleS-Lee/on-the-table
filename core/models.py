from django.db import models
from . import managers

class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    #DateTimefield의 기능으로 auto_now_add는 생성된 날짜시간을 기록해주고
    #auto_now는 업데이트 될때마다의 날짜시간을 기록해준다
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    #여기서 abstract = True를 안해주면 데이터베이스에 이 정보들이 등록되므로 꼭 True를 해준다
    class Meta:
        abstract = True