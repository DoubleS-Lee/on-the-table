from django.urls import path
from . import views

app_name = "contents"

urlpatterns = [
    path("create/", views.CreateContentView, name="create"),
    path("<int:pk>/", views.ContentDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<int:pk>/photos/", views.ContentPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:content_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:content_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("<int:pk>/edit/", views.EditContentView.as_view(), name="edit"),
    path("tag/", views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
]