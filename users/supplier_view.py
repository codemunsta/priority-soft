from .view_imports import *
from .supplier_view_imports import *

User = get_user_model()


class SupplierView(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer

    @swagger_auto_schema(
        request_body=SupplierSerializer(),
        responses={201: GeneralMessageSerializer(), 400: GeneralMessageSerializer()},
        operation_summary="Create Supplier",
        operation_description="Create a supplier by passing the required information specified in the serializer definition."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(return_general_message("Supplier Created..."), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(return_general_message(str(e)), status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: SupplierSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Get all supplier",
        operation_description="Get a list of all the available suppliers"
    )
    def get(self, request):
        suppliers = Supplier.objects.all().order_by("-created_at")
        serializer = self.serializer_class(suppliers, many=True).data
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(serializer, request)
        response = paginator.get_paginated_response(result_page)
        response.status_code = status.HTTP_200_OK
        return response


class SupplierDetailView(APIView):

    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer

    @swagger_auto_schema(
        responses={200: SupplierSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Get a supplier",
        operation_description="Get details of a specific supplier by passing the id of the supplier"
    )
    def get(self, request, pk):
        try:
            supplier = Supplier.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(return_general_message("Supplier not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(supplier).data
        return Response(serializer, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SupplierSerializer(),
        responses={200: SupplierSerializer(), 400: GeneralMessageSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Update a supplier",
        operation_description="update details of a specific supplier by passing the id of the supplier along with details to update"
    )
    def put(self, request, pk):
        try:
            supplier = Supplier.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(return_general_message("Supplier not found"), status=status.HTTP_404_NOT_FOUND)
        data = self.serializer_class(supplier, data=request.data, partial=True)
        try:
            if data.is_valid(raise_exception=True):
                data.save()
                return Response(data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(return_general_message(str(e)), status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: GeneralMessageSerializer(), 404: GeneralMessageSerializer()},
        operation_summary="Delete a supplier",
        operation_description="Delete a specific supplier by passing the id of the supplier"
    )
    def delete(self, request, pk):
        try:
            supplier = Supplier.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(return_general_message("Supplier not found"), status=status.HTTP_404_NOT_FOUND)
        supplier.delete()
        return Response(return_general_message("Supplier Deleted..."), status=status.HTTP_200_OK)
