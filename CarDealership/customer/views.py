from django_countries import countries
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import RoleChoices, Customer, BuyingHistoryCustomer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, BuyingHistoryCustomerSerializer

User = get_user_model()


class RegisterViewAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data

            name = data["name"]
            email = data["email"]
            email = email.lower()
            password = data["password"]
            re_password = data["re_password"]
            role = data["role"]

            if role not in RoleChoices.values:
                return Response(
                    {"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST
                )

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if role == RoleChoices.is_dealership_admin:
                            if request.user.role == RoleChoices.is_superuser:
                                User.objects.create_dealership_admin(
                                    email=email, name=name, password=password
                                )
                                return Response(
                                    {
                                        "success": "Dealership admin created successfully"
                                    },
                                    status=status.HTTP_201_CREATED,
                                )
                            else:
                                return Response(
                                    {
                                        "error": "Only superuser can create Dealership_admin user"
                                    },
                                    status=status.HTTP_403_FORBIDDEN,
                                )
                        else:
                            User.objects.create_customer(
                                email=email,
                                name=name,
                                password=password,
                                balance=None,
                                location=None,
                                contact_number=None,
                                dob=None,
                            )
                            return Response(
                                {"success": "User created successfully"},
                                status=status.HTTP_201_CREATED,
                            )
                    else:
                        return Response(
                            {"error": "User with this email already exists"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"error": "Passwords must be at least 8 characters in length"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                return Response(
                    {"error": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when registering an account"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveUserView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response({"user": user.data}, status=status.HTTP_200_OK)
        except BaseException:
            return Response(
                {"error": "Something went wrong when retrieving user details"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):

        try:
            data = request.data
            for code, name in countries:
                if name == data["location"]:
                    location = code
                    break
            Customer.objects.filter(email=request.user.email).update(
                name=data["name"],
                location=location,
                contact_number=data["contact_number"],
                dob = data["dob"]
            )
            return Response(
                {"success": "User update successfully"}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"error": "Something went wrong when updating user information"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BuyingHistoryCustomerView(APIView):
    def get(self, request, format=None):
        history = BuyingHistoryCustomer.objects.filter(customer=request.user)
        history = BuyingHistoryCustomerSerializer(history, many=True)
        return Response({"History": history.data}, status=status.HTTP_200_OK)

