from rest_framework.permissions import IsAdminUser

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin:
    permission_classes = [IsAdminUser, IsStaffEditorPermission]


class UserQueryMixin:
    user_field = 'user'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        lookup_data = {self.user_field: user}
        return queryset.filter(**lookup_data)
