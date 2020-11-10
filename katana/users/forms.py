from django import forms
from models import Tester
from django.contrib.auth.models import User, Group

from project.models import Project


class UserDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())

    def check_match(self):
        pw = self.fields["password"].initial
        cf = self.fields["confirm"].initial
        if pw != None and cf != None:
            if pw != "":
                if pw == cf:
                    return True
        return False


class TesterForm(forms.ModelForm):
    class Meta:
        model = Tester
        fields = ("avatar",)


class UserForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(render_value=True)
    )
    tier = forms.IntegerField(min_value=0, max_value=4, required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    phone = forms.CharField(
        max_length=10, required=False, label="<b>Phone (digits only, no dashes)</b>"
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False
    )
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(), required=False
    )


class UserEditForm(forms.Form):
    username = forms.CharField(required=False)
    first = forms.CharField(required=False)
    last = forms.CharField(required=False)
    email = forms.CharField(required=False)
    active = forms.BooleanField(required=False)
    avatar = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": False}), required=False
    )
    tier = forms.IntegerField(min_value=0, max_value=4, required=True)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False
    )
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(), required=False
    )
