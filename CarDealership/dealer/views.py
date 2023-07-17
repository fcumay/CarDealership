from django_countries import countries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from customer.models import RoleChoices
from dealer.models import Dealer, DealerInventory, PromotionDealership, PromotionDealer
from dealer.permissions import CanCreateDealershipPromotion
from dealer.serializers import DealerSerializer, DealerInventorySerializer, PromotionDealershipSerializer, \
    PromotionDealerSerializer
from dealership.models import Model, Dealership
from django.utils import timezone


class ManageDealerView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            if not name:
                return self.get_dealers(request)
            else:
                return self.get_dealer(request, name)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving dealer detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_dealer(self, request, name):
        dealer = Dealer.objects.get(name=name)
        dealer = DealerSerializer(dealer)
        return Response({"dealer": dealer.data}, status=status.HTTP_200_OK)

    def get_dealers(self, request):
        dealers = Dealer.objects.all()
        dealers = DealerSerializer(dealers, many=True)
        return Response({"dealer": dealers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

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
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when creating dealer detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            data = request.data
            name = data["name"]
            dealer = Dealer.objects.get(name=name)
            dealer.is_active = False
            dealer.save()
            return Response(
                {"success": "Dealer publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(

                {"error": "Something went wrong when deleted dealer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            Dealer.objects.filter(name=data["name"]).update(
                name=data["name"],
                amount_of_client=data["amount_of_client"],
                location=data["location"],
                contact_number=data["contact_number"],
                discount_program=data["discount_program"],
                updated_at=timezone.now()
            )

            return Response(
                {"success": "Dealer update successfully"}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"error": "Something went wrong when updating dealer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validation_values(self, data):

        name = data["name"]
        amount_of_client = data["amount_of_client"]
        location = data["location"]
        contact_number = data["contact_number"]
        discount_program = data["discount_program"]

        for code, country in countries:
            if country == location:
                location = code
                break

        if discount_program:
            try:
                discount_program = int(discount_program)
            except:
                return Response(
                    {"error": "Price must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "name": name,
            "amount_of_client":amount_of_client,
            "location": location,
            "contact_number": contact_number,
            "discount_program": discount_program,
        }
        return data

class ManageDealerInventoryView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        try:
            dealer = request.query_params.get("dealer")
            if not dealer:
                return self.get_inventories(request)
            else:
                return self.get_inventory(request, dealer)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving dealer detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_inventory(self, request, dealer):
        inventory = DealerInventory.objects.get(dealer=dealer)
        inventory = DealerInventorySerializer(inventory)
        return Response({"Inventory": inventory.data}, status=status.HTTP_200_OK)

    def get_inventories(self, request):
        inventories = DealerInventory.objects.all()
        inventories = DealerInventorySerializer(inventories, many=True)
        return Response({"inventories": inventories.data}, status=status.HTTP_200_OK)
    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            DealerInventory.objects.create(
                dealer=data["dealer"],
                model=data["model"],
                price=data["price"],
            )
            return Response(
                {"success": "Dealer Inventory updated successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when updating dealer inventory "},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    def delete(self, request):
        try:
            data = request.data
            id = data["id"]
            inventory = DealerInventory.objects.get(id=id)
            inventory.is_active = False
            inventory.save()
            return Response(
                {"success": "inventory publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(

                {"error": "Something went wrong when deleted inventory"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validation_values(self, data):

        dealer = data["dealer"]
        model = data["model"]
        price = data["price"]
        print(f'Dealer {dealer}')

        try:
            dealer = Dealer.objects.get(name=dealer)
        except Dealer.DoesNotExist:
            return Response(
                {"error": f"Invalid dealer {dealer}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            model = Model.objects.get(name=model)
        except Model.DoesNotExist:
            return Response(
                {"error": f"Invalid model {model}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "dealer": dealer,
            "model":model,
            "price": price,
        }
        return data

class ManagePromotionDealersipView(APIView):
    permission_classes = (CanCreateDealershipPromotion,)
    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data,request)

            PromotionDealership.objects.create(
                name=data["name"],
                date_start=data["date_start"],
                date_finish=data["date_finish"],
                description=data["description"],
                percentage=data["percentage"],
                dealership=data["dealership"],
                model = data["model"]
            )
            return Response(
                {"success": "PromotionDealership created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when creating PromotionDealership"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            if not name:
                return self.get_promotions(request)
            else:
                return self.get_promotion(request, name)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving dealerships detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_promotion(self, request, name):
        dealerships = Dealership.objects.filter(owner=request.user)
        promotions_data = []
        for dealership in dealerships:
            promotion = PromotionDealership.objects.filter(dealership=dealership, name=name).first()
            if promotion:
                serializer = PromotionDealershipSerializer(promotion)
                promotions_data.append(serializer.data)
        return Response({"promotions": promotions_data}, status=status.HTTP_200_OK)
    def get_promotions(self, request):
        dealerships = Dealership.objects.filter(owner=request.user)
        promotions_data = []
        for dealership in dealerships:
            promotions = PromotionDealership.objects.filter(dealership=dealership)
            if promotions:
                serializer = PromotionDealershipSerializer(promotions, many=True)
                promotions_data.append(serializer.data)
        return Response({"promotions": promotions_data}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            data = request.data
            name = data["name"]
            promotion = PromotionDealership.objects.get(name=name)
            promotion.is_active = False
            promotion.save()
            return Response(
                {"success": "Promotion publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when deleted promotion"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            data = request.data
            data = self.validation_values(data,request)

            PromotionDealership.objects.filter(name=data["name"]).update(
                name=data["name"],
                date_start=data["date_start"],
                date_finish=data["date_finish"],
                description=data["description"],
                percentage=data["percentage"],
                dealership=data["dealership"],
                model = data["model"],
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
    def validation_values(self, data,request):
        name = data.get("name")
        date_start = data.get("date_start")
        date_finish = data.get("date_finish")
        description = data.get("description")
        percentage = data.get("percentage")
        dealership = data.get("dealership")
        model = data.get("model")
        if dealership:
            try:
                dealership = Dealership.objects.get(name=dealership,owner=request.user)
            except dealership.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {dealership}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if model:
            try:
                model = Model.objects.get(name=model)
            except model.DoesNotExist:
                return Response(
                    {"error": f"Invalid model {model}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "name": name,
            "date_start": date_start,
            "date_finish": date_finish,
            "description": description,
            "percentage": percentage,
            "dealership": dealership,
            "model": model,
        }
        print(name,date_start,date_finish,description,percentage,dealership,model)
        return data


class ManagePromotionDealerView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    def post(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            PromotionDealer.objects.create(
                name=data["name"],
                date_start=data["date_start"],
                date_finish=data["date_finish"],
                description=data["description"],
                percentage=data["percentage"],
                dealer=data["dealer"],
                model = data["model"]
            )
            return Response(
                {"success": "PromotionDealer created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when creating PromotionDealer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    def get(self, request, format=None):
        try:
            name = request.query_params.get("name")
            if not name:
                return self.get_promotions(request)
            else:
                return self.get_promotion(request, name)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when retrieving dealer detail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_promotion(self, request, name):
        promotion = PromotionDealer.objects.get(name=name)
        promotion = PromotionDealerSerializer(promotion)
        return Response({"promotions": promotion.data}, status=status.HTTP_200_OK)
    def get_promotions(self, request):
        promotions = PromotionDealer.objects.all()
        promotions = PromotionDealerSerializer(promotions, many=True)
        return Response({"promotions": promotions.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            data = request.data
            name = data["name"]
            promotion = PromotionDealer.objects.get(name=name)
            promotion.is_active = False
            promotion.save()
            return Response(
                {"success": "Promotion publish status deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when deleted promotion"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            data = request.data
            data = self.validation_values(data)

            PromotionDealer.objects.filter(name=data["name"]).update(
                name=data["name"],
                date_start=data["date_start"],
                date_finish=data["date_finish"],
                description=data["description"],
                percentage=data["percentage"],
                dealer=data["dealer"],
                model = data["model"],
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
        date_start = data.get("date_start")
        date_finish = data.get("date_finish")
        description = data.get("description")
        percentage = data.get("percentage")
        dealer = data.get("dealer")
        model = data.get("model")
        if dealer:
            try:
                dealer = Dealer.objects.get(name=dealer)
            except dealer.DoesNotExist:
                return Response(
                    {"error": f"Invalid brand {dealer}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if model:
            try:
                model = Model.objects.get(name=model)
            except model.DoesNotExist:
                return Response(
                    {"error": f"Invalid model {model}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "name": name,
            "date_start": date_start,
            "date_finish": date_finish,
            "description": description,
            "percentage": percentage,
            "dealer": dealer,
            "model": model,
        }
        print(name,date_start,date_finish,description,percentage,dealer,model)
        return data