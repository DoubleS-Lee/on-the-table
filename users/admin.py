from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

#@를 Decorator라고 부른다
#admin 패널에서 이 user를 보고싶다 라는 뜻임
#그리고 user를 컨트롤한 클래스가 바로 CustomUserAdmin이 될것이다라는 뜻
#model.py의 User 클래스를 상속받는다
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    
    """ Custom User Admin """

    #장고 admin 화면에 fieldset(파란색바)을 하나 만들어준다
    #내가 새로 정의한 정보들을 모아놓았음
    #UserAdmin.fieldsets을 더해줘야 장고에서 기본으로 제공하는 정보들이 살아있다
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "nickname",
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "nationality",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("nationality",)

    list_display = (
        "nickname",
        "gender",
        "language",
        "nationality",
    )