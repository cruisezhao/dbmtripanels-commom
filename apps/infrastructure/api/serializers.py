from rest_framework import serializers
from ..models.network import Devices

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