from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django_countries import countries
from customer.models import RoleChoices
from .models import (
    Dealership,
    Brand,
    Customer,
    DrivetrainChoices,
    FuelTypeChoices,
    BodyTypeChoices,
    TransmissionChoices,
    Model,
    Car,
)
from .permissions import CanGetDealership, CanModifyDealership, CanDeleteDealership
from .serializers import (
    DealershipSerializer,
    BrandSerializer,
    ModelSerializer,
    CarSerializer,
)
from django.utils import timezone
from django.db.models import Q

class ManageDealershipView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [CanGetDealership()]
        elif self.request.method == "POST":
            return [IsAdminUser()]
        elif self.request.method == "PUT":
            return [CanModifyDealership()]
        elif self.request.method == "DELETE":
            return [CanDeleteDealership()]
        return super().get_permissions()

    # def get(self, request, format=None):
    #     try:
    #         name = request.query_params.get("name")
    #         if not name:
    #             return self.get_dealerships(request)
    #         else:
    #             return self.get_dealership(request, name)
    #     except:
    #         return Response(
    #             {"error": "Something went wrong when retrieving dealerships detail"},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )
    #
    # def get_dealership(self, request, name):
    #     dealership = Dealership.objects.get(name=name)
    #     try:
    #         self.check_object_permissions(request, dealership)
    #     except:
    #         return Response(
    #             {
    #                 "error": "User does not have necessary permissions for retrieve dealerships information"
    #             },
    #             status=status.HTTP_403_FORBIDDEN,
    #         )
    #     dealership = DealershipSerializer(dealership)
    #     return Response({"dealership": dealership.data}, status=status.HTTP_200_OK)
    #
    # def get_dealerships(self, request):
    #     if request.user.role == RoleChoices.is_dealership_admin:
    #         dealerships = Dealership.objects.filter(owner=request.user)
    #     else:
    #         dealerships = Dealership.objects.all()
    #     dealerships = DealershipSerializer(dealerships, many=True)
    #     return Response({"dealerships": dealerships.data}, status=status.HTTP_200_OK)

    def get(self,request,format=None):
        try:
            dealerships=self.validation_parameters(request)
            if request.user.role == RoleChoices.is_dealership_admin:
                dealerships = dealerships.filter(owner=request.user)
            dealerships = DealershipSerializer(dealerships, many=True)
            return Response({"dealerships": dealerships.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving dealerships detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validation_parameters(self,request):
        #можно тут проводить валидацию
        #а опциональность проверять уже в методах

        name = request.query_params.get("name")
        brand=request.query_params.get("brand")
        balance=request.query_params.get("balance")
        location=request.query_params.get("location")
        contact_number=request.query_params.get("contact_number")
        discount_program=request.query_params.get("discount_program")
        owner=request.query_params.get("owner")
        criteria = Q()

        if name:
            criteria &= Q(name=name)
        if brand:
            criteria &= Q(brand=brand)
        if balance:
            criteria &= Q(balance=balance)
        if location:
            criteria &= Q(location=location)
        if contact_number:
            criteria &= Q(contact_number=contact_number)
        if discount_program:
            criteria &= Q(discount_program=discount_program)
        if owner:
            criteria &= Q(owner=owner)

        dealerships = Dealership.objects.filter(criteria)
        return dealerships



    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            Dealership.objects.create(
                name=data["name"],
                brand=data["brand"],
                location=data["location"],
                contact_number=data["contact_number"],
                discount_program=data["discount_program"],
                owner=data["owner"],
            )
            return Response(
                {"success": "Dealership created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"error": "Something went wrong when creating dealerships detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            data = request.data
            name = data["name"]
            dealership = Dealership.objects.get(name=name)
            try:
                self.check_object_permissions(request, dealership)
            except:
                return Response(
                    {
                        "error": "User does not have necessary permissions for retrieve dealerships information"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            dealership.is_active = False
            dealership.save()
            return Response(
                {"success": "Dealership publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"error": "Something went wrong when deleted dealership"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            data = request.data
            data = self.validation_values(data)
            try:
                self.check_object_permissions(
                    request, Dealership.objects.get(name=data["name"])
                )
            except:
                return Response(
                    {
                        "error": "User does not have necessary permissions for update dealerships information"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            if request.user.role == RoleChoices.is_superuser:
                Dealership.objects.filter(name=data["name"]).update(
                    name=data["name"],
                    brand=data["brand"],
                    balance=data["balance"],
                    location=data["location"],
                    contact_number=data["contact_number"],
                    discount_program=data["discount_program"],
                    owner=data["owner"],
                    updated_at=timezone.now()

                )
            else:
                Dealership.objects.filter(name=data["name"]).update(
                    name=data["name"],
                    brand=data["brand"],
                    location=data["location"],
                    contact_number=data["contact_number"],
                    discount_program=data["discount_program"],
                    updated_at=timezone.now()
                )
            return Response(
                {"success": "Dealership update successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when updating dealership"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validation_values(self, data):
        name = data.get("name")
        brand = data.get("brand")
        balance = data.get("balance")
        location = data.get("location")
        contact_number = data.get("contact_number")
        discount_program = data.get("discount_program")
        owner = data.get("owner")
        if brand:
            try:
                brand = Brand.objects.get(name=brand)
            except Brand.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {brand}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if location not in dict(countries).values():
            return Response(
                {"error": f"Invalid country {location} "},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if discount_program:
            try:
                discount_program = int(discount_program)
            except:
                return Response(
                    {"error": "Price must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if owner:
            try:
                owner = Customer.objects.get(email=owner)
            except Customer.DoesNotExist:
                return Response(
                    {"error": f"Invalid owner {owner}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "name": name,
            "brand": brand,
            "balance": balance,
            "location": location,
            "contact_number": contact_number,
            "discount_program": discount_program,
            "owner": owner,
        }
        return data

    #         if not Dealership.objects.filter(name=name).exists():
    #             return Response(
    #                 {"error": "Dealership does not exist"},
    #                 status=status.HTTP_404_NOT_FOUND,
    #             )
    #


class DealershipView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            if not Dealership.objects.filter(is_active=True).exists():
                return Response(
                    {"error": "No published dealerships in the database"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            dealership = Dealership.objects.order_by("created_at").filter(
                is_active=True
            )
            dealership = DealershipSerializer(dealership, many=True)

            return Response({"dealership": dealership.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Something went wrong retrieving listing"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ManageBrandView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def get(self, request, format=None):
        brand = Brand.objects.all()
        brand = BrandSerializer(brand, many=True)
        return Response({"Brands": brand.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data

            Brand.objects.create(
                name=data["name"],
            )
            return Response(
                {"success": "Brand created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"error": "Something went wrong when creating brand"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            data = request.data
            brand = Brand.objects.get(name=data["name"])
            brand.is_active = False
            brand.save()
            return Response(
                {"success": "Brand publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"error": "Something went wrong when deleted brand"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ManageModelView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            Model.objects.create(
                name=data["name"],
                brand=data["brand"],
                drivetrain=data["drivetrain"],
                engine=data["engine"],
                bodytype=data["bodytype"],
                transmission=data["transmission"],
            )
            return Response(
                {"success": "Model created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"error": "Something went wrong when creating model"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            if not name:
                return self.get_models(request)
            else:
                return self.get_model(request, name)
        except:
            return Response(
                {"error": "Something went wrong when retrieving models detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_model(self, request, name):
        model = Model.objects.get(name=name)
        model = ModelSerializer(model)
        return Response({"Car": model.data}, status=status.HTTP_200_OK)

    def get_models(self, request):
        models = Model.objects.all()
        models = ModelSerializer(models, many=True)
        return Response({"Cars": models.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            data = request.data
            model = Model.objects.get(name=data["name"])
            model.is_active = False
            model.save()
            return Response(
                {"success": "Model publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when deleted model"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            data = request.data
            data = self.validation_values(data)
            Model.objects.filter(name=data["name"]).update(
                name=data["name"],
                brand=data["brand"],
                drivetrain=data["drivetrain"],
                engine=data["engine"],
                bodytype=data["bodytype"],
                transmission=data["transmission"],
                updated_at=timezone.now(),
            )
            return Response(
                {"success": "Model update successfully"}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"error": "Something went wrong when updating model"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validation_values(self, data):
        name = data["name"]
        brand = data["brand"]
        drivetrain = data["drivetrain"]
        engine = data["engine"]
        bodytype = data["bodytype"]
        transmission = data["transmission"]
        if brand:
            try:
                brand = Brand.objects.get(name=brand)
            except Brand.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {brand}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if drivetrain not in DrivetrainChoices.values:
            return Response(
                {"error": "Invalid drivetrain"}, status=status.HTTP_400_BAD_REQUEST
            )

        if engine not in FuelTypeChoices.values:
            return Response(
                {"error": "Invalid engine"}, status=status.HTTP_400_BAD_REQUEST
            )
        if bodytype not in BodyTypeChoices.values:
            return Response(
                {"error": "Invalid bodytype"}, status=status.HTTP_400_BAD_REQUEST
            )
        if transmission not in TransmissionChoices.values:
            return Response(
                {"error": "Invalid transmission"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "name": name,
            "brand": brand,
            "drivetrain": drivetrain,
            "engine": engine,
            "bodytype": bodytype,
            "transmission": transmission,
        }
        return data


class ManageCarView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            Car.objects.create(
                name=data["name"],
                model=data["model"],
                price=data["price"],
            )
            return Response(
                {"success": "Car created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"error": "Something went wrong when creating car"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            if not name:
                return self.get_cars(request)
            else:
                return self.get_car(request, name)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving cars detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_car(self, request, name):
        car = Car.objects.get(name=name)
        car = CarSerializer(car)
        return Response({"Car": car.data}, status=status.HTTP_200_OK)

    def get_cars(self, request):
        cars = Car.objects.all()
        cars = CarSerializer(cars, many=True)
        return Response({"Car": cars.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            data = request.data
            car = Car.objects.get(name=data["name"])
            car.is_active = False
            car.save()
            return Response(
                {"success": "Car publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"error": "Something went wrong when deleted car"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            data = request.data
            data = self.validation_values(data)
            Car.objects.filter(name=data["name"]).update(
                name=data["name"],
                model=data["model"],
                price=data["price"],
                updated_at=timezone.now(),
            )
            return Response(
                {"success": "Car update successfully"}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"error": "Something went wrong when updating car"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validation_values(self, data):
        name = data["name"]
        model = data["model"]
        price = data["price"]
        if model:
            try:
                model = Model.objects.get(name=model)
            except Brand.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {model}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "name": name,
            "model": model,
            "price": price,
        }
        return data
