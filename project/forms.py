from django import forms
from django.forms.widgets import Select
from django.utils import timezone
from django.forms import models
from django.db.models import Q

from django.contrib.auth.models import User

from .models import Project
from utils.models import Label
from contacts.models import Contact as C
from clients.models import Client
from models import Milestone
from methodologies.models import Phase


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        exclude = ["guid", "content_type", "object_id", "project", "tasks", "status"]

    def __init__(self, *args, **kwargs):
        try:
            self.project = kwargs.pop("project")
        except:
            pass
        super(MilestoneForm, self).__init__(*args, **kwargs)
        self.fields["hours"].label = "<b>Total Hours Allotted</b>"
        try:
            p = self.project
        except:
            p = ""
        else:
            self.fields["phases"].queryset = Phase.objects.filter(
                Q(project_type=p.project_type) | Q(project=p)
            )


class FileUploadForm(forms.Form):
    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "style": "padding:0;padding-left:5px;"}
        ),
        required=False,
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        client = forms.CharField()
        fields = (
            "title",
            "codename",
            "client",
            "contract_hours",
            "description",
            "start_date",
            "end_date",
            "vips",
            "project_type",
        )

    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "style": "padding:0;padding-left:5px;"}
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].initial = timezone.now()
        self.fields["end_date"].initial = timezone.now()


class ProjectRoleForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ()

    person = forms.ChoiceField(choices=[], required=False)
    role = forms.ModelChoiceField(queryset=Label.objects.filter(project=True))

    def __init__(self, *args, **kwargs):
        super(ProjectRoleForm, self).__init__(*args, **kwargs)
        tester_list = []
        tester_list.append(("add", "+ Add Contact to %s" % self.instance.name))
        TESTERS = list(User.objects.all())
        for item in TESTERS:
            tester_list.append(
                ("u%s" % item.id, "User: %s %s" % (item.first_name, item.last_name))
            )
        contact_list = []
        CONTACTS = list(self.instance.contacts.all())
        for item in CONTACTS:
            contact_list.append(
                ("c%s" % item.id, "Contact: %s %s" % (item.first_name, item.last_name))
            )
        choices = tester_list + contact_list
        self.fields["person"].choices = choices


class ProjectVIPForm(forms.Form):
    """
    Can accept a project instance to populate the queryset
    """

    vips = forms.ModelMultipleChoiceField(
        queryset=[], required=False, label="<b>Project Roles</b>"
    )

    def __init__(self, *args, **kwargs):
        super(ProjectVIPForm, self).__init__(*args, **kwargs)
        try:
            self.fields["vips"].queryset = self.instance.vips.all()
        except:
            pass
