from rest_framework.permissions import BasePermission

class IsClient (BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'


class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'courier'


class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
