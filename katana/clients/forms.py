from django import forms

from models import Client as C


class ClientForm(forms.ModelForm):
    class Meta:
        model = C
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
