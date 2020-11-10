from django import forms

from models import Report_Item as RI, Report_Item_Type
from models import Wizard_Template
from models import Wizard_Step
from models import Report_Variable
from models import Report


class ReportVariableForm(forms.ModelForm):
    class Meta:
        model = Report_Variable
        fields = ("display", "template", "limit", "input_type")

    def __init__(self, *args, **kwargs):
        super(ReportVariableForm, self).__init__(*args, **kwargs)
        self.fields["display"].label = "<b>Displayed Field Label</b>"
        self.fields["template"].label = "<b>Template Tag</b>"
        self.fields["input_type"].label = "<b>Input Field Type</b>"
        self.fields["limit"].label = "<b>Input Field limit</b>"
        self.fields["display"].required = True
        self.fields["input_type"].required = True
        self.fields["limit"].required = True
        self.fields["template"].required = True


class StepForm(forms.ModelForm):
    class Meta:
        model = Wizard_Step
        fields = ("title", "description")

    def __init__(self, *args, **kwargs):
        super(StepForm, self).__init__(*args, **kwargs)
        self.fields["title"].label = "<b>Step Title</b>"
        self.fields["description"].label = "<b>Step Description</b>"


class WizardForm(forms.ModelForm):
    class Meta:
        model = Wizard_Template
        fields = ("title", "description")

    template = forms.FileField(
        label="<b>Template File Upload</b>",
        widget=forms.ClearableFileInput(attrs={"multiple": False}),
        required=False,
    )


class ReportItemForm(forms.ModelForm):
    class Meta:
        model = RI
        fields = ("title", "description", "item_type")

    def __init__(self, *args, **kwargs):
        super(ReportItemForm, self).__init__(*args, **kwargs)
        self.fields["item_type"].queryset = Report_Item_Type.objects.all()


class ReportItemSimpleForm(forms.ModelForm):
    class Meta:
        model = RI
        fields = ("title", "description")


class ReportItemTypeForm(forms.ModelForm):
    class Meta:
        model = Report_Item_Type
        fields = ("title",)


class ReportTypeForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("title", "wizard")

    def __init__(self, *args, **kwargs):
        super(ReportTypeForm, self).__init__(*args, **kwargs)
        self.fields["title"].label = "<b>Title Your Report</b>"
        self.fields["wizard"].label = "<b>Select a Wizard</b>"
        self.fields["wizard"].required = True
        self.fields["wizard"].queryset = Wizard_Template.objects.exclude(active=False)
        # title = forms.
        # wizards = forms.ModelChoiceField(queryset=Wizard_Template.objects.all(),label='<b>Report Type</b>',required=True)
