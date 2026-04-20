from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS
    

class IsNotTestUser(BasePermission):
    def has_permission(self, request, view):
        is_test = request.user.username == "test"
        return not is_test
    

class IsAdminForDeleteAndPatchAndReadOnly(BasePermission):
    def has_object_permission (self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['DELETE', 'PATCH']:
            return bool(request.user and request.user.is_superuser)
        return bool(request.user and request.user.is_staff)
        


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['DELETE', 'PATCH']:
            return request.user.is_authenticated and (request.user == obj.user or request.user and request.user.is_superuser)
        else:
            return request.user.is_authenticated and (request.user == obj.user or request.user.is_staff)
        