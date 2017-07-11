from django_filters.widgets import RangeWidget
from django_filters import filters
import django_filters
from django.db.models import Q
from common.utilities.filters import NumericInFilter
from .models import Clients, STATUS_CHOICES
from django.contrib.auth.models import Group

class ClientFilter(django_filters.FilterSet):
    # id__in = NumericInFilter(name='id', lookup_expr='in')
    # q = django_filters.CharFilter(
    #     method='search',
    #     label='Search',
    # )
    email = django_filters.CharFilter(
        lookup_expr=['exact', 'iexact'],
        label = 'Email',
    )
    first_name = django_filters.CharFilter(
        lookup_expr=['exact', 'iexact'],
        label = 'First Name',
    )
    status = django_filters.MultipleChoiceFilter(
        choices=STATUS_CHOICES,
        label='Status',
    )
    phone_number = django_filters.NumberFilter(
        label='Phone_number',
    )
    groups = django_filters.ModelMultipleChoiceFilter(
        name='attr__name',
        to_field_name='name',
        queryset=Group.objects.all(),
        label='Group',
    )

    class Meta:
        model = Clients
        fields = []

    # def search(self, queryset, name, value):
    #     if not value.strip():
    #         return queryset
    #     return queryset.filter(
    #         Q(id__icontains=value) |
    #         Q(email__icontains=value) |
    #         Q(phone_number__icontains=value)
    #     )