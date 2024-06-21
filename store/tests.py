from faker import Faker
from django.urls import reverse
from users.models import Supplier
from rest_framework import status
from .models import Item, ItemSupply
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()
simulator = Faker()


class StoreItemsTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email=simulator.email(),
            phone=simulator.phone_number()[:19],
            firstname=simulator.first_name(),
            lastname=simulator.last_name(),
            password="passWord@101",
        )

        self.supplier = Supplier.objects.create(
            name=simulator.name(),
            phone=simulator.phone_number()[:19],
            address=simulator.address()
        )

        self.item = Item.objects.create(
            name=simulator.name(),
            description=simulator.text(),
            price=15.00,
            quantity=15
        )

        self.item_supply = ItemSupply.objects.create(
            item=self.item,
            quantity_supplied=self.item.quantity,
            supplier=self.supplier,
            registerer=self.user
        )

        self.item.suppliers.add(self.supplier)

        self.employee_login_url = reverse("employee_login")

        response = self.client.post(self.employee_login_url, {
            'email': self.user.email,
            'password': "passWord@101"
        }, format='json')

        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION=data['token'])

        self.request_data = {
            "name": simulator.name(),
            "description": simulator.text(),
            "price": "10.00",
            "quantity": 10,
            "supplier": self.supplier.id
        }

        self.update_data = {
            "name": simulator.name(),
            "description": simulator.text(),
            "price": "10.00",
            "quantity": 10,
        }

        self.item_url = reverse("item")
        self.item_details_url = lambda pk: reverse("item_detail", kwargs={'pk': pk})
        self.supplier_items_url = lambda pk: reverse("get_item_by_supplier", kwargs={'pk': pk})
        self.get_item_supply_list_url = reverse("get_supply_list")
        self.get_supply_info_url = lambda pk: reverse("supply_details", kwargs={'pk': pk})
        self.get_supply_by_item_url = lambda pk: reverse("item_supplies_info", kwargs={'pk': pk})

    def test_create_item(self):
        response = self.client.post(self.item_url, self.request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_items(self):
        response = self.client.get(self.item_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item(self):
        item = Item.objects.all().first()
        response = self.client.get(self.item_details_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        item = Item.objects.all().first()
        response = self.client.put(self.item_details_url(item.id), self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_supplier(self):
        item = Item.objects.all().first()
        response = self.client.delete(self.item_details_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_suppler_items(self):
        supplier = Supplier.objects.all().first()
        response = self.client.get(self.supplier_items_url(supplier.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item_supply_list(self):
        response = self.client.get(self.get_item_supply_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_supply_info(self):
        item = ItemSupply.objects.all().first()
        response = self.client.get(self.get_supply_info_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_supply_by_item(self):
        item = Item.objects.all().first()
        response = self.client.get(self.get_supply_by_item_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
