from rest_framework import serializers
from ..models.network import Devices
from ..models.ip import VLANs

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Devices
        fields = [
            'id','data_center','manufacturer','seller','name','tag',
            'description', 'type','u_height','size','model_no',
            'serial_no','online_date','offline_date','order_date',
            'price','order_no','warranty_date','access_method',
            'access_port','username','password','status','notes',
        ]


class VlanSerializer(serializers.ModelSerializer):
    """vlan serializer
    """
    class Meta:
        model = VLANs
        fields = ['data_center', 'device', 'name', 'description', 'vid','status','notes']