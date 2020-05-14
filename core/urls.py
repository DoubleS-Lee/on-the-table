from django.urls import path
from contents import views as content_views

#app_name은 config-urls.py의 namespace와 이름이 같아야한다
app_name = "core"
#장고에서 class based views는 view로 변환시켜주는 메소드(as_view())를 가지고 있다
urlpatterns = [path("", content_views.HomeView.as_view(), name="home")]