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
    class Meta:
        model = SystemOptions
        fields = ['name']