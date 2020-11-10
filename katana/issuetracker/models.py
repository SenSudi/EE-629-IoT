from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from project.models import Project
from files.models import Associated_File
from files.models import Issue_File

from notes.models import Note
from timetracker.models import Time_Entry as time
# Create your models here.


class Status(models.Model):
    title = models.CharField(max_length=100)
    sequence = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s" % (self.title)

    add_url = "/it_status_add_form/"
    submit_url = "/it_status_add/"
    edit_url = "/it_status_edit/"
    delete_url = "/it_status_delete/"
    model_type = "status"
    app = "issuetracker"
    model_name = "Status"
    min_sequence = 1


class Issue(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contributors = models.ManyToManyField(User, blank=True)
    author = models.ForeignKey(
        User, related_name="author", null=True, on_delete=models.SET_NULL
    )
    technical_poc = models.ForeignKey(
        User,
        related_name="technical_poc",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    project = models.ForeignKey(Project, blank=True, null=True)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)
    client_issue_designation = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, null=True)
    issue_files = models.ManyToManyField(Issue_File, blank=True)
    issue_number = models.PositiveIntegerField(default=1)
    daily_version = models.PositiveIntegerField(default=1)
    associated_files = models.ManyToManyField(Associated_File, blank=True)
    # below is for dynamic owner population
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    issue_owner = GenericForeignKey("content_type", "object_id")
    notes = GenericRelation(Note, related_query_name="issue")

    def __str__(self):
        return "%s" % self.title

    def latest_issue_file(self):
        try:
            return self.issue_files.latest("updated")
        except:
            return False

    @property
    def date(self):
        return "%s" % self.updated.strftime("%m-%d-%y")

    @property
    def audit_label(self):
        return self.title

    def get_files(self):
        return list(self.issue_files.all()) + list(self.associated_files.all())

    def get_notes(self):
        return self.notes.filter(newest=True)

    def get_time_entries(self):
        return self.time.filter( newest=True)

    details_url = "/it_issue_details/"
    edit_url = "/it_issue_update_form/"
    note_form = "/note_add_form/?cancel_class=it-modal-note-cancel&form_id=form-issue-note-form&submit_id=btn-it-modal-note-submit"
    file_form = "/both_files_form/"
