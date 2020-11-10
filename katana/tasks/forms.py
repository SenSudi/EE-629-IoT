from django import forms

from models import Task
from methodologies.models import Phase
import sys

try:
    from files.models import Associated_File as AF
except:
    AF = getattr(sys.modules["files.models"], "Associated_File")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "tier",
            "sequence",
            "description",
            "est_time",
            "help_base",
            "base_command",
        )

    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": True,
                "style": "position:relative;padding:0;padding-left:5px;min-height:35px;",
            }
        ),
        required=False,
    )


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "phase",
            "tier",
            "sequence",
            "description",
            "est_time",
            "help_base",
            "base_command",
        )

    files = forms.ModelMultipleChoiceField(queryset=None, required=False)

    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": True,
                "style": "position:relative;padding:0;padding-left:5px;min-height:35px;",
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(TaskEditForm, self).__init__(*args, **kwargs)
        self.fields["phase"].queryset = self.instance.project.phase_set.all().order_by(
            "sequence"
        )
        self.fields[
            "files"
        ].queryset = (
            self.instance.files.all()
        )  # AF.objects.filter(a_i_guid=self.instance.guid)
        self.fields["files"].initial = self.instance.files.values_list("id", flat=True)
        self.fields["files"].label = "<span>Current Files</span>"
