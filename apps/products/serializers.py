from rest_framework import serializers
from .models import ProductApps


class ProductAppsListSerializer(serializers.HyperlinkedModelSerializer):
    '''
    serailizer for list on index page
    '''
    features = serializers.JSONField(read_only=True)
    uuid = serializers.JSONField(read_only=True,source='get_product_uuid')
    # url = ParameterisedHyperlinkedIdentityField(view_name="software_detail", read_only=True)
    class Meta:
        model = ProductApps
        fields = ['pk','uuid', 'product_pic', 'app_name', 'summary', 'features']


class ProductAppsDetailSerializer(serializers.ModelSerializer):
    """software detail serialzer"""
    features = serializers.JSONField(read_only=True)
    screenshots = serializers.JSONField(read_only=True,source='get_screenshots')
    videos = serializers.JSONField(read_only=True,source='get_videos')

    class Meta:
        model = ProductApps
        fields = ['pk','uuid','app_name', 'total_users', 'summary', 'description', 'product_url', 'product_pic',
                  'product_img', 'latest_version', 'facebook_url', 'google_plus_url',
                  'linkedin_url', 'twitter_url', 'document_url',  'free_plan', 'features','screenshots',
                  'videos']
        read_only_fields = ('pk','app_name','type','features','environments','screenshot')
