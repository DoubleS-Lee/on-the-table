from django.urls import path
from . import views


app_name = "reviews"

urlpatterns = [
    path("<int:content>/reviews/", views.CreateReviewView, name="create_review"),
    path(
        "<int:content_pk>/reviews/<int:review_pk>/delete/",
        views.delete_review,
        name="delete-review",
    ),
]