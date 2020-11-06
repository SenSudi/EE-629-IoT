from django import forms
from django.utils import timezone

from models import Time_Entry as TE
from project.models import Project

from notes.models import Note


class TimeEntryForm(forms.ModelForm):
    time = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"placeholder": "e.g. 1 . 25 = 1 & 1/4 hours", "step": 0.25}
        ),
        required=False,
        initial=0,
    )
    date = forms.DateField(initial=timezone.now, required=False)

    class Meta:
        model = TE
        fields = (
            "title",
            "project",
            # 'time',
            # 'date',
            "body",
        )

    def __init__(self, *args, **kwargs):
        super(TimeEntryForm, self).__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(is_billable=True)


class TaskTimeEntryForm(forms.ModelForm):
    time = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": "1.25", "step": 0.25}), required=True)
    date = forms.DateField(initial=timezone.now, required=True)

    class Meta:
        model = TE
        fields = ("title","body",)

    def __init__(self,*args,**kwargs):
        super(TaskTimeEntryForm,self).__init__(*args,**kwargs)
        self.fields["time"].label = "<span>Hours</span>"
        self.fields["date"].label = "<span>Date of work</span>"
