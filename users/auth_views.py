from .view_imports import *
from .auth_imports import *

User = get_user_model()


@swagger_auto_schema(methods=['POST'], request_body=RegisterSerializer, responses={400: GeneralMessageSerializer(), 201: LoginResponseSerializer()})
@api_view(["POST"])
@permission_classes([AllowAny])
def create_employee_account(request):
    serializer = RegisterSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValueError("User already exists")

        if serializer.data.get("password") != serializer.data.get("password2"):
            raise ValueError("Password Mismatch")

        user = User.objects.create_staff(
            firstname=serializer.data.get('firstname'),
            lastname=serializer.data.get('lastname'),
            email=email,
            phone=serializer.data.get('phone'),
            password='',
        )

        user.set_password(serializer.data.get("password"))
        user.save()

        token = create_auth_token(user)
        login(request, user)

        return Response({"email": user.email, "token": token}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            return_general_message(str(e)), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(methods=['POST'], request_body=LoginRequestSerializer, responses={400: GeneralMessageSerializer(), 200: LoginResponseSerializer()})
@api_view(["POST"])
@permission_classes([AllowAny])
def employee_login(request):
    serializer = LoginRequestSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        user = User.objects.filter(email=email)

        if not user.exists():
            raise ValueError("User does not exits")

        password = serializer.data.get("password")
        user = authenticate(username=email, password=password)
        if user is None:
            raise ValueError("Incorrect password")
        else:
            token = create_auth_token(user)
            login(request, user)
        return Response({"email": user.email, "token": token}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            return_general_message(str(e)), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(methods=['POST'], responses={200: GeneralMessageSerializer()})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def employee_logout(request):
    logout(request)
    return Response(return_general_message("Logout Success"), status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET'], responses={200: UserSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_employees(request):
    users = User.objects.filter(is_active=True, is_superuser=False).only(
        "id", "firstname", "email", "phone"
    )
    serializer = UserSerializer(users, many=True).data
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(serializer, request)
    response = paginator.get_paginated_response(result_page)
    response.status_code = status.HTTP_200_OK
    return response


@swagger_auto_schema(methods=['GET'], responses={200: UserSerializer(), 404: GeneralMessageSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_employee(request, pk):
    try:
        users = User.objects.get(id=pk, is_active=True, is_superuser=False)
    except ObjectDoesNotExist:
        return Response(return_general_message("User not found"), status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(users, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)
