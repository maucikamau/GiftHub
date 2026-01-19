from django.urls import path

from .views import ReviewSetView, ReviewSeeListView, ReviewGetAvgView
app_name = "reviews"

urlpatterns = [
    path("create", ReviewSetView.as_view(), name="createReview"),
    path("list/<int:user>", ReviewSeeListView.as_view(), name="listReviews"),
    path("average/<int:user>", ReviewGetAvgView.as_view(), name="averageReviews")
]
