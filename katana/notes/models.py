from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from project.models import Project


from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=True, default="")
    project = models.ForeignKey(Project, blank=True, null=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    ancestor = models.ForeignKey("self", blank=True, null=True)
    child = models.ForeignKey("self", blank=True, null=True, related_name="child_note")
    newest = models.BooleanField(default=False)
    # for generic item association
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "%s for %s" % (self.title, self.content_type)


class Scratchpad(models.Model):
    body = models.TextField(blank=True, default="")
    testers = models.ManyToManyField(User, blank=True)
    updated = models.DateTimeField(auto_now=True)
    in_use = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name="current_users", blank=True)
    # for generic item association (Most Likely Project)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        try:
            name = self.tester_set.get().user.username
        except:
            name = self.associated_item
        return "%s's scratchpad" % name


class Narrative(models.Model):
    body = models.TextField(blank=True)
    project = models.ForeignKey(
        Project, blank=True, null=True, on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s - %s, %s" % (self.project, self.date, self.time)
