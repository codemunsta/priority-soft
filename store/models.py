import uuid
from django.db import models


class Item(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)
    description = models.TextField()
    price = models.DecimalField(max_digits=17, decimal_places=2)
    quantity = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ItemSupply(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey("store.Item", on_delete=models.CASCADE)
    supplier = models.ForeignKey("users.Supplier", null=True, on_delete=models.SET_NULL)
    registerer = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item.name
