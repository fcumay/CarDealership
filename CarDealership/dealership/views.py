from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
from .permissions import CanModifyDealership, IsAdminOrReadOnly
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
            return [CanModifyDealership()]
        elif self.request.method == "POST":
            return [IsAdminUser()]
        elif self.request.method == "PUT":
            return [CanModifyDealership()]
        elif self.request.method == "DELETE":
            return [CanModifyDealership()]
        return super().get_permissions()

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            brand = request.query_params.get("brand")
            balance = request.query_params.get("balance")
            location = request.query_params.get("location")
            contact_number = request.query_params.get("contact_number")
            discount_program = request.query_params.get("discount_program")
            owner = request.query_params.get("owner")
            data = self.valid_data(
                name, brand, balance, location, contact_number, discount_program, owner
            )
            if data:
                dealerships = self.get_set(
                    data["name"],
                    data["brand"],
                    data["balance"],
                    data["location"],
                    data["contact_number"],
                    data["discount_program"],
                    data["owner"],
                )
                if request.user.role == RoleChoices.is_dealership_admin:
                    dealerships = dealerships.filter(owner=request.user)
                dealerships = DealershipSerializer(dealerships, many=True)
                return Response(
                    {"Dealerships": dealerships.data}, status=status.HTTP_200_OK
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when retrieving dealerships detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_set(
            self,
            name=None,
            brand=None,
            balance=None,
            location=None,
            contact_number=None,
            discount_program=None,
            owner=None,
    ):
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
            name = data["name"]
            brand = data["brand"]
            balance = data["balance"]
            location = data["location"]
            contact_number = data["contact_number"]
            discount_program = data["discount_program"]
            owner = data["owner"]
            data = self.valid_data(
                name, brand, balance, location, contact_number, discount_program, owner
            )
            if data:
                Dealership.objects.create(
                    name=data["name"],
                    brand=data["brand"],
                    balance=data["balance"],
                    location=data["location"],
                    contact_number=data["contact_number"],
                    discount_program=data["discount_program"],
                    owner=data["owner"],
                )
                return Response(
                    {"success": "Dealership created successfully"},
                    status=status.HTTP_201_CREATED,
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when creating dealership"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            name = request.data.get("name")
            brand = request.data.get("brand")
            balance = request.data.get("balance")
            location = request.data.get("location")
            contact_number = request.data.get("contact_number")
            discount_program = request.data.get("discount_program")
            owner = request.data.get("owner")
            data = self.valid_data(
                name, brand, balance, location, contact_number, discount_program, owner
            )
            dealerships = self.get_set(
                data["name"],
                data["brand"],
                data["balance"],
                data["location"],
                data["contact_number"],
                data["discount_program"],
                data["owner"],
            )
            for dealership in dealerships:
                try:
                    self.check_object_permissions(request, dealership)
                    dealership.is_active = False
                    dealership.save()
                except BaseException:
                    continue

            return Response(
                {"success": "Dealership publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when deleted dealership"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            name = request.query_params.get("name")
            brand = request.query_params.get("brand")
            balance = request.query_params.get("balance")
            location = request.query_params.get("location")
            contact_number = request.query_params.get("contact_number")
            discount_program = request.query_params.get("discount_program")
            owner = request.query_params.get("owner")
            data = self.valid_data(
                name, brand, balance, location, contact_number, discount_program, owner
            )
            if data:
                dealerships = self.get_set(
                    data["name"],
                    data["brand"],
                    data["balance"],
                    data["location"],
                    data["contact_number"],
                    data["discount_program"],
                    data["owner"],
                )

                name = request.data.get("name")
                brand = request.data.get("brand")
                balance = request.data.get("balance")
                location = request.data.get("location")
                contact_number = request.data.get("contact_number")
                discount_program = request.data.get("discount_program")
                owner = request.data.get("owner")
                data = self.valid_data(
                    name,
                    brand,
                    balance,
                    location,
                    contact_number,
                    discount_program,
                    owner,
                )
                for dealership in dealerships:
                    try:
                        self.check_object_permissions(request, dealership)
                        if data["name"]:
                            dealership.name = data["name"]
                        if data["brand"]:
                            dealership.brand = data["brand"]
                        if data["location"]:
                            dealership.location = data["location"]
                        if data["contact_number"]:
                            dealership.contact_number = data["contact_number"]
                        if data["discount_program"]:
                            dealership.discount_program = data["discount_program"]
                        dealership.update_at = timezone.now()
                        if request.user.role == RoleChoices.is_superuser:
                            if data["balance"]:
                                dealership.balance = data["balance"]
                            if data["owner"]:
                                dealership.owner = data["owner"]

                        dealership.save()
                    except BaseException:
                        continue
                return Response(
                    {"success": "Dealership update successfully"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when updating dealership"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def valid_data(
            self, name, brand, balance, location, contact_number, discount_program, owner
    ):
        if brand:
            try:
                brand = Brand.objects.get(name=brand)
            except Brand.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {brand}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if location:
            if location not in dict(countries).values():
                return Response(
                    {"error": f"Invalid country {location} "},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if discount_program:
            try:
                discount_program = int(discount_program)
            except BaseException:
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
        return {
            "name": name,
            "brand": brand,
            "balance": balance,
            "location": location,
            "contact_number": contact_number,
            "discount_program": discount_program,
            "owner": owner,
        }

    def get_values(self, data):
        name = data.get("name")
        brand = data.get("brand")
        balance = data.get("balance")
        location = data.get("location")
        contact_number = data.get("contact_number")
        discount_program = data.get("discount_program")
        owner = data.get("owner")
        if self.valid_data(
                name, brand, balance, location, contact_number, discount_program, owner
        ):
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


class ManageBrandView(APIView):
    permission_classes = [
        IsAdminOrReadOnly,
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
        except BaseException:
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
        except BaseException:
            return Response(
                {"error": "Something went wrong when deleted brand"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ManageModelView(APIView):
    permission_classes = [
        IsAdminOrReadOnly,
    ]

    def post(self, request):
        try:
            data = request.data
            name = data["name"]
            brand = data["brand"]
            drivetrain = data["drivetrain"]
            engine = data["engine"]
            bodytype = data["bodytype"]
            transmission = data["transmission"]
            data = self.valid_data(
                name, brand, drivetrain, engine, bodytype, transmission
            )

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
        except BaseException:
            return Response(
                {"error": "Something went wrong when creating model"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_set(
            self,
            name=None,
            brand=None,
            drivetrain=None,
            engine=None,
            bodytype=None,
            transmission=None,
    ):
        criteria = Q()
        if name:
            criteria &= Q(name=name)
        if brand:
            criteria &= Q(brand=brand)
        if drivetrain:
            criteria &= Q(balance=drivetrain)
        if engine:
            criteria &= Q(location=engine)
        if bodytype:
            criteria &= Q(contact_number=bodytype)
        if transmission:
            criteria &= Q(discount_program=transmission)
        models = Model.objects.filter(criteria)
        return models

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            brand = request.query_params.get("brand")
            drivetrain = request.query_params.get("drivetrain")
            engine = request.query_params.get("engine")
            bodytype = request.query_params.get("bodytype")
            transmission = request.query_params.get("transmission")
            data = self.valid_data(
                name, brand, drivetrain, engine, bodytype, transmission
            )
            if data:
                models = self.get_set(
                    data["name"],
                    data["brand"],
                    data["drivetrain"],
                    data["engine"],
                    data["bodytype"],
                    data["transmission"],
                )
                models = ModelSerializer(models, many=True)
                return Response({"Models": models.data},
                                status=status.HTTP_200_OK)
        except BaseException:
            return Response(
                {"error": "Something went wrong when retrieving models detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            name = request.data.get("name")
            brand = request.data.get("brand")
            drivetrain = request.data.get("drivetrain")
            engine = request.data.get("engine")
            bodytype = request.data.get("bodytype")
            transmission = request.data.get("transmission")
            data = self.valid_data(
                name, brand, drivetrain, engine, bodytype, transmission
            )
            if data:
                models = self.get_set(
                    data["name"],
                    data["brand"],
                    data["drivetrain"],
                    data["engine"],
                    data["bodytype"],
                    data["transmission"],
                )
            for model in models:
                model.is_active = False
                model.save()

            return Response(
                {"success": "Model publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when deleted model"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            name = request.query_params.get("name")
            brand = request.query_params.get("brand")
            drivetrain = request.query_params.get("drivetrain")
            engine = request.query_params.get("engine")
            bodytype = request.query_params.get("bodytype")
            transmission = request.query_params.get("transmission")
            data = self.valid_data(
                name, brand, drivetrain, engine, bodytype, transmission
            )
            if data:
                models = self.get_set(
                    data["name"],
                    data["brand"],
                    data["drivetrain"],
                    data["engine"],
                    data["bodytype"],
                    data["transmission"],
                )

            name = request.data.get("name")
            brand = request.data.get("brand")
            drivetrain = request.data.get("drivetrain")
            engine = request.data.get("engine")
            bodytype = request.data.get("bodytype")
            transmission = request.data.get("transmission")
            data = self.valid_data(
                name, brand, drivetrain, engine, bodytype, transmission
            )

            for model in models:
                if data["name"]:
                    model.name = data["name"]
                if data["brand"]:
                    model.brand = data["brand"]
                if data["drivetrain"]:
                    model.drivetrain = data["drivetrain"]
                if data["engine"]:
                    model.engine = data["engine"]
                if data["bodytype"]:
                    model.bodytype = data["bodytype"]
                if data["transmission"]:
                    model.transmission = data["transmission"]
                model.update_at = timezone.now()
                model.save()
                return Response(
                    {"success": "Model update successfully"}, status=status.HTTP_200_OK
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when updating model"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def valid_data(self, name, brand, drivetrain,
                   engine, bodytype, transmission):
        if brand:
            try:
                brand = Brand.objects.get(name=brand)
            except Brand.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {brand}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if drivetrain:
            if drivetrain not in DrivetrainChoices.values:
                return Response(
                    {"error": "Invalid drivetrain"}, status=status.HTTP_400_BAD_REQUEST
                )
        if engine:
            if engine not in FuelTypeChoices.values:
                return Response(
                    {"error": "Invalid engine"}, status=status.HTTP_400_BAD_REQUEST
                )
        if bodytype:
            if bodytype not in BodyTypeChoices.values:
                return Response(
                    {"error": "Invalid bodytype"}, status=status.HTTP_400_BAD_REQUEST
                )
        if transmission:
            if transmission not in TransmissionChoices.values:
                return Response(
                    {"error": "Invalid transmission"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return {
            "name": name,
            "brand": brand,
            "drivetrain": drivetrain,
            "engine": engine,
            "bodytype": bodytype,
            "transmission": transmission,
        }


class ManageCarView(APIView):
    permission_classes = [
        IsAdminOrReadOnly,
    ]

    def post(self, request):
        try:
            data = request.data
            name = data["name"]
            model = data["model"]
            price = data["price"]
            data = self.valid_data(name, model, price)

            Car.objects.create(
                name=data["name"],
                model=data["model"],
                price=data["price"],
            )
            return Response(
                {"success": "Car created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when creating car"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_set(
            self,
            name=None,
            model=None,
            price=None,
    ):
        criteria = Q()
        if name:
            criteria &= Q(name=name)
        if model:
            criteria &= Q(model=model)
        if price:
            criteria &= Q(price=price)
        cars = Car.objects.filter(criteria)
        return cars

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            model = request.query_params.get("model")
            price = request.query_params.get("price")
            data = self.valid_data(name, model, price)
            if data:
                cars = self.get_set(
                    data["name"],
                    data["model"],
                    data["price"],
                )
                cars = CarSerializer(cars, many=True)
                return Response({"Cars": cars.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving cars detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            name = request.data.get("name")
            model = request.data.get("model")
            price = request.data.get("price")
            data = self.valid_data(name, model, price)
            if data:
                cars = self.get_set(
                    data["name"],
                    data["model"],
                    data["price"],
                )
            for car in cars:
                try:
                    car.is_active = False
                    car.save()
                except BaseException:
                    continue
            return Response(
                {"success": "Car publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when deleted car"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            name = request.query_params.get("name")
            model = request.query_params.get("model")
            price = request.query_params.get("price")
            data = self.valid_data(name, model, price)
            if data:
                cars = self.get_set(
                    data["name"],
                    data["model"],
                    data["price"],
                )

            name = request.data.get("name")
            model = request.data.get("model")
            price = request.data.get("price")
            data = self.valid_data(name, model, price)

            for car in cars:
                if data["name"]:
                    car.name = data["name"]
                if data["model"]:
                    car.model = data["model"]
                if data["price"]:
                    car.price = data["price"]
                car.update_at = timezone.now()
                car.save()
            return Response(
                {"success": "Car update successfully"}, status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when updating car"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def valid_data(self, name, model, price):
        if model:
            try:
                model = Model.objects.get(name=model)
            except Model.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {model}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return {
            "name": name,
            "model": model,
            "price": price,
        }
