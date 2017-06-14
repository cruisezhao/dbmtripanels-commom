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
        fields = ['id', 'product_pic', 'name', 'type', 'summary', 'features']


class ProductDetailSerializer(serializers.ModelSerializer):
    """software detail serialzer"""
    features = serializers.JSONField(read_only=True)
    environments = serializers.JSONField(read_only=True)
    screenshots = serializers.JSONField(read_only=True,source='get_screenshots')
    videos = serializers.JSONField(read_only=True,source='get_videos')

    class Meta:
        model = Products
        fields = ['id', 'name', 'type','total_users', 'summary', 'description', 'product_url', 'product_pic',
                  'product_img', 'latest_version', 'facebook_url', 'google_plus_url',
                  'linkedin_url', 'twitter_url', 'document_url',  'free_plan', 'features', 'environments','screenshots',
                  'videos']
        read_only_fields = ('name','type','features','environments','screenshot')
