from rest_framework import permissions


class HasScrapPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("part.view_part")
