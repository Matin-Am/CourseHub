from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "You are not allowed to do this action"


    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user    

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user