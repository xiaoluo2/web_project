from rest_framework import permissions

class IsUser():

    def has_object_permission(self, request, view, obj):
        return obj == request.user
