from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, user_object):
        return request.user == user_object

class IsObjectOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, object):
        return request.user == object.user
