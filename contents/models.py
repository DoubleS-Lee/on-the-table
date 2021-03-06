from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models
from taggit.managers import TaggableManager


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    # Meta 클래스 모델 내의 모든 class들 안에 있는 class
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CookingUtensil(AbstractItem):

    """ CookingUtensil Model Definition """

    # 원래는 admin에서 클래스명에 항상 s를 붙여서 표현해주는데 이 밑에 Meta클래스에
    # verbose_name_plural를 써주면 항상 ""안에 있는 명칭으로 표시해준다
    # ordering은 정렬 방법을 적어주면 된다
    # 자세한건 장도 도큐먼트를 살펴보자
    class Meta:
        verbose_name_plural = "CookingUtensils"
        ordering = ["name"]


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    file = models.ImageField(upload_to="content_photos")
    # 파이썬은 코드를 수직으로 읽어서 원래 괄호안에 Content는 여기서 뒤에 나오기 때문에 ""없이 써주면 읽지 못한다
    # 따라서 ""를 추가해줬다
    content = models.ForeignKey("Content", related_name="photos", on_delete=models.CASCADE)


class Content(core_models.TimeStampedModel, models.Model):

    title = models.CharField(max_length=140)
    dish = models.CharField(max_length=140)
    description = models.TextField()
    cuisine = models.TextField()
    cooking_ingredients = models.TextField()
    # related_name을 설정하는 이유는 장고의 ORM 기능을 활용하기 위해서
    # related_name은 대상(contents)이 나(user)를 찾는 방식이다
    # user가 어떻게 우리(content)를 찾기 원하는지 설정하기 위해
    # foreingkey와 manytomany가 1과 2를 이어주는 방식이면
    # 이제 2에서 1을 찾기 위해서는 related_name으로 다시 연결해줘야된다는 것이다
    user = models.ForeignKey("users.User", related_name="contents", on_delete=models.CASCADE)
    cooking_utensils = models.ManyToManyField("CookingUtensil", related_name="contents", blank=True)
    tags = TaggableManager(blank=True)

    like_users = models.ManyToManyField("users.User", related_name="like_contents")

    # 장고 admin 페이지에 view on site라고 실제로 홈페이지 화면에서 어떻게 보이는지 볼 수 있는 버튼을 생성한다
    def get_absolute_url(self):
        return reverse("contents:detail", kwargs={"pk": self.pk})

    # str 형식으로 반환해줄 데이터를 정의해준다
    def __str__(self):
        return self.dish

    def first_photo(self):
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_photos(self):
        photos = self.photos.all()
        return photos