from .views_imports import *
from .item_supply_imports import *


@swagger_auto_schema(methods=['GET'], responses={200: ItemSupplySerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_items_supply_list(request):
    items_supply = ItemSupply.objects.all().order_by("-date_updated")
    serializer = ItemSupplySerializer(items_supply, many=True).data
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(serializer, request)
    response = paginator.get_paginated_response(result_page)
    response.status_code = status.HTTP_200_OK
    return response


@swagger_auto_schema(methods=['GET'], responses={200: ItemSupplySerializer(), 404: GeneralMessageSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_supply_info(request, pk):
    try:
        items_supply = ItemSupply.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(return_general_message("Supply information not found"), status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSupplySerializer(items_supply).data
    return Response(serializer, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET'], responses={200: ItemSupplySerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_supply_info_by_item(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(return_general_message("Item not found"), status=status.HTTP_404_NOT_FOUND)
    items_supply = ItemSupply.objects.filter(item=item).order_by("-date_updated")
    serializer = ItemSupplySerializer(items_supply, many=True).data
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(serializer, request)
    response = paginator.get_paginated_response(result_page)
    response.status_code = status.HTTP_200_OK
    return response
