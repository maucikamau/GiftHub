from django.urls import path

from .views import user_detail_view, CreateUserView, UserList, user_delete_view, UserMeView, user_update_type_view, \
    user_basic_info_update_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", UserMeView.as_view(), name="detail"),
    path("list/", UserList.as_view(), name="list"),
    path("register/", CreateUserView.as_view(), name="register"), #kad idemo na taj url otvara se ovaj view
    path("register/type/", view=user_update_type_view, name="type"),
    path("register/basicinfo/", view=user_basic_info_update_view, name="basicinfo"),
    path("register/udruga-additional-info/", CreateUserView.as_view(), name="register"),
    path("deleteUser/<int:pk>/", view=user_delete_view, name="deleteUser"),
    path("me/", UserMeView.as_view(), name="myProfile"),
]
