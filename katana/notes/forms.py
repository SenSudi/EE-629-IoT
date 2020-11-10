from django.utils import timezone
from django import forms

from models import Note as N


class NoteForm(forms.ModelForm):
    class Meta:
        model = N
        fields = ("title", "body")
