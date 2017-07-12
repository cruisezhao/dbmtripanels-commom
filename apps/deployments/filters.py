import django_filters
from .models import (SystemOptions, Clouds, DeployPolicies, DeployInstances,
                    InstanceConfigurations, Questions)
from django import forms
from datetimewidget.widgets import DateWidget

class SysOptionFilter(django_filters.FilterSet):
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


class CloudFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        name='name',
        label = 'Name',
        lookup_expr='exact',
        widget = forms.TextInput(attrs={'class':'TinputText'}))
    start_date = django_filters.DateFilter(
        name='created',
        lookup_expr='gte',
        label = "Start Date",
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    end_date = django_filters.DateFilter(
        name='created',
        lookup_expr='lte',
        label = "End Date",
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )

    class Meta:
        model = Clouds
        fields = ['name','start_date','end_date' ]


class DeployPolicyFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        name="created",
        label = "Start Date",
        lookup_expr='gte',
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
        )

    end_date = django_filters.DateFilter(
        name='created',
        lookup_expr='lte',
        label = "End Date",
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    class Meta:
        model  = DeployPolicies
        fields = ['start_date','end_date']


class DeployInstanceFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        name="created",
        label = "Start Date",
        lookup_expr='gte',
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
        )

    end_date = django_filters.DateFilter(
        name='created',
        lookup_expr='lte',
        label = "End Date",
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )

    class Meta:
        model = DeployInstances
        fields = ['start_date', 'end_date']


class InstanceConfigurationFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        name="created",
        label = "Start Date",
        lookup_expr='gte',
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
        )

    end_date = django_filters.DateFilter(
        name='created',
        lookup_expr='lte',
        label = "End Date",
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )

    class Meta:
        model = InstanceConfigurations
        fields = ['start_date', 'end_date']


class QuestionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        name="created",
        label = "Start Date",
        lookup_expr='gte',
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
        )

    end_date = django_filters.DateFilter(
        name='created',
        lookup_expr='lte',
        label = "End Date",
        widget = DateWidget(
            options ={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )

    class Meta:
        model = Questions
        fields = ['start_date', 'end_date']