from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from file_utils import project_directory_path
from file_utils import issue_file_path
from file_utils import size_conversion


# from project.models import Project as P


# Create your models here.
class AssociatedFileManager(models.Manager):
    def get_by_natural_key(self, guid):
        return self.get(guid=guid)


class Associated_File(models.Model):
    objects = AssociatedFileManager()

    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to=project_directory_path, blank=True, null=True)
    subdirectory = models.CharField(max_length=100, default="misc")
    uploader = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    newest = models.BooleanField(default=True)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")
    a_i_guid = models.CharField(max_length=260, blank=True, null=True)

    def natural_key(self):
        return self.guid

    def __str__(self):
        return "%s" % (self.filename)

    @property
    def extension(self):
        return "%s" % self.file.name[self.file.name.rfind(".") :]

    @property
    def size(self):
        return "%s" % size_conversion(self.file.size)

    @property
    def url(self):
        return "%s" % self.file.url

    @property
    def path(self):
        return "%s" % self.file.path

    @property
    def name_only(self):
        return "%s" % self.filename[: self.filename.rfind(".")]

    def a_tag(self):
        return '<a href="%s" target="_blank">%s</a>' % (self.url, self.filename)


###############################################################################


class IssueFileManager(models.Manager):
    def get_by_natural_key(self, guid):
        return self.get(guid=guid)


class Issue_File(models.Model):
    objects = IssueFileManager()

    guid = models.CharField(max_length=260, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to=issue_file_path, blank=True, null=True)
    uploader = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)
    issue_number = models.PositiveIntegerField(default=1)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_project = GenericForeignKey("content_type", "object_id")

    def natural_key(self):
        return self.guid

    def __str__(self):
        return "%s" % self.filename

    @property
    def name_only(self):
        return "%s" % self.filename[: self.filename.rfind(".")]

    @property
    def date(self):
        return "%s" % self.updated.strftime("%d-%m-%y")

    @property
    def extension(self):
        return "%s" % self.file.name[self.file.name.rfind(".") :]

    @property
    def size(self):
        return "%s" % size_conversion(self.file.size)

    @property
    def url(self):
        return "%s" % self.file.url
