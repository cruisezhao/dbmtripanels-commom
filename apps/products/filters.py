from django_filters.widgets import RangeWidget
from django_filters import filters
import django_filters
from django.db.models import Q
from common.utilities.filters import NumericInFilter
from .models import Products, Plans

class ProductFilter(django_filters.FilterSet):
    """product filter set"""
    name = django_filters.CharFilter(
        name='product_name',
        lookup_expr='exact'
    )

    plan = django_filters.ModelMultipleChoiceFilter(
        name='plans__pk',
        queryset=Plans.objects.all(),
        to_field_name='pk',
        label='name',
    )

    type = django_filters.MultipleChoiceFilter(
        name='product_type',
        choices=Products.TYPE_CHOICE,
    )
    # date = django_filters.DateFromToRangeFilter(
    #     name = "created",
    #     widget=RangeWidget(attrs={'display':'inline'}),
    # )
    start_date = filters.DateFilter(name='created', lookup_expr='gte')
    end_date = filters.DateFilter(name='created', lookup_expr='lte')
    q = django_filters.CharFilter(
        method = 'search',
        label = 'Search',
    )
    class Meta:
        model = Products
        fields = ['start_date', 'end_date']

    def search(self, queryset, name, value):

        if not value.strip():
            return queryset
        qs_filter = (
            Q(product_name__icontains=value) |
            Q(product_type__icontains=value)
        )
        return queryset.filter(qs_filter)