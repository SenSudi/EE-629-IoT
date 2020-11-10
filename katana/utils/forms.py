from django import forms

from models import Label


class FeedbackForm(forms.Form):
    subject = forms.CharField(label="<b>Subject</b>", max_length=100, required=True)
    body = forms.CharField(label="<b>Body</b>", required=True, widget=forms.Textarea)
    feedback_files = forms.FileField(
        label="<b>Supporting File (optional)</b>",
        widget=forms.ClearableFileInput(attrs={"multiple": False}),
        required=False,
    )


class RoleForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ("label",)

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields["label"].label = "<b>Role</b>"


class RoleSelectForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Label.objects.filter(project=True), label="<b>Role</b>", required=False
    )


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ("label",)
