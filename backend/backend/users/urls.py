from django.urls import path

from .views import CreateUserView, UserList, user_delete_view, UserMeView, \
    user_basic_info_update_view, UserAdminView, UserLogoutView, RegisterAssociationView, user_update_role_view, \
    CitiesView
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", UserAdminView.as_view(), name="detail"),
    path("list/", UserList.as_view(), name="list"),
    path("register/", CreateUserView.as_view(), name="register"),
    path("register/role/", view=user_update_role_view, name="role"),
    path("register/basicinfo/", view=user_basic_info_update_view, name="basicinfo"),
    path("register/association/", RegisterAssociationView.as_view(), name="udruge"),
    path("deleteUser/<int:pk>/", view=user_delete_view, name="deleteUser"),
    path("cities/", view=CitiesView.as_view(), name="cities"),
    path("me/", UserMeView.as_view(), name="myProfile"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
