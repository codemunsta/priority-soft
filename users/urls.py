from django.urls import path
from .views import *

urlpatterns = [

    # Auth URLs
    path("accounts/create/account/", create_employee_account, name="create_employee_account"),
    path("accounts/login/", employee_login, name="employee_login"),
    path("accounts/logout/", employee_logout, name="employee_logout"),
    path("accounts/get/employees/", get_all_employees, name="get_all_employees"),
    path("accounts/get/employee/<uuid:pk>", get_all_employees, name="get_employee_by_id"),

    # Supplier URLs
    path("supplier/", SupplierView.as_view(), name="create_supplier"),
    path("supplier/<uuid:pk>/", SupplierDetailView.as_view(), name="get_or_update_supplier")

]
