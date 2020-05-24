import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db import models
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


#abstract는 코드내에서만 잠깐쓰이고 데이터베이스에 저장되지는 않는다
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "남자"
    GENDER_FEMALE = "여자"
    GENDER_OTHER = "기타"

    GENDER_CHOICES = (
        (GENDER_MALE, "남자"),
        (GENDER_FEMALE, "여자"),
        (GENDER_OTHER, "기타"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN,"한국어"))
    
    nickname = models.CharField(max_length=80)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate= models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    nationality = CountryField(blank=True)
    
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def __str__(self):
        return self.nickname