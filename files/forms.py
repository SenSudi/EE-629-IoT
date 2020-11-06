from django import forms


class FileUploadForm(forms.Form):
    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )


class BothFilesForm(forms.Form):
    issue_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": False}), required=False
    )
    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )


class ImportFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": False}), required=True
    )
