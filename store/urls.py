from django.urls import path
from .views import *

urlpatterns = [

    # Items URLs
    path("item/", ItemView.as_view(), name="item"),
    path("item/<uuid:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("item/by-supplier/<uuid:pk>/", get_items_by_supplier, name="get_item_by_supplier"),

    # Items Supply Tracking URLs
    path("supply/all/", get_items_supply_list, name="get_supply_list"),
    path("supply/<uuid:pk>/", get_supply_info, name="supply_details"),
    path("supply/by-item/<uuid:pk>/", get_supply_info_by_item, name="item_supplies_info")
]
