from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # svi mogu čitati
        if request.method in permissions.SAFE_METHODS:
            return True
        # samo vlasnik može mijenjati/brisati
        return obj.owner == request.user
