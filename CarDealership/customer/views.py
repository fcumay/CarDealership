from .forms import LoginForm, SignUpForm
from .models import RoleChoices
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class RegisterCustomerView(View):
    template_name = "register.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login_view")
        else:
            msg = "Form is not valid"
        return render(request, self.template_name, {"form": form, "msg": msg})


class LoginView(View):
    template_name = "login.html"
    token_validity = 7

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)

                refresh = RefreshToken.for_user(user)
                token = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                if user.role == RoleChoices.is_superuser:
                    response = redirect("admin:index")
                elif user.role == RoleChoices.is_customer:
                    response = redirect("customer")
                elif user.role == RoleChoices.is_dealership_admin:
                    response = redirect("dealership_admin")
                response.set_cookie(
                    key="jwt_token",
                    value=token["access"],
                    httponly=True,
                    max_age=self.token_validity * 24 * 60 * 60,
                )

                return response

            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating form"

        return render(request, self.template_name, {"form": form, "msg": msg})


class CustomerView(View):
    def get(self, request):
        return render(request, "customer.html")


class DealershipAdminView(View):
    def get(self, request):
        return render(request, "dealership_admin.html")


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
                                (" 5 step creator is superuser")
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
                                age=None,
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
