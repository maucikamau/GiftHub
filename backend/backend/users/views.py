from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import RedirectView
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.users.api.serializers import UserSerializer, UserRoleUpdateSerializer, UserBasicInfoUpdateSerializer, \
    UserUdrugaAdditionalInfoSerializer, OrganizationUserSerializer, LocationSerializer
from backend.users.models import User, Association, LocationCroatia
from backend.users.permissions import CanAccessBasicInfo, CanAccessUdrugaInfo


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


class CreateUserView(generics.CreateAPIView):  # generičan view koji hendla kreiranje novog korisnika/objekta
    queryset = User.objects.all()  # pregledava da ne napravimo duplikata
    serializer_class = UserSerializer  # javlja viewu koje podatke trebamo prihvatiti za novog korisnika
    permission_classes = [AllowAny]  # tko smije ovo pozvati (u nasem slucaju svi mogu napraviti korisnika)


class UserUpdateView(generics.UpdateAPIView):  # LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
        if self.request.user.role == 'recipient_association' and hasattr(self.request.user, 'association'):
            return OrganizationUserSerializer
        return UserSerializer

    def get(self, request, *args, **kwargs):
        """Return serialized user data with an added `permissions` list."""
        user = self.get_object()
        serializer = self.get_serializer(user, context={"request": request})
        data = dict(serializer.data)
        # include all permissions the user has (including group permissions)
        data["permissions"] = sorted(request.user.get_all_permissions())
        return Response(data, status=status.HTTP_200_OK)


class UserUpdateRole(generics.UpdateAPIView):
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(registration_step=1)
        if user.role == 'donor' or user.role == 'recipient_individual' or user.role == 'recipient_association':
            permission = Permission.objects.get(codename='can_access_basic_info')
            user.user_permissions.add(permission)

            role_group = Group.objects.get(name=user.role)
            user.groups.add(role_group)


user_update_role_view = UserUpdateRole.as_view()


class UserBasicInfoUpdateView(generics.UpdateAPIView):
    serializer_class = UserBasicInfoUpdateSerializer
    permission_classes = [CanAccessBasicInfo]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(registration_step=3)
        if user.role == "recipient_association":
            permission = Permission.objects.get(codename='can_access_basic_info')
            user.user_permissions.remove(permission)
            permission = Permission.objects.get(codename='can_access_udruga_additional_info')
            user.user_permissions.add(permission)


user_basic_info_update_view = UserBasicInfoUpdateView.as_view()


class RegisterAssociationView(generics.CreateAPIView):
    """Create a new Association (unique by email), link it to the logged in user,
    and remove the `can_access_udruga_additional_info` permission when successful."""
    serializer_class = UserUdrugaAdditionalInfoSerializer
    permission_classes = [CanAccessUdrugaInfo]

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assoc_email = serializer.validated_data.get('association_email')

        # enforce uniqueness by email if provided
        if assoc_email and Association.objects.filter(association_email=assoc_email).exists():
            return Response({"detail": "Association with this email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        # create and link to user
        association = serializer.save(user=request.user)

        request.user.registration_step = 3
        request.user.save()

        # remove the permission from the user
        try:
            permission = Permission.objects.get(codename='can_access_udruga_additional_info')
            request.user.user_permissions.remove(permission)
        except Permission.DoesNotExist:
            pass

        return Response(self.get_serializer(association).data, status=status.HTTP_201_CREATED)


class UserAdminView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)


class CitiesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = LocationCroatia.objects.all()

