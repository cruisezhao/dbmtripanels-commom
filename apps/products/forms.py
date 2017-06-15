from django.forms import ModelForm
from .models import Software


class SoftwareForm(ModelForm):
    """software verify form"""
    def __init__(self, *args, **kwargs):
        super(SoftwareForm, self).__init__(*args,**kwargs)
        self.fields['type'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Software
        fields = ('type', 'name', 'status')


class SoftwareShowForm(ModelForm):
    """show software in portal"""
    def __init__(self, *args, **kwargs):
        super(SoftwareShowForm, self).__init__(*args,**kwargs)
        self.fields['type'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Software
        fields = ('type', 'name', 'in_homepage')
