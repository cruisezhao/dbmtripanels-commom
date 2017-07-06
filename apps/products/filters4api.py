"""product filter for portal"""

from django_filters import rest_framework  as filters
from common.apps.products.models import ProductApps

class ProductAppsFilter4API(filters.FilterSet):
    """product filter"""
    class Meta:
        model = ProductApps
        exclude = ['uuid','pk']