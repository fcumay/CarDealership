from .models import Dealership, Car
from celery import shared_task
from dealer.models import DealerInventory, PromotionDealer, BuyingHistoryDealer
from customer.models import BuyingHistoryCustomer, Customer
from CarDealership.celery import app
from django.db.models import Count, Subquery, OuterRef, F, Case, When, Value, DecimalField, IntegerField
from django.db import transaction
from datetime import datetime


class DealershipManager():
    def __init__(self):
        self.dealers_inventory = list()
        self.get_dealers()

    def get_dealers(self):
        current_time = datetime.now()
        print(f'\n*** Start get_dealers***\n')
        print(f'\n***current_time - {current_time}***\n')

        dealership_brands = Dealership.objects.values('brand')
        print(f'\n*** Dealership brands{dealership_brands}***\n')
        popular_models = BuyingHistoryCustomer.objects.select_related('car').values('car__model',
                                                                                    'car__model__brand').annotate(
            model_count=Count('car__model')).order_by('-model_count')
        dealers_inventory = DealerInventory.objects.filter(
            model__in=popular_models.values('car__model'),
            model__brand__in=dealership_brands
        ).annotate(
            model_rank=Case(
                *[
                    When(model=model, then=Value(rank))
                    for rank, model in enumerate(popular_models.values_list('car__model', flat=True), start=1)
                ],
                default=Value(len(popular_models) + 1),
                output_field=IntegerField()
            )
        ).annotate(
            promotion_percentage=Subquery(
                PromotionDealer.objects.filter(
                    dealer=OuterRef('dealer'),
                    model=OuterRef('model'),
                    date_start__lte=current_time,
                    date_finish__gte=current_time
                ).values('percentage')[:1]
            )
        ).annotate(
            discounted_price=Case(
                When(promotion_percentage__isnull=False, then=F('price') * (1 - F('promotion_percentage') / 100.0)),
                default=F('price') * (1 - F('dealer__discount_program') / 100.0),
                output_field=DecimalField()
            )
        ).order_by('model_rank', 'discounted_price').values('dealer', 'model', 'discounted_price', 'model__brand__name')

        unique_models = {}
        for item in dealers_inventory:
            model = item['model']
            if model not in unique_models or item['discounted_price'] < unique_models[model]['discounted_price']:
                unique_models[model] = item

        self.dealers_inventory = list(unique_models.values())
        print(f'\n*** dealers_inventory: {self.dealers_inventory}***\n')

    def buy_car(self):
        print(f'\n***Ibuy_car: {self.dealers_inventory}***\n')
        car_number = Car.objects.count()
        dealerships = Dealership.objects.all()
        cars_to_create = []
        histories_to_create = []
        for dealership in dealerships:
            targets = [item for item in self.dealers_inventory if item["model__brand__name"] == dealership.brand.name]
            balance = dealership.balance
            print(f'\n***targets: {targets}***\n')
            for target in targets:
                if balance != 0 and target["discounted_price"] <= balance:
                    car_number += 1
                    car = Car(
                        name=f"{dealership.brand.name}_{car_number}",
                        model_id=target["model"],
                        dealership=dealership,
                        price=target["discounted_price"] + 10
                    )
                    print(f'\n***Create car: {car}***\n')
                    cars_to_create.append(car)
                    history = BuyingHistoryDealer(
                        dealership=dealership,
                        dealer_id=target['dealer'],
                        car=car,
                        price=target['discounted_price']
                    )
                    print(f'\n***Create history: {history}***\n')
                    histories_to_create.append(history)
                    balance -= target['discounted_price']
            dealership.balance = balance
            dealership.save()
        with transaction.atomic():
            Car.objects.bulk_create(cars_to_create)
            BuyingHistoryDealer.objects.bulk_create(histories_to_create)


manager = DealershipManager()


@shared_task
def buy_car():
    manager.buy_car()


@shared_task
def get_dealers():
    manager.get_dealers()


@app.task()
def do_offer(user, data):
    customer = Customer.objects.get(id=user)
    car = Car.objects.select_related('dealership').filter(model__name=data['model'], is_active=True,
                                                          price__lte=data['price']).order_by(
        'price').first()
    print(f'\n***Car: {car}***\n')
    price = car.price * (1 - car.dealership.discount_program / 100)
    if customer.balance >= price:
        BuyingHistoryCustomer.objects.create(
            customer=customer,
            dealership=car.dealership,
            car=car,
            price=price
        )
        car.dealership = None
        car.customer = customer
        car.is_active = False
        car.save()
        customer.balance -= price
        customer.save()
    return True
