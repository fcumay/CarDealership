from django_countries import countries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dealer.models import Dealer, DealerInventory

from dealer.serializers import (
    DealerSerializer,
    DealerInventorySerializer,
)
from dealership.models import Model
from django.utils import timezone
from django.db.models import Q

from dealer.permissions import IsAdminOrReadOnly


class ManageDealerView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def post(self, request):
        try:
            data = request.data
            name = data["name"]
            amount_of_client = data["amount_of_client"]
            location = data["location"]
            contact_number = data["contact_number"]
            discount_program = data["discount_program"]
            data = self.valid_data(
                name, amount_of_client, location, contact_number, discount_program
            )

            if data:
                Dealer.objects.create(
                    name=data["name"],
                    amount_of_client=data["amount_of_client"],
                    location=data["location"],
                    contact_number=data["contact_number"],
                    discount_program=data["discount_program"],
                )
                return Response(
                    {"success": "Dealer created successfully"},
                    status=status.HTTP_201_CREATED,
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when creating dealer detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_set(
            self,
            name=None,
            amount_of_client=None,
            location=None,
            contact_number=None,
            discount_program=None,
    ):
        criteria = Q()
        if name:
            criteria &= Q(name=name)
        if amount_of_client:
            criteria &= Q(amount_of_client=amount_of_client)
        if location:
            criteria &= Q(location=location)
        if contact_number:
            criteria &= Q(contact_number=contact_number)
        if discount_program:
            criteria &= Q(discount_program=discount_program)
        dealers = Dealer.objects.filter(criteria)
        return dealers

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            amount_of_client = request.query_params.get("amount_of_client")
            location = request.query_params.get("location")
            contact_number = request.query_params.get("contact_number")
            discount_program = request.query_params.get("discount_program")
            data = self.valid_data(
                name, amount_of_client, location, contact_number, discount_program
            )
            if data:
                dealers = self.get_set(
                    data["name"],
                    data["amount_of_client"],
                    data["location"],
                    data["contact_number"],
                    data["discount_program"],
                )
            dealers = DealerSerializer(dealers, many=True)
            return Response({"Dealers": dealers.data},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response(
                {"error": "Something went wrong when retrieving dealer detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            name = request.data.get("name")
            amount_of_client = request.data.get("amount_of_client")
            location = request.data.get("location")
            contact_number = request.data.get("contact_number")
            discount_program = request.data.get("discount_program")
            data = self.valid_data(
                name, amount_of_client, location, contact_number, discount_program
            )
            if data:
                dealers = self.get_set(
                    data["name"],
                    data["amount_of_client"],
                    data["location"],
                    data["contact_number"],
                    data["discount_program"],
                )
                for dealer in dealers:
                    dealer.is_active = False
                    dealer.save()

                return Response(
                    {"success": "Dealer publish status deleted successfully"},
                    status=status.HTTP_200_OK,
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when deleted dealer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            name = request.query_params.get("name")
            amount_of_client = request.query_params.get("amount_of_client")
            location = request.query_params.get("location")
            contact_number = request.query_params.get("contact_number")
            discount_program = request.query_params.get("discount_program")
            data = self.valid_data(
                name, amount_of_client, location, contact_number, discount_program
            )
            if data:
                dealers = self.get_set(
                    data["name"],
                    data["amount_of_client"],
                    data["location"],
                    data["contact_number"],
                    data["discount_program"],
                )
                name = request.data.get("name")
                amount_of_client = request.data.get("amount_of_client")
                location = request.data.get("location")
                contact_number = request.data.get("contact_number")
                discount_program = request.data.get("discount_program")
                data = self.valid_data(
                    name, amount_of_client, location, contact_number, discount_program
                )
                for dealer in dealers:
                    if data["name"]:
                        dealer.name = data["name"]
                    if data["amount_of_client"]:
                        dealer.amount_of_client = data["amount_of_client"]
                    if data["location"]:
                        dealer.location = data["location"]
                    if data["contact_number"]:
                        dealer.contact_number = data["contact_number"]
                    if data["discount_program"]:
                        dealer.discount_program = data["discount_program"]
                    dealer.update_at = timezone.now()
                    dealer.save()

                return Response(
                    {"success": "Dealer update successfully"}, status=status.HTTP_200_OK
                )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when updating dealer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def valid_data(
            self, name, amount_of_client, location, contact_number, discount_program
    ):
        if location:
            for code, country in countries:
                if country == location:
                    location = code
                    break

        if discount_program:
            try:
                discount_program = int(discount_program)
            except BaseException:
                return Response(
                    {"error": "Price must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return {
            "name": name,
            "amount_of_client": amount_of_client,
            "location": location,
            "contact_number": contact_number,
            "discount_program": discount_program,
        }


class ManageDealerInventoryView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_set(
            self,
            dealer=None,
            model=None,
            price=None,
    ):
        criteria = Q()
        if dealer:
            criteria &= Q(dealer=dealer)
        if model:
            criteria &= Q(model=model)
        if price:
            criteria &= Q(price=price)
        iventories = DealerInventory.objects.filter(criteria)
        return iventories

    def get(self, request, format=None):
        try:
            dealer = request.query_params.get("dealer")
            model = request.query_params.get("model")
            price = request.query_params.get("price")
            data = self.valid_data(dealer, model, price)
            if data:
                inventories = self.get_set(
                    data["dealer"],
                    data["model"],
                    data["price"],
                )
            inventories = DealerInventorySerializer(inventories, many=True)
            return Response(
                {"Inventories": inventories.data}, status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when retrieving inventory detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            data = request.data
            dealer = data["dealer"]
            model = data["model"]
            price = data["price"]
            data = self.valid_data(dealer, model, price)

            if data:
                DealerInventory.objects.create(
                    dealer=data["dealer"],
                    model=data["model"],
                    price=data["price"],
                )
            return Response(
                {"success": "Dealer Inventory updated successfully"},
                status=status.HTTP_201_CREATED,
            )
        except BaseException:
            return Response(
                {"error": "Something went wrong when updating dealer inventory "},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            dealer = request.query_params.get("dealer")
            model = request.query_params.get("model")
            price = request.query_params.get("price")
            data = self.valid_data(dealer, model, price)
            if data:
                inventories = self.get_set(
                    data["dealer"],
                    data["model"],
                    data["price"],
                )
                for inventory in inventories:
                    inventory.is_active = False
                    inventory.save()

                return Response(
                    {"success": "inventory publish status deleted successfully"},
                    status=status.HTTP_200_OK,
                )
        except BaseException:
            return Response(
                {"error": "Something went wrong when deleted inventory"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def valid_data(self, dealer, model, price):
        if dealer:
            try:
                dealer = Dealer.objects.get(name=dealer)
            except Dealer.DoesNotExist:
                return Response(
                    {"error": f"Invalid dealer {dealer}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if model:
            try:
                model = Model.objects.get(name=model)
            except Model.DoesNotExist:
                return Response(
                    {"error": f"Invalid model {model}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return {
            "dealer": dealer,
            "model": model,
            "price": price,
        }
