from dealership.models import Dealership
from django.db.models import Sum, Count


def get_dealership(id):
    return Dealership.objects.get(id=id)


def get_statistic(dealership):
    dealership_with_stats = Dealership.objects.annotate(
        car_sales=Count('buyinghistorycustomer'),
        total_profit=Sum('buyinghistorycustomer__price'),
        unique_customers=Count(
            'buyinghistorycustomer__customer',
            distinct=True)
    ).get(name=dealership.name)

    return {
        'cars': dealership_with_stats.car_sales,
        'totally_profit': dealership_with_stats.total_profit,
        'number_unique': dealership_with_stats.unique_customers
    }
