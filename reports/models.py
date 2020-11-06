from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from files.models import Associated_File

from django.utils import timezone

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.postgres.fields import ArrayField, JSONField

from utils.tools import get_guid

# Create your models here.


class Report_Item_Attribute(models.Model):
    title = models.CharField(max_length=100)
    input_type = models.CharField(max_length=20, default="text")
    value = ArrayField(models.CharField(max_length=200), blank=True)
    item_type = models.ForeignKey(
        "reports.Report_Item_Type", null=True, blank=True, related_name="attributes"
    )
    item = models.ForeignKey(
        "reports.Report_Item", null=True, blank=True, related_name="attributes"
    )
    sequence = models.PositiveIntegerField(default=1)
    selected = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s" % self.title


class Report_Item_Type(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.title

    @property
    def select_label(self):
        return self.title


class Report_Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    item_type = models.ForeignKey(Report_Item_Type, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contributor = models.ForeignKey(User, blank=True, null=True)
    ancestor = models.ForeignKey("self", blank=True, null=True)
    newest = models.BooleanField(default=True)

    app_label = "reports"
    model_class = "Report_Item"
    type_label = "report_item"

    def __str__(self):
        return "%s - created by: %s | updated: %s | is newest generation: %s" % (
            self.title,
            self.contributor,
            self.updated.date(),
            self.newest,
        )

    def get_atts_data(self):
        dict = {}
        for attr in self.attributes.all():
            tag = attr.title.replace(" ", "_").upper()
            dict[tag] = attr.value[attr.selected]
        return dict


class Static_Attribute(models.Model):
    title = models.CharField(max_length=100, unique=True)
    values = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return "%s" % self.title


class Report_Variable(models.Model):
    CHOICES = (("text", "text"), ("textarea", "textarea"))
    display = models.CharField(max_length=255, blank=True, null=True)
    template = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    limit = models.PositiveIntegerField(default=1000)
    input_type = models.CharField(max_length=20, blank=True, null=True, choices=CHOICES)

    app_label = "reports"
    model_class = "Report_Variable"
    type_label = "report_variable"

    def __str__(self):
        return "%s" % self.display


class Wizard_Variable(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    variable = GenericForeignKey("content_type", "object_id")
    limited = models.BooleanField(default=False, blank=True)
    limit = models.PositiveIntegerField(default=1000)
    input_type = models.CharField(max_length=100, blank=True, null=True)
    template_var = models.CharField(max_length=100, blank=True, null=True)
    selectable = models.BooleanField(default=False, blank=True)
    multiple = models.BooleanField(default=False, blank=True)
    selected = ArrayField(
        models.IntegerField(default=-1), blank=True, null=True, default=list
    )
    content = models.TextField(blank=True, null=True)
    step = models.ForeignKey(
        "reports.Wizard_Step", blank=True, null=True, related_name="variables"
    )

    def __str__(self):
        return "%s" % self.variable

    app_label = "reports"
    model_class = "Wizard_Variable"
    type_label = "wizard_variable"
    delete_url = "/wizard_step_var_remove/"
    edit_url = "/wizard_vriable_edit/"

    selectable_list = [("m", "multi-select"), ("s", "single-select")]
    input_list = [("t", "text"), ("a", "textarea")]

    @property
    def title(self):
        try:
            title = self.variable.title
        except:
            title = self.variable.display
        return title

    def get_input_type(self):
        if self.input_type == "single-select":
            return "select"
        elif self.input_type == "multi-select":
            return "select"
        elif self.input_type == "text":
            return "text"
        elif self.input_type == "textarea":
            return "textarea"

    def get_select_items(self):
        if self.get_input_type() == "select":
            return Report_Item.objects.filter(newest=True, item_type=self.variable.id)

    def get_selected_items(self):
        if len(self.selected) > 0:
            items = []
            for rid in self.selected:
                items.append(Report_Item.objects.get(id=rid).get_atts_data())
            return items
        else:
            return []

    def var_label(self):
        return str(self.title).lower().replace(" ", "_")

    def copy(self):
        vcopy = self
        vcopy.id = None
        vcopy.guid = get_guid()
        return vcopy


class Wizard_Step(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sequence = models.PositiveIntegerField(default=1, blank=True)
    wizard = models.ForeignKey(
        "reports.Wizard_Template", blank=True, null=True, related_name="steps"
    )
    report = models.ForeignKey(
        "reports.Report", blank=True, null=True, related_name="steps"
    )

    app_label = "reports"
    model_class = "Wizard_Step"
    type_label = "wizard_step"

    def __str__(self):
        return "%s" % self.title

    def copy(self):
        scopy = self
        scopy.id = None
        scopy.guid = get_guid()
        return scopy


class Wizard_Template(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    title = models.CharField(
        max_length=255, blank=True, null=True, default="New Wizard"
    )
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(
        Associated_File, blank=True, null=True, on_delete=models.SET_NULL
    )

    add_url = "/wizard_template_modal/"
    app_label = "reports"
    model_class = "Wizard_Template"
    type_label = "wizard_template"
    details_url = "/wizard_template_modal/"
    edit_url = "/wizard_template_edit/"

    def __str__(self):
        return "%s" % self.title

    def next_step(self):
        try:
            count = max(list(self.steps.values_list("sequence", flat=True))) + 1
        except:
            return 1
        else:
            return count

    def first_step(self):
        try:
            return self.steps.get(sequence=1)
        except:
            return False

    def step_count(self):
        return self.steps.count()


class Report(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    wizard = models.ForeignKey(Wizard_Template, blank=True, null=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    step_modified = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return "%s" % self.title

    add_url = "/report_add_form/"
    app_label = "reports"
    model_class = "Report"
    type_label = "report"
    details_url = "/report_wizard_details/"
    edit_url = "/report_wizard_update/"
    delete_url = "/report_delete/"
    export_url = "/report_export/"

    @property
    def report_date(self):
        return "%s" % self.updated.strftime("%B %d, %Y")

    def step_count(self):
        return self.steps.count()
