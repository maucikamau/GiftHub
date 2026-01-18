from django.urls import path

from .views import ReviewSetView
app_name = "reviews"

urlpatterns = [
    path("create", ReviewSetView.as_view(), name="createReview"),
]
