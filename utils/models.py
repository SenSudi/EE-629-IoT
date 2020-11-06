from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.shortcuts import render

from files.models import Associated_File
from files.file_utils import project_directory_path

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.postgres.fields import ArrayField, JSONField

from files.file_utils import feedback_file_path


class Guid(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.guid)


class Label(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    label = models.CharField(max_length=255)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    associated_item = GenericForeignKey("content_type", "object_id")
    project = models.BooleanField(default=False)
    ri_label = models.BooleanField(default=False)
    attributes = JSONField(default={"Title": [{"value": "", "input_type": "text"}]})
    attr_order = JSONField(default=["Title"])

    def __str__(self):
        return "%s" % (self.label)

    def select_label(self):
        return "%s" % self.label

    def add_attribute(
        self, name="new attribute", value="", context={}, input_type="text"
    ):
        if context["static"]:
            attr = context["staticAttr"]
            self.attributes.update(
                {attr.title: [{"value": attr.values, "input_type": "list"}]}
            )
            self.attr_order.append(attr.title)
            self.save()
            name = attr.title
        else:
            self.attributes.update({name: [{"value": value, "input_type": input_type}]})
            self.save()
        attribute = self.attributes[name][0]
        context["attr"] = (name, attribute["value"], attribute["input_type"])
        context["item_type"] = self
        return render(None, "type_attr.html", context)

    def get_attributes(self):
        at_list = []
        for name in self.attr_order:
            if name in self.attributes.keys():
                attribute = self.attributes[name][0]
                at_list.append((name, attribute["value"], attribute["input_type"]))
        return at_list

    def update_items(self, new, old):
        for item in self.report_item_set.all():
            if item.attrs.get(new, False):
                continue
            else:
                item.attrs[new] = item.attrs.pop(old, None)
                item.save()


class Feedback(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User)
    current_page = models.URLField(max_length=1000)
    supporting_file = models.FileField(
        upload_to=feedback_file_path, blank=True, null=True
    )

    def __str__(self):
        if self.supporting_file:
            return "%s | supporting file:%s" % (self.subject, self.supporting_file.name)
        else:
            return "%s" % self.subject


class Time_Object(models.Model):

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    aggregate = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return "Started: %s" % (self.start_time)


class Variable_Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return "%s, value: %s" % (self.name, self.value)
