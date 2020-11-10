from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q, Sum, Count, F
from decimal import Decimal

from django.db import models
from project.models import Project
from methodologies.models import Method
from utils.models import Time_Object
from utils.models import Variable_Item
from methodologies.models import Phase
from notes.models import Note
from files.models import Associated_File as AF
from timetracker.models import Time_Entry

# Create your models here.
class Task(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    meth_item = models.ForeignKey(
        Method, blank=True, default="", null=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255, blank=True, default="")
    session_time = models.ForeignKey(Time_Object, blank=True, null=True)
    variables = models.ManyToManyField(Variable_Item, blank=True)
    session = models.BooleanField(default=False)
    newest = models.BooleanField(default=True)
    phase = models.ForeignKey(Phase, blank=True, null=True, on_delete=models.SET_NULL)
    parent_guid = models.CharField(max_length=260, blank=True, null=True)
    sequence = models.IntegerField(default=1)
    tier = models.IntegerField(default=1)
    description = models.TextField(max_length=1000, blank=True, default="")
    help_base = models.TextField(max_length=1000, blank=True, default="")
    base_command = models.CharField(max_length=3500, blank=True, null=True)
    est_time = models.CharField(max_length=12, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, default="open")
    created = models.DateTimeField(auto_now_add=True)
    tsk_duration = models.DecimalField(
        default=0, blank=True, max_digits=6, decimal_places=2
    )
    exec_duration = models.CharField(max_length=50, blank=True, default="")
    exec_cmd = models.TextField(max_length=3500, blank=True, null=True)
    mangle = models.CharField(max_length=150, blank=True, null=True)
    notes = GenericRelation(Note, related_query_name="task", blank=True)
    files = GenericRelation(AF, related_query_name="task", blank=True)
    time = GenericRelation(Time_Entry, related_query_name="task", blank=True)

    def __str__(self):
        return "Task: %s" % (self.title)

    model_class = "Task"
    app_label = "tasks"
    type_label = "task"
    delete_url = "/task_delete/"

    @property
    def total_time(self):
        total_time = self.time.filter(newest=True).aggregate(Sum(F("time")))["time__sum"]
        if total_time == None:
            total_time = Decimal(0.00)
        return total_time

    @property
    def note_count(self):
        count = self.notes.filter(newest=True).count()
        return count

    @property
    def get_notes(self):
        notes = self.notes.filter(newest=True)
        return notes

    @property
    def audit_label(self):
        return self.title

    def get_time_entries(self):
        entries = self.time.filter(newest=True)
        return entries

    def entries_count(self):
        return self.time.filter(newest=True).count()

    def has_parent(self):
        if self.meth_item is None:
            return False
        else:
            return True
