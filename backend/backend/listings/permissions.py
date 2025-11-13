from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        if not user.has_perm("listings.change_listing"):
            return False

        # only owner can change or delete
        return obj.owner == request.user


class CanCreateListing(permissions.BasePermission):
    """Allow listing creation only for users with the model add permission.
    """

    def has_permission(self, request, view):

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        # staff/superuser always allowed
        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        # check Django model permission
        return user.has_perm("listings.add_listing")
