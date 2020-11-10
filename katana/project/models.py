from __future__ import unicode_literals

from decimal import Decimal
from django.db import models
from project.getters.models import get_project_phases

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from methodologies.models import Project_Type
from files.models import Associated_File, Issue_File

# ''.join('%02x' % ord(x) for x in os.urandom(16))

# Create your models here.
#


class Vip(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    person = GenericForeignKey("content_type", "object_id")
    role = models.ForeignKey(
        "utils.Label", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return "%s - %s" % (self.role, self.person)

    @property
    def name(self):
        return "%s %s" % (self.person.first_name, self.person.last_name)


class Project(models.Model):
    title = models.CharField(max_length=255)
    client = models.ForeignKey(
        "clients.Client", blank=True, null=True, on_delete=models.SET_NULL
    )
    codename = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(max_length=2000, blank=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    contract_hours = models.DecimalField(
        blank=True, max_digits=7, decimal_places=2, default=0.00
    )
    project_type = models.ForeignKey(Project_Type, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True, blank=True)
    issue_number = models.PositiveIntegerField(default=1, blank=True)
    is_billable = models.BooleanField(default=True, blank=True)
    vips = models.ManyToManyField(Vip, blank=True)
    associated_files = GenericRelation(Associated_File, related_query_name="project")
    issue_files = GenericRelation(Issue_File, related_query_name="project")
    notes = GenericRelation("notes.Note", related_query_name="associated_project")
    members = models.ManyToManyField(User, blank=True)
    project_milestone = models.ForeignKey(
        "project.Milestone",
        related_query_name="completion_milestone",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return "%s" % (self.title)

    @property
    def url(self):
        return "/overview"

    @property
    def phases(self):
        phases = get_project_phases(self)
        return phases

    @property
    def issue_count(self):
        count = self.issue_set.all().count()
        return count

    @property
    def task_count(self):
        return self.task_set.filter(newest=True).count()

    @property
    def note_count(self):
        return self.notes.all().count()

    @property
    def file_count(self):
        return self.associated_files.all().count() + self.issue_files.all().count()

    @property
    def contact_count(self):
        return self.client.contacts.all().count()

    def get_contacts(self):
        return self.client.contacts.all()

    def get_newest_task(self, lineage):
        return self.task_set.get(lineage_guid=lineage, newest=True)

    def get_phase(self, lineage):
        try:
            phase = self.phase_set.get(lineage_guid=lineage)
        except:
            return None
        else:
            return phase

    def get_phases(self):
        return self.phase_set.filter(newest=True).order_by("sequence")

    def get_narrative(self):
        return self.narrative_set.all().order_by("-date").order_by("-time")


class Milestone(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    hours = models.DecimalField(
        blank=True, max_digits=7, decimal_places=2, default=0.00
    )
    comment = models.TextField(max_length=500, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(
        Project, blank=True, null=True, on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50, blank=True, default="open")

    phases = models.ManyToManyField("methodologies.Phase", blank=True)
    tasks = models.ManyToManyField("tasks.Task", blank=True)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "%s - %s hours remain" % (self.title, self.hours)

    @property
    def start(self):
        return "%s" % self.start_date.strftime("%m/%d/%Y")

    @property
    def end(self):
        return "%s" % self.end_date.strftime("%m/%d/%Y")

    @property
    def completed(self):
        project = self.project
        phase_list = list(self.phases.all())
        completed = Decimal(0.00)
        for task in project.task_set.all():
            if task.phase in phase_list:
                if task.total_time is not None:
                    completed += task.total_time
        return completed

    @property
    def remaining(self):
        completed = self.completed
        total = self.hours
        remaining = total - completed
        return remaining

    @property
    def display_phases(self):
        out = "Associated Phases:\n"
        for phase in self.phases.all():
            out += "    - %s\n" % (phase.title)
        out += "\n"
        return out
