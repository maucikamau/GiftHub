from rest_framework.permissions import IsAuthenticated


class HasPermission(IsAuthenticated):
    """Base permission class to check if user has specific permission"""
    permission_codename = None

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.has_perm(f'users.{self.permission_codename}')

class CanAccesUpdateRole(HasPermission):
    """Permission for accessing the type update view (step 1)"""
    permission_codename = "can_access_update_role"

class CanAccessUpdateType(HasPermission):
    """Permission for accessing the type update view (step 2)"""
    permission_codename = 'can_access_update_type'


class CanAccessBasicInfo(HasPermission):
    """Permission for accessing the basic info update view (step 3)"""
    permission_codename = 'can_access_basic_info'


class CanAccessUdrugaInfo(HasPermission):
    """Permission for accessing the udruga additional info view (step 4)"""
    permission_codename = 'can_access_udruga_additional_info'

