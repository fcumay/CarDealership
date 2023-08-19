from customer.models import BuyingHistoryCustomer
from dealership.models import Dealership
from django.db.models import Sum
from django.db.models import Sum, Count


def get_dealership(name):
    return Dealership.objects.get(name=name)


def get_statistic(dealership):
    dealership_with_stats = Dealership.objects.annotate(
        car_sales=Count('buyinghistorycustomer'),
        total_profit=Sum('buyinghistorycustomer__price'),
        unique_customers=Count(
            'buyinghistorycustomer__customer',
            distinct=True)
    ).get(name=dealership.name)

    return {
        'Cars': dealership_with_stats.car_sales,
        'Totally profit': dealership_with_stats.total_profit or 0,
        'Number unique': dealership_with_stats.unique_customers
    }
