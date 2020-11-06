from django import forms

# from django.forms.widgets import Select
from models import Method as M
from models import Project_Type as PT
from models import Phase as Ph
from files.models import Associated_File as AF


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class MethodForm(forms.ModelForm):
    position = ChoiceFieldNoValidation(
        choices=[("before", "Before"), ("after", "After")]
    )
    method = ChoiceFieldNoValidation(
        choices=[("", "--------")], required=False, widget=forms.Select()
    )

    class Meta:
        model = M
        fields = (
            "title",
            "project_type",
            "phase",
            "tier",
            "command",
            "description",
            "automate",
            "help_base",
            "help_import",
            "est_time",
            "mangle",
        )

    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )


class MethodUpdateForm(forms.ModelForm):
    position = ChoiceFieldNoValidation(
        choices=[("before", "Before"), ("after", "After")]
    )
    method = ChoiceFieldNoValidation(
        choices=[("", "--------")], required=False, widget=forms.Select()
    )

    class Meta:
        model = M
        fields = (
            "title",
            "project_type",
            "phase",
            "tier",
            "command",
            "mangle",
            "description",
            "automate",
            "help_base",
            "help_import",
            "est_time",
            "mangle",
            "files",
        )

    def __init__(self, *args, **kwargs):
        super(MethodUpdateForm, self).__init__(*args, **kwargs)
        self.fields["files"].queryset = AF.objects.filter(a_i_guid=self.instance.guid)

    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )


class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = PT
        fields = ("title", "shorthand", "phase")

    def __init__(self, *args, **kwargs):
        super(ProjectTypeForm, self).__init__(*args, **kwargs)
        self.fields["phase"].label = "<b>Associate Phases With This Project Type</b>"


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Ph
        fields = ("title", "sequence")


class mdbPhaseForm(forms.ModelForm):
    class Meta:
        model = Ph
        fields = ("title", "sequence")

    associated_project_types = forms.ModelMultipleChoiceField(
        queryset=PT.objects.all(), label="<b>Associate Phase With Project Types</b>"
    )


class PhaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Ph
        fields = ("title", "sequence")

    associated_project_types = forms.ModelMultipleChoiceField(
        queryset=PT.objects.all(), label="<b>Dis/Associate Phase With Project Types</b>"
    )
    associated_methods = forms.ModelMultipleChoiceField(
        queryset=[], label="<b>Dis/Associate Methods With This Phase</b>"
    )
