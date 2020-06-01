
from django.urls import path
from . import views

app_name = "wishlists"

urlpatterns = [
    path("toggle/<int:content_pk>", views.toggle_content, name="toggle-content"),
    path("favs/", views.SeeFavsView.as_view(), name="see-favs"),
]