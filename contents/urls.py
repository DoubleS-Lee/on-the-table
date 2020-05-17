from django.urls import path
from . import views

app_name = "contents"

urlpatterns = [path("<int:pk>", views.ContentDetail.as_view(), name="detail"), path("search/", views.SearchView.as_view(), name="search")]