# courses/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrReadOnly(BasePermission):
    """
    Teacher bo‘lsa o‘zgartira oladi, boshqalar faqat o‘qiy oladi.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_teacher

class IsOwnerOrReadOnly(BasePermission):
    """
    Faqat o‘zi yaratgan obyektni tahrirlashi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.teacher == request.user
