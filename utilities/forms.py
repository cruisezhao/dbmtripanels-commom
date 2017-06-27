from django import forms


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