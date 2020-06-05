from django.urls import path
from . import views


app_name = "reviews"

urlpatterns = [path("r_create/<int:content>/", views.CreateReviewView, name="create_review")]