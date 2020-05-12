from django.contrib import admin
from django.utils.html import mark_safe
from . import models

@admin.register(models.CookingUtensil)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "count_contents",)

    def count_contents(self, obj):
        return obj.contents.count()

#content에 연결된 photo를 볼수있게 하는 코드
#밑에 ContentAdmin 클래스에 inlines = (PhotoInline,)를 추가해야한다
class PhotoInline(admin.TabularInline):

    model = models.Photo
    extra = 1

@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):

    """ Content Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("title", "description")},
        ),
        ("Dish Info", {"fields": ("dish", )}),
        ("How to Cook", {'classes': ('collapse',), "fields": ("cooking_ingredients", "cuisine", "cooking_utensils", )}),
        ("Last Details", {"fields": ("user",)}),
    )
    
    list_display = (
        "title",
        "dish",
        "description",
        "cuisine",
        "cooking_ingredients",
        "user",
        "count_cooking_utensils",
        "count_photos",

    )

    list_filter = (
        "dish",
        #ForgeignKey의 속성을 이용해서 user내의 다른 정보들을 가져오고 싶을때 __를 사용한다
        "user__gender",
        "cooking_utensils",
        
    )

    #admin 패널안의 user가 너무 많아지면 선택하기 힘드니까 검색할수있는 장치를 만드는 것
    raw_id_fields = ("user",)

    search_fields = [
        "title",
        "dish",
        "cooking_ingredients",
        "description",
        #ForgeignKey의 속성을 이용해서 user내의 다른 정보들을 가져오고 싶을때 __를 사용한다
        "user__gender",

    ]

    #Many to Many 타입을 검색하고 싶은 경우 사용
    filter_horizontal = ("cooking_utensils",)

    #특정 컬럼을 순서대로 정렬하고 싶을때 사용
    ordering =(
        "title",
        "dish",
        )

    #list_display에서 ManytoMany타입의 정보를 개수의 형태로 나타내고 싶을때 함수를 사용해서 나타낸다
    #여기서 self는 ContentAdmin class를 나타내고, obj는 admin 패널에서 해당 row를 말한다 즉 여기서는 한개의 content를 말한다
    def count_cooking_utensils(self, obj):
        return obj.cooking_utensils.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"    

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"