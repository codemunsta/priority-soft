import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)
    firstname = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        return f"{self.firstname} {self.lastname}"

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(update_fields=['is_active'])


class Supplier(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)
    address = models.TextField()
    items = models.ManyToManyField('store.Item', related_name='suppliers')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def get_contact_info(self):
        return {
            "phone": self.phone,
            "address": self.address
        }
