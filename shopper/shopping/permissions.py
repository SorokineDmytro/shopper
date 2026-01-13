from rest_framework.permissions import BasePermission

class IsOwnerOfShoppingList(BasePermission):
    # Object-level permission: only owners can access their ShoppingList.

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id