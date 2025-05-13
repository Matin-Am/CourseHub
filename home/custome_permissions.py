from rest_framework.permissions import BasePermission , SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "You are not allowed to do this action"


    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user    

    def has_object_permission(self, request, view, obj):
        if request in (SAFE_METHODS or 'POST'):
            return True
        return obj.user == request.user