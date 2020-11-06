from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from project.models import Project

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Action(models.Model):
    who = models.ForeignKey(User)
    what = models.CharField(max_length=255, default="")
    where = models.CharField(max_length=255, default="")
    when = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(Project, blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "%s %s %s %s" % (self.who, self.what, self.where, self.when)
