import django_filters
from django.db.models import Q
from common.utilities.filters import NumericInFilter
from .models import Products

class ProductFilter(django_filters.FilterSet):
    """product filter set"""
    id__in = NumericInFilter(name='id', lookup_expr='in')
    q = django_filters.CharFilter(
        method = 'search',
        label = 'Search',
    )
    class Meta:
        model = Products
        fields = ['product_name', 'product_type']

    def search(self, queryset, name, value):

        if not value.strip():
            return queryset
        qs_filter = (
            Q(product_name__icontains=value) |
            Q(product_type__icontains=value)
        )
        return queryset.filter(qs_filter)