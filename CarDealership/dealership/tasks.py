from .models import Dealership, Car
from celery import shared_task
from dealer.models import DealerInventory, PromotionDealer, BuyingHistoryDealer, PromotionDealership, Dealer
from customer.models import BuyingHistoryCustomer, Customer
from CarDealership.celery import app
from django.db.models import Count, DecimalField, IntegerField
from django.db import transaction
from datetime import datetime
from django.db.models import Subquery, OuterRef, Case, When, F, Value
import logging

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DealershipManager:
    def __init__(self):
        self.dealers_inventory = self.get_dealers()

    def get_dealers(self):
        current_time = datetime.now()

        dealership_brands = Dealership.objects.values('brand')

        popular_models = BuyingHistoryCustomer.objects.select_related('car').values('car__model',
                                                                                    'car__model__brand').annotate(
            model_count=Count('car__model')).order_by('-model_count')
        dealer_inventory = DealerInventory.objects.annotate(
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
                When(promotion_percentage__isnull=False, then=F(
                    'price') * (1 - F('promotion_percentage') / 100.0)),
                default=F('price') *
                (1 - F('dealer__discount_program') / 100.0),
                output_field=DecimalField()
            )
        ).annotate(
            model_rank=Case(
                *[
                    When(model=model, then=Value(rank))
                    for rank, model in enumerate(popular_models.values_list('car__model', flat=True), start=1)
                ],
                default=Value(len(popular_models) + 1),
                output_field=IntegerField()
            )
        ).values('dealer', 'model', 'discounted_price', 'model__brand__name').order_by('model_rank', 'discounted_price')
        self.dealers_inventory = dealer_inventory
        logging.info('get_dealers: Dealers retrieved successfully.')
        return dealer_inventory

    def buy_car(self):
        car_number = Car.objects.count()
        dealerships = Dealership.objects.all()
        for dealership in dealerships:
            cars_to_create = []
            histories_to_create = []
            balance = dealership.balance
            targets = []
            models = set()
            for item in self.dealers_inventory:
                model = item["model"]
                brand_name = item["model__brand__name"]
                if model not in models and brand_name == dealership.brand.name:
                    targets.append(item)
                    models.add(model)
            if len(targets) != 0:
                for target in targets:
                    if balance != 0 and target["discounted_price"] <= balance:
                        car_number += 1
                        car = Car(
                            name=f"{dealership.brand.name}_{str(target['model'])}_{car_number}",
                            model_id=target["model"],
                            dealership=dealership,
                            price=target["discounted_price"] + 10
                        )
                        cars_to_create.append(car)
                        history = BuyingHistoryDealer(
                            dealership=dealership,
                            dealer_id=target['dealer'],
                            car=car,
                            price=target['discounted_price']
                        )
                        histories_to_create.append(history)
                        balance -= target['discounted_price']
                        dealer = Dealer.objects.get(id=target['dealer'])
                        dealer.amount_of_client += 1
                        dealer.save()
                logging.info(
                    f'buy_car: Bought {len(cars_to_create)} cars for dealership {dealership.id}.')
                dealership.balance = balance
                dealership.save()
                with transaction.atomic():
                    Car.objects.bulk_create(cars_to_create)
                    BuyingHistoryDealer.objects.bulk_create(
                        histories_to_create)
                    logging.info(
                        'buy_car: Cars and histories created successfully.')


manager = DealershipManager()


@shared_task
def buy_car():
    logging.info('buy_car task started.')
    manager.buy_car()
    logging.info('buy_car task completed.')


@shared_task
def get_dealers():
    logging.info('get_dealers task started.')
    manager.get_dealers()
    logging.info('get_dealers task completed.')


@app.task()
def do_offer(user, data):
    logging.info(f'do_offer: Processing offer for user {user} and data {data}')
    customer = Customer.objects.get(id=user)
    car = Car.objects.filter(is_active=True, model__name=data['model']).annotate(
        discounted_price=Case(
            When(dealership__discount_program__isnull=False,
                 then=F('price') * (1 - F('dealership__discount_program') / 100.0)),
            default=F('price'),
            output_field=DecimalField()
        )
    ).annotate(
        promotion_discount=Subquery(
            PromotionDealership.objects.filter(
                dealership=OuterRef('dealership'),
                model=OuterRef('model'),
            ).values('percentage')[:1]
        )
    ).annotate(
        final_price=Case(
            When(promotion_discount__isnull=False, then=F(
                'discounted_price') * (1 - F('promotion_discount') / 100.0)),
            default=F('discounted_price'),
            output_field=DecimalField()
        )
    ).order_by('final_price').first()
    if customer.balance >= car.final_price and data["price"] >= car.final_price:
        car.dealership.balance += car.final_price
        car.dealership.save()
        BuyingHistoryCustomer.objects.create(
            customer=customer,
            dealership=car.dealership,
            car=car,
            price=car.final_price
        )
        car.dealership = None
        car.customer = customer
        car.is_active = False
        car.save()
        customer.balance -= car.final_price
        customer.save()
