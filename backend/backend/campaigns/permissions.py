from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        # Staff and superuser can always modify
        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        # User must have permission to change campaigns
        if not user.has_perm("campaigns.change_campaign"):
            return False

        # Only owner can change or delete
        return obj.owner == request.user


class CanCreateCampaign(permissions.BasePermission):
    """
    Allow campaign creation only for users with the model add permission.
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        # Staff/superuser always allowed
        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        # Check Django model permission
        return user.has_perm("campaigns.add_campaign")
