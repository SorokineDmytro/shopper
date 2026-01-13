from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Item, ShoppingList, ListItem

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon"]

class ItemSerializer(serializers.ModelSerializer):
    # Readable nested item
    category = CategorySerializer(read_only=True)
    # Write using id
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Item
        fields = ["id", "name", "icon", "category_id"]

class ListItemsSerializer(serializers.ModelSerializer):
    # Readable nested item
    item = ItemSerializer(read_only=True)
    # Write using id
    item_id = serializers.PrimaryKeyRelatedField(
        queryst=Item.objects.all(), source="item", write_only=True
    )

    class Meta:
        model = ListItem
        fields = ["id", "shopping_list", "item", "item_id", "quantity", "note", "is_checked", "created_at"]
        read_only_fields = ["id", "created_at", "shopping_list"]

    def validate_quantity(self, value):
        if(value <= 0):
            raise serializers.ValidationError("Quantity must be > 0.")
        return value

class ShoppinListSerializer(serializers.ModelSerializer):
    # Return all list_items with nested item/category
    list_items = ListItemsSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingList
        fields = ["id", "name", "created_at", "modified_at", "list_items"]
        read_only_fields = ["id", "created_at", "modified_at"]