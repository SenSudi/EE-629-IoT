from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.shortcuts import render

from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder as DJE

# Create your models here.
class DataType(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True)
    attributes = JSONField(default=dict, encoder=DJE)

    def __str__(self):
        return self.label

    def add_attribute(self, name="new attribute", value="", context={}):
        self.attributes.update({name: value})
        self.save()
        context["name"] = name
        context["value"] = value
        return render(None, "attr.html", context).content

    def get_attributes(self):
        at_list = []
        for name in (self.attributes).keys():
            at_list.append((name, self.attributes[name].strip()))
        return at_list

    @property
    def list_attributes(self):
        at_list = self.get_attributes()
        context = {}
        context["attrs"] = at_list
        return render(None, "attrs.html", context).content

    @property
    def option(self):
        context = {}
        context["type"] = self
        return render(None, "option.html", context).content


class DataItem(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    data_type = models.ForeignKey(DataType)
    attrs = JSONField(default=dict, encoder=DJE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s Item" % self.data_type

    @property
    def get_attrs(self):
        at_list = []
        for name in dict(self.data_type.attributes).keys():
            at_list.append((name, self.attrs.get(name, "")))
        return at_list

    @property
    def html(self):
        context = {}
        context["item"] = self
        return render(None, "item.html", context).content


class DataTable(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    items = models.ManyToManyField(DataItem, blank=True)
    project = models.ForeignKey(
        "project.Project", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return "%s - %s item(s)" % (self.name, self.items.count())

    @property
    def get_items(self):
        return self.items.all()

    @property
    def html(self):
        context = {}
        context["table"] = self
        return render(None, "table.html", context).content
