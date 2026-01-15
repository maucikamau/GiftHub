from django.urls import path

from .views import CreateCampaignView, UpdateCampaignView, CampaignListView, CampaignsMeView, CampaignSpecificView, CampaignDonate

app_name = "campaigns"

urlpatterns = [
    path("", CampaignListView.as_view(), name="allCampaigns"),
    path("create/", CreateCampaignView.as_view(), name="createCampaign"),
    path("update/<int:pk>/", UpdateCampaignView.as_view(), name="updateCampaign"),
    path("me/", CampaignsMeView.as_view(), name="myCampaigns"),
    path("<int:pk>/", CampaignSpecificView.as_view(), name="pkCampaigns"),
    path("donate/<str:item>/", CampaignDonate.as_view(), name="donateCampaign"),
]
