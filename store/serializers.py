from .models import Item, ItemSupply
from rest_framework import serializers
from users.serializers import SupplierSerializer
from drf_yasg.utils import swagger_serializer_method


class ItemSerializer(serializers.ModelSerializer):

    suppliers = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id", "name", "description", "price", "quantity", "date_created", "suppliers"
        ]

    @swagger_serializer_method(SupplierSerializer)
    def get_suppliers(self, instance):
        suppliers = instance.suppliers.all()
        return SupplierSerializer(suppliers, many=True).data


class ItemCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=225)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=17, decimal_places=2)
    quantity = serializers.IntegerField()
    supplier = serializers.UUIDField()


class SupplierItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [
            "id", "name", "price", "quantity",
        ]


class ItemSupplySerializer(serializers.ModelSerializer):

    item = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    registerer = serializers.SerializerMethodField()

    class Meta:
        model = ItemSupply
        fields = [
            "id", "item", "quantity_supplied", "supplier", "registerer", "date_created"
        ]

    def get_item(self, instance):
        return {
            "id": instance.item.id,
            "name": instance.item.name
        }

    def get_supplier(self, instance):
        return {
            "id": instance.supplier.id,
            "name": instance.supplier.name,
            "contact": instance.supplier.get_contact_info()
        }

    def get_registerer(self, instance):
        return {
            "id": instance.registerer.id,
            "name": instance.registerer.get_username()
        }
