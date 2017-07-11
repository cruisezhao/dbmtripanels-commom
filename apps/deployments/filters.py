import django_filters
from .models import SystemOptions

class SysOptionFilterForm(django_filters.FilterSet):
    name = django_filters.CharFilter(
        name='name',
        lookup_expr='exact'
    )
    value = django_filters.CharFilter(
        name='name',
        lookup_expr='exact'
    )

    start_date = django_filters.DateFilter(name='created', lookup_expr='gte')
    end_date = django_filters.DateFilter(name='created', lookup_expr='lte')
    class Meta:
        model = SystemOptions
        fields = ['name']