from rest_framework import serializers
from .models import Products


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    '''
    serailizer for list on index page
    '''
    features = serializers.JSONField(read_only=True)
    # url = ParameterisedHyperlinkedIdentityField(view_name="software_detail", read_only=True)
    class Meta:
        model = Products
        fields = ['id', 'software_pic', 'name', 'type', 'summary', 'features']
