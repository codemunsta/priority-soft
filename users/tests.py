from faker import Faker
from .models import Supplier
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()
simulator = Faker()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.create_employee_url = reverse("create_employee_account")
        self.employee_login_url = reverse("employee_login")
        self.employee_logout_url = reverse("employee_logout")

        self.request_data = {
            "email": simulator.email(),
            "phone": simulator.phone_number()[:19],
            "firstname": simulator.first_name(),
            "lastname": simulator.last_name(),
            "password": "passWord@101",
            "password2": "passWord@101"
        }

    def test_create_employee(self):
        response = self.client.post(self.create_employee_url, self.request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_employee_login(self):
        self.client.post(self.create_employee_url, self.request_data, format="json")
        response = self.client.post(self.employee_login_url, {
            'email': self.request_data['email'],
            'password': self.request_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_employee_login__invalid_credentials(self):
        self.client.post(self.create_employee_url, self.request_data, format='json')

        invalid_login_data = {
            'email': self.request_data['email'],
            'password': 'WrongPassword'
        }
        response = self.client.post(self.employee_login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmployeeQueryTest(APITestCase):

    def setUp(self):
        self.users = []

        for _ in range(3):
            user = User.objects.create_user(
                email=simulator.email(),
                phone=simulator.phone_number()[:19],
                firstname=simulator.first_name(),
                lastname=simulator.last_name(),
                password="passWord@101",
            )
            self.users.append(user)

        self.employee_login_url = reverse("employee_login")

        response = self.client.post(self.employee_login_url, {
            'email': self.users[0].email,
            'password': "passWord@101"
        }, format='json')

        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION=data['token'])

        self.get_all_employees_url = reverse("get_all_employees")
        self.get_employee_url = lambda pk: reverse("get_employee_by_id", kwargs={'pk': pk})

    def test_get_all_employees(self):
        response = self.client.get(self.get_all_employees_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_employee(self):
        user = self.users[0]
        response = self.client.get(self.get_employee_url(user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SupplierTests(APITestCase):

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

        self.employee_login_url = reverse("employee_login")

        response = self.client.post(self.employee_login_url, {
            'email': self.user.email,
            'password': "passWord@101"
        }, format='json')

        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION=data['token'])

        self.request_data = {
            "name": simulator.name(),
            "phone": simulator.phone_number()[:19],
            "address": simulator.address()
        }

        self.supplier_url = reverse("supplier")
        self.supplier_details_url = lambda pk: reverse("get_or_update_supplier", kwargs={'pk': pk})

    def test_create_supplier(self):
        response = self.client.post(self.supplier_url, self.request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_suppliers(self):
        response = self.client.get(self.supplier_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_supplier(self):
        supplier = Supplier.objects.all().first()
        response = self.client.get(self.supplier_details_url(supplier.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_supplier(self):
        supplier = Supplier.objects.all().first()
        response = self.client.put(self.supplier_details_url(supplier.id), self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_supplier(self):
        supplier = Supplier.objects.all().first()
        response = self.client.delete(self.supplier_details_url(supplier.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
