from django import forms

from models import Contact as C
from clients.models import Client
from utils.models import Label


class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = C
        fields = ("first_name", "last_name", "email", "phone")

    roles = forms.ModelMultipleChoiceField(
        queryset=Label.objects.filter(project=True), required=False
    )

    def __init__(self, *args, **kwargs):
        super(ContactUpdateForm, self).__init__(*args, **kwargs)
        self.fields["roles"].initial = self.instance.get_role_ids()


class ContactForm(forms.ModelForm):
    class Meta:
        model = C
        fields = ("first_name", "last_name", "email", "phone", "role")

    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)


class ContactEditForm(forms.ModelForm):
    class Meta:
        model = C
        fields = ("first_name", "last_name", "email", "phone", "role")

    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ContactEditForm, self).__init__(*args, **kwargs)
        self.fields["client"].initial = self.instance.client_set.all()[0].id


class ContactOnlyForm(forms.ModelForm):
    class Meta:
        model = C
        fields = ("first_name", "last_name", "email", "phone")

    roles = forms.ModelMultipleChoiceField(
        queryset=Label.objects.filter(project=True), required=False
    )


class DBContactForm(forms.ModelForm):
    class Meta:
        model = C
        fields = ("first_name", "last_name", "email", "phone")

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(), required=False, label="<b>Client</b>"
    )
