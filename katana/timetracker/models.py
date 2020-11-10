from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from project.models import Project

# Create your models here.
class Time_Entry(models.Model):
    tester = models.ForeignKey(User, blank=True, null=True)
    project = models.ForeignKey(
        Project, blank=True, null=True, on_delete=models.CASCADE
    )
    time = models.DecimalField(default=0, blank=True, max_digits=6, decimal_places=2)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    newest = models.BooleanField(default=False)
    ancestor = models.ForeignKey("self", blank=True, null=True)
    child = models.ForeignKey("self", blank=True, null=True, related_name="child_timetracker")

    # Associated Item fields
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "%s minutes on %s for %s by %s" % (
            self.time,
            self.date,
            self.project.title,
            self.tester,
        )
