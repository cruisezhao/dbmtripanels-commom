from django import forms
from django.contrib.contenttypes.models import ContentType
from collections import OrderedDict


def get_custom_fields_for_model(content_type, filterable_only=False, bulk_edit=False):
    """
    Retrieve all CustomFields applicable to the given ContentType
    """
    field_dict = OrderedDict()
    kwargs = {'obj_type': content_type}
    if filterable_only:
        kwargs['is_filterable'] = True
    custom_fields = CustomField.objects.filter(**kwargs)

    for cf in custom_fields:
        field_name = 'cf_{}'.format(str(cf.name))

        # Integer
        if cf.type == CF_TYPE_INTEGER:
            field = forms.IntegerField(required=cf.required, initial=cf.default)

        # Boolean
        elif cf.type == CF_TYPE_BOOLEAN:
            choices = (
                (None, '---------'),
                (1, 'True'),
                (0, 'False'),
            )
            if cf.default.lower() in ['true', 'yes', '1']:
                initial = 1
            elif cf.default.lower() in ['false', 'no', '0']:
                initial = 0
            else:
                initial = None
            field = forms.NullBooleanField(required=cf.required, initial=initial,
                                           widget=forms.Select(choices=choices))

        # Date
        elif cf.type == CF_TYPE_DATE:
            field = forms.DateField(required=cf.required, initial=cf.default, help_text="Date format: YYYY-MM-DD")

        # Select
        elif cf.type == CF_TYPE_SELECT:
            choices = [(cfc.pk, cfc) for cfc in cf.choices.all()]
            if not cf.required or bulk_edit or filterable_only:
                choices = [(None, '---------')] + choices
            field = forms.TypedChoiceField(choices=choices, coerce=int, required=cf.required)

        # URL
        elif cf.type == CF_TYPE_URL:
            field = LaxURLField(required=cf.required, initial=cf.default)

        # Text
        else:
            field = forms.CharField(max_length=255, required=cf.required, initial=cf.default)

        field.model = cf
        field.label = cf.label if cf.label else cf.name.replace('_', ' ').capitalize()
        if cf.description:
            field.help_text = cf.description

        field_dict[field_name] = field

    return field_dict


class CustomFieldFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):

        self.obj_type = ContentType.objects.get_for_model(self.model)

        super(CustomFieldFilterForm, self).__init__(*args, **kwargs)

        # Add all applicable CustomFields to the form
        custom_fields = get_custom_fields_for_model(self.obj_type, filterable_only=True).items()
        for name, field in custom_fields:
            field.required = False
            self.fields[name] = field
