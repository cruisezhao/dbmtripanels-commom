from django import forms
from .models.network import DeviceRacks

class DeviceRacksForm(forms.ModelForm):
    """"""
    class Meta:
        model = DeviceRacks
        fields = ['name','price']