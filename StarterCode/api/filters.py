import django_filters
from api.models import Product, Order
from rest_framework import filters




# filtro customizado
class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
        # return queryset.exclude(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model=Product
        fields={
            'name':['exact', 'contains'],
            'price':['exact', 'lt', 'gt', 'range'],
        }


class OrderFilter(django_filters.FilterSet):
    # filtra as datas por dd/mm/aaaa envez da datetime completo
    # sobreescreve o campo de create_at 
    # create_at__date extrai a data do datetime
    create_at = django_filters.DateFilter(field_name='create_at__date')
    class Meta:
        model=Order
        fields={
            'status':['exact'],
            'create_at':['lt','gt','exact'],
        }