from django import forms
from models import *


class DataTableCreate(forms.ModelForm):
    class Meta:
        model = DataTable
        fields = ("name",)


class DataTypeCreate(forms.ModelForm):
    class Meta:
        model = DataType
        fields = ("label",)
        labels = {"label": "<b>Create New Data Type</b>"}


class DataItemCreate(forms.ModelForm):
    class Meta:
        model = DataItem
        fields = ("data_type",)


class DataItemImport(forms.Form):
    data_type = forms.ModelChoiceField(
        required=True, label="<b>Data Type</b", queryset=DataType.objects.all()
    )
    import_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": False}), required=True
    )
