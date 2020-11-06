from django import forms
from models import Issue as I
from django.contrib.auth.models import User
from contacts.models import Contact as C
from models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ("title", "sequence")


class IssueUpdateForm(forms.ModelForm):
    class Meta:
        model = I
        fields = (
            "title",
            "status",
            "client_issue_designation",
            "description",
            "technical_poc",
            "project",
        )

    issue_owner = forms.ChoiceField(choices=[], required=False)
    issue_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": False}), required=False
    )
    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )

    def __init__(self, *args, **kwargs):
        super(IssueUpdateForm, self).__init__(*args, **kwargs)
        self.fields["project"].disabled = True
        if self.instance.latest_issue_file():
            latest = self.instance.latest_issue_file()
            self.fields["issue_file"].label = (
                'Current Issue File: <a href="%s">%s</a>'
                % (latest.file.url, latest.filename)
            )
        blank = [("", "---------")]
        tester_list = []
        TESTERS = list(User.objects.all())
        for item in TESTERS:
            tester_list.append(
                ("u%s" % item.id, "User: %s %s" % (item.first_name, item.last_name))
            )
        contact_list = []
        CONTACTS = list(C.objects.all())
        for item in CONTACTS:
            contact_list.append(
                ("c%s" % item.id, "Contact: %s %s" % (item.first_name, item.last_name))
            )
        choices = blank + tester_list + contact_list
        self.fields["issue_owner"].choices = choices
        try:
            initial = self.instance.issue_owner._meta.model_name[:1] + str(
                self.instance.issue_owner.id
            )
        except:
            pass
        else:
            self.fields["issue_owner"].initial = initial


class IssueForm(forms.ModelForm):
    class Meta:
        model = I
        fields = (
            "title",
            "project",
            "client_issue_designation",
            "status",
            "description",
            "technical_poc",
        )

    issue_owner = forms.ChoiceField(choices=[], required=False)
    issue_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": False}), required=False
    )
    associated_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        tester_list = []
        TESTERS = list(User.objects.all())
        for item in TESTERS:
            tester_list.append(
                ("u%s" % item.id, "User: %s %s" % (item.first_name, item.last_name))
            )
        contact_list = []
        CONTACTS = list(C.objects.all())
        for item in CONTACTS:
            contact_list.append(
                ("c%s" % item.id, "Contact: %s %s" % (item.first_name, item.last_name))
            )
        blank = [("", "---------")]
        choices = blank + tester_list + contact_list
        self.fields["issue_owner"].choices = choices
        self.fields["status"].initial = Status.objects.get(title="Open").id
        # self.fields['status'].label 		= '<b>Status </b><i class="btn-it-status-add btn-form-field-add fa fa-plus" data-url="%s" data-model-type="%s" style="cursor:pointer;margin-left:10px;color:green;position:relative;top:1px;"></i>'%(Status.add_url,Status.model_type)
