from django.conf import settings
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=120, blank=True, default="ban")

    def __str__(self) -> str:
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=120, blank=True, default="ban")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="unique_item_name_per_category")
        ]
    
    def __str__(self) -> str:
        return self.name

class ShoppingList(TimeStampedModel):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shopping_lists")

    items = models.ManyToManyField(Item, through="ListItem", related_name="lists")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_list_name_per_user")
        ]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.user_id})"
    
class ListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="list_items")
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="list_items")

    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    note = models.TextField(blank=True, default="")
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["shopping_list", "item"], name="unique_item_per_list")
        ]

    def __str__(self) -> str:
        return f"{self.shopping_list_id} -> {self.item_id} x{self.quantity}"