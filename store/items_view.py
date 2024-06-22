from .views_imports import *
from .items_view_imports import *


class ItemView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    @swagger_auto_schema(
        request_body=ItemCreateSerializer(),
        responses={201: GeneralMessageSerializer(), 400: GeneralMessageSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Create Item",
        operation_description="Create an Item by passing the required information specified in the serializer definition."
    )
    def post(self, request):
        serializer = ItemCreateSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
                supplier_id = data.pop("supplier")
                try:
                    supplier = Supplier.objects.get(id=supplier_id)
                except ObjectDoesNotExist:
                    return Response(return_general_message("Invalid Supplier"), status=status.HTTP_404_NOT_FOUND)
                item_data = self.serializer_class(data=data)
                if item_data.is_valid(raise_exception=True):
                    data = item_data.validated_data
                    item = Item.objects.create(
                        **data
                    )
                    item.suppliers.add(supplier)
                    item.save()

                    ItemSupply.objects.create(
                        item=item,
                        quantity_supplied=data.get("quantity"),
                        supplier=supplier,
                        registerer=request.user
                    )
                return Response(return_general_message("Item Created..."), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(return_general_message(str(e)), status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: ItemSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Get all Items",
        operation_description="Get a list of all the available items"
    )
    def get(self, request):
        items = Item.objects.all().order_by("-date_created")
        serializer = self.serializer_class(items, many=True).data
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(serializer, request)
        response = paginator.get_paginated_response(result_page)
        response.status_code = status.HTTP_200_OK
        return response


class ItemDetailView(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    serializer_update_class = ItemUpdateSerializer

    @swagger_auto_schema(
        responses={200: ItemSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Get an Item",
        operation_description="Get details of a specific item by passing the id of the item"
    )
    def get(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(return_general_message("Item not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(item).data
        return Response(serializer, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ItemUpdateSerializer(),
        responses={200: ItemSerializer(), 400: GeneralMessageSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Update an Item",
        operation_description="update details of a specific item by passing the id of the item along with details to update"
    )
    def put(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(return_general_message("Item not found"), status=status.HTTP_404_NOT_FOUND)
        data = self.serializer_update_class(item, data=request.data, partial=True)
        try:
            if data.is_valid(raise_exception=True):
                data_ = data.validated_data
                if data_.get("quantity") and data_.get("quantity") < 0:
                    return Response(return_general_message("Quantity cannot be less than 0"), status=status.HTTP_404_NOT_FOUND)
                data.save()
                return Response(data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(return_general_message(str(e)), status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: GeneralMessageSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Delete an Item",
        operation_description="Delete a specific item by passing the id of the item"
    )
    def delete(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(return_general_message("Item not found"), status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(return_general_message("Item Deleted..."), status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET'], responses={200: SupplierItemSerializer(), 404: GeneralMessageSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_items_by_supplier(request, pk):
    try:
        supplier = Supplier.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(return_general_message("Invalid Supplier Selected"), status=status.HTTP_404_NOT_FOUND)
    items = supplier.items.all()
    serializer = SupplierItemSerializer(items, many=True).data
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(serializer, request)
    response = paginator.get_paginated_response(result_page)
    response.status_code = status.HTTP_200_OK
    return response


@swagger_auto_schema(methods=['POST'], responses={200: GeneralMessageSerializer(), 404: GeneralMessageSerializer()})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_supplier(request, item_id, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
    except ObjectDoesNotExist:
        return Response(return_general_message("Invalid Supplier Selected"), status=status.HTTP_404_NOT_FOUND)
    try:
        item = Item.objects.get(id=item_id)
    except ObjectDoesNotExist:
        return Response(return_general_message("Item not found"), status=status.HTTP_404_NOT_FOUND)
    item.suppliers.add(supplier)
    return Response(return_general_message("Supplier Added..."), status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['POST'], request_body=SupplyItemSerializer(), responses={200: GeneralMessageSerializer(), 404: GeneralMessageSerializer()})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def supply_item(request, item_id, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
    except ObjectDoesNotExist:
        return Response(return_general_message("Invalid Supplier Selected"), status=status.HTTP_404_NOT_FOUND)
    try:
        item = Item.objects.get(id=item_id)
    except ObjectDoesNotExist:
        return Response(return_general_message("Item not found"), status=status.HTTP_404_NOT_FOUND)
    data = request.data
    if supplier in item.suppliers.all():
        item.quantity += int(data.get("quantity"))
        item.save()
        ItemSupply.objects.create(
            item=item,
            quantity_supplied=data.get("quantity"),
            supplier=supplier,
            registerer=request.user
        )
        return Response(return_general_message("Item Supplied..."), status=status.HTTP_200_OK)
    else:
        return Response(return_general_message("Supplier does not provide this item..."), status=status.HTTP_200_OK)

