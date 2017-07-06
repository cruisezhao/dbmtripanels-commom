from django import forms
from django.utils.html import mark_safe
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget


class ReturnURLForm(forms.Form):
    """
    Privide a hidden return URL field to control where the user is directed
    after the form is submitted
    """
    return_url = forms.CharField(required=False, widget=forms.HiddenInput())

class ComfirmationForm(ReturnURLForm):
    """confirmation form, the form is not valid unless the
        confirm field is checked"""
    confirm = forms.BooleanField(required=True)

class FilterChoiceFieldMixin(object):
    iterator = forms.models.ModelChoiceIterator

    def __init__(self, null_option=None, *args, **kwargs):
        self.null_option = null_option
        if 'required' not in kwargs:
            kwargs['required'] = False
        if 'widget' not in kwargs:
            kwargs['widget'] = forms.SelectMultiple(attrs={'size': 6})
        super(FilterChoiceFieldMixin, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        label = super(FilterChoiceFieldMixin, self).label_from_instance(obj)
        if hasattr(obj, 'filter_count'):
            return mark_safe("{} <span class='badge pull-right'>{}</span>".format(label, obj.filter_count))
        return label

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        if self.null_option is not None:
            return itertools.chain([self.null_option], self.iterator(self))
        return self.iterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)


class FilterChoiceField(FilterChoiceFieldMixin, forms.ModelMultipleChoiceField):
    pass


class DateFilterMixin(forms.Form):
    """used for render start date and end date"""
    start_date = forms.DateField(
        required=False,
        label='Start Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3),
    )
    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=DateWidget(
            options={'format': 'yyyy-mm-dd',},
            bootstrap_version=3
        ),
    )