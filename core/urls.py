from django.urls import path
from contents import views as content_views

#app_name은 config-urls.py의 namespace와 이름이 같아야한다
app_name = "core"

urlpatterns = [path("", content_views.all_contents, name="home")]