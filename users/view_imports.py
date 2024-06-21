import requests
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .serializers import GeneralMessageSerializer
from django.core.exceptions import ObjectDoesNotExist
from inventory_management.custom_pagination import CustomPagination
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny


def return_general_message(message, detail=""):
    return {
        "message": str(message),
        "detail": detail
    }
