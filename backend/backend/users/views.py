from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.users.api.serializers import UserSerializer, UserRoleUpdateSerializer, UserBasicInfoUpdateSerializer, \
    UserUdrugaAdditionalInfoSerializer, OrganizationUserSerializer
from backend.users.models import User, Organization
from backend.users.permissions import CanAccessUpdateType, CanAccessBasicInfo, CanAccessUdrugaInfo


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

user_detail_view = UserDetailView.as_view()

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



class CreateUserView(generics.CreateAPIView): #generičan view koji hendla kreiranje novog korisnika/objekta
    queryset = User.objects.all() #pregledava da ne napravimo duplikata
    serializer_class = UserSerializer # javlja viewu koje podatke trebamo prihvatiti za novog korisnika
    permission_classes = [AllowAny] # tko smije ovo pozvati (u nasem slucaju svi mogu napraviti korisnika)


class UserUpdateView(generics.UpdateAPIView): #LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    '''def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user'''


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()

class UserDelete(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()  # pregledava da ne napravimo duplikata

    '''def get_queryset(self):
        user = self.request.user #radimo ovako queryset jer nam je to ovisno u useru
        return User.objects.filter(author=user) # zelimo da samo gledamo za naseg ulogiranog korisnika'''

user_delete_view = UserDelete.as_view()

class UserMeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.user.role == 'recipient.association' and hasattr(self.request.user, 'organization'):
            return OrganizationUserSerializer
        return UserSerializer

class UserUpdateRole(generics.UpdateAPIView):
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(registration_step = 1)
        if user.role == 'donor' or user.role == 'recipient_individual' or user.role == 'recipient.association':
            permission = Permission.objects.get(codename='can_access_basic_info')
            user.user_permissions.add(permission)

user_update_role_view = UserUpdateRole.as_view()


'''class UserUpdateType(generics.UpdateAPIView):
    serializer_class = UserTypeUpdateSerializer
    permission_classes = [CanAccessUpdateType]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(registration_step = 2)
        if user.type == "udruga":
            if not hasattr(user, 'organization'):
                Organization.objects.create(user=user, company_name="", company_email="")
        permission =  Permission.objects.get(codename='can_access_type')
        user.user_permissions.remove(permission)
        permission = Permission.objects.get(codename='can_access_basic_info')
        user.user_permissions.add(permission)

user_update_type_view = UserUpdateType.as_view()'''

class UserBasicInfoUpdateView(generics.UpdateAPIView):
    serializer_class = UserBasicInfoUpdateSerializer
    permission_classes = [CanAccessBasicInfo]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(registration_step = 3)
        if user.role == "recipient.association":
            permission = Permission.objects.get(codename='can_access_basic_info')
            user.user_permissions.remove(permission)
            permission = Permission.objects.get(codename='can_access_udruga_additional_info')
            user.user_permissions.add(permission)

user_basic_info_update_view = UserBasicInfoUpdateView.as_view()


class UserUdrugaAddView(generics.UpdateAPIView):
    serializer_class = UserUdrugaAdditionalInfoSerializer
    permission_classes = [CanAccessUdrugaInfo]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(registration_step=4)
        permission = Permission.objects.get(codename='can_access_udruga_additional_info')
        user.user_permissions.remove(permission)


class UserAdminView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)
