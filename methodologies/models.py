from __future__ import unicode_literals

from django.db import models
from django.db.models import Q, Sum, Count, F
from decimal import Decimal
from django.contrib.auth.models import User

# from files.models import Associated_File

from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class PhaseManager(models.Manager):
    def get_by_natural_key(self, guid):
        return self.get(guid=guid)


class Phase(models.Model):
    objects = PhaseManager()

    guid = models.CharField(max_length=260, blank=True, null=True)
    parent_guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    title = models.CharField(max_length=100)
    sequence = models.IntegerField(default=1)
    project = models.ForeignKey(
        "project.Project", blank=True, null=True, on_delete=models.CASCADE
    )
    version = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
    ancestor = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL
    )
    descendant = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="childphase",
        on_delete=models.SET_NULL,
    )
    notes = GenericRelation("notes.Note", related_query_name="phase")
    timeEntries = GenericRelation("timetracker.Time_Entry",related_query_name="phase")
    recommend = models.BooleanField(default=False)
    suggestor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )
    newest = models.BooleanField(default=True)

    def natural_key(self):
        return (self.guid,)

    def __str__(self):
        return "%s" % (self.title)

    app_label = "methodologies"
    model_class = "Phase"
    type_label = "phase"
    details_url = "/db_phase_details/"
    edit_url = "/db_phase_edit_form/"

    @property
    def note_count(self):
        count = self.notes.filter(newest=True).count()
        return count

    @property
    def task_count(self):
        count = self.task_set.all().count()
        return count

    @property
    def billed_phase_time(self):
        time = self.timeEntries.filter(newest=True).aggregate(Sum(F("time")))["time__sum"]
        if time is None:
            time = Decimal(0.00)
        return time

    @property
    def billed_task_time(self):
        time = Decimal(0.00)
        tasks = self.task_set.all()
        for task in tasks:
            t = task.total_time
            if t != None:
                time += t
        return time

    @property
    def billed_total_time(self):
        time = self.billed_phase_time + self.billed_task_time
        if time is None:
            time = Decimal(0.00)
        return time

    @property
    def audit_label(self):
        return self.title

    @property
    def get_notes(self):
        return self.notes.filter(newest=True)

    @property
    def get_time_entries(self):
        return self.timeEntries.filter(newest=True)

    @property
    def has_recommended(self):
        for method in self.method_set.all():
            if method.recommend:
                for pt in self.project_type_set.all():
                    if pt.has_recommended:
                        return True
        return False

    @property
    def select_label(self):
        return self.title

    @property
    def method_count(self):
        return self.method_set.all().count()

    @property
    def has_ancestor(self):
        if self.ancestor:
            return True
        else:
            return False

    @property
    def has_descendant(self):
        if self.descendant:
            return True
        else:
            return False

    def current_methods(self):
        return self.method_set.filter(newest=True).order_by("sequence")

    def current_tasks(self):
        return self.task_set.filter(newest=True)


###############################################################################


class ProjectTypeManager(models.Manager):
    def get_by_natural_key(self, guid):
        return self.get(guid=guid)


class Project_Type(models.Model):
    guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    title = models.CharField(max_length=400)
    shorthand = models.CharField(max_length=10)
    version = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
    phase = models.ManyToManyField(Phase, blank=True)
    newest = models.BooleanField(default=True)
    sequence = models.IntegerField(default=1)
    objects = ProjectTypeManager()

    def natural_key(self):
        return (self.guid,)

    def __str__(self):
        return "%s - %s" % (self.shorthand, self.title)

    app_label = "methodologies"
    model_class = "Project_Type"
    type_label = "project_type"
    details_url = "/db_ptype_details/"
    edit_url = "/db_ptype_edit_form/"
    export_url = "/export_project_type/"

    @property
    def has_recommended(self):
        for method in self.method_set.all():
            if method.recommend:
                return True
        return False

    @property
    def has_recommended_unassociated(self):
        for method in self.method_set.filter(phase=None):
            if method.recommend:
                return True
        return False

    @property
    def audit_label(self):
        return self.title

    @property
    def select_label(self):
        return self.title

    def current_phases(self):
        return self.phase.filter(newest=True, project=None).order_by("sequence")

    def no_phase_methods(self):
        return self.method_set.filter(phase=None)


###############################################################################


class MethodManager(models.Manager):
    def get_by_natural_key(self, guid):
        return self.get(guid=guid)


class Method(models.Model):
    objects = MethodManager()

    guid = models.CharField(max_length=260, blank=True, null=True)
    parent_guid = models.CharField(max_length=260, blank=True, null=True)
    lineage_guid = models.CharField(max_length=260, blank=True, null=True)
    project_type = models.ManyToManyField(Project_Type, blank=True)
    phase = models.ForeignKey(Phase, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    tier = models.IntegerField(default=1)
    sequence = models.IntegerField(default=1, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    command = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True, default="")
    automate = models.BooleanField(default=False)
    mangle = models.CharField(max_length=50, blank=True, null=True)
    help_base = models.TextField(blank=True, null=True)
    help_import = models.TextField(blank=True, null=True)
    est_time = models.CharField(max_length=50, blank=True, null=True)
    version = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
    files = models.ManyToManyField("files.Associated_File", blank=True)
    recommend = models.BooleanField(default=False)
    newest = models.BooleanField(default=True)
    children = models.ManyToManyField("tasks.Task", blank=True)
    suggestor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )
    ancestor = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL
    )
    descendant = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="method_descendant",
    )

    def set_sequence(self, seq, phase_id, project_type_id):
        seq = int(seq)
        try:
            mo = Method_Order.objects.get(
                method__id=self.id, phase__id=phase_id, project_type__id=project_type_id
            )
        except Method_Order.DoesNotExist:
            mo = None
        if mo:
            original_sequence = mo.sequence
            print(original_sequence, seq)
            if seq < 1:
                seq = 1
            mo.sequence = seq
            if original_sequence < seq:
                print("lesser")
                rows = Method_Order.objects.filter(
                    sequence__gt=original_sequence, sequence__lte=seq
                )
                for row in rows:
                    row.sequence -= 1
                    row.save()
            else:
                print("greater")
                rows = Method_Order.objects.filter(
                    sequence__gte=seq, sequence__lt=original_sequence
                )
                for row in rows:
                    row.sequence += 1
                    row.save()
            mo.save()
        else:
            method_order = Method_Order(
                method=self,
                phase=self.phase,
                project_type=Project_Type.objects.get(id=project_type_id),
                sequence=seq,
            )
            rows = Method_Order.objects.filter(sequence__gte=seq)
            for row in rows:
                row.sequence += 1
                row.save()
            method_order.save()

    def natural_key(self):
        return (self.guid,)

    def __str__(self):
        return "%s" % (self.title)

    add_url = ""
    submit_url = ""
    edit_url = "/db_method_edit_form/"
    delete_url = ""
    details_url = "/db_method_details/"
    model_type = "method"
    type_label = "method"
    app = "methodologies"
    model_name = "Method"

    @property
    def get_total_task_time(self):
        time = Decimal(0.00)
        for task in self.task_set.all():
            if task.total_time != None:
                time += task.total_time
        return time

    @property
    def task_count(self):
        count = self.task_set.all().count()
        return count

    @property
    def has_ancestor(self):
        if self.ancestor:
            return True
        else:
            return False

    @property
    def has_descendant(self):
        if self.descendant:
            return True
        else:
            return False

    @property
    def select_label(self):
        return self.title

    def can_deploy(self):
        if (
            not self.recommend
            and self.phase is not None
            and self.project_type.count() > 0
        ):
            return True
        else:
            return False


class Method_Order(models.Model):
    project_type = models.ForeignKey(Project_Type)
    phase = models.ForeignKey(Phase)
    method = models.ForeignKey(Method, related_name="orders")
    sequence = models.IntegerField(default=1)

    def remove(self):
        orders = Method_Order.objects.filter(
            phase__id=self.phase.id,
            project_type__id=self.project_type.id,
            sequence__gt=self.sequence,
        )
        for order in orders:
            order.sequence -= 1
            order.save()
        self.delete()

    def update_phase(self, phase):
        orders = Method_Order.objects.filter(
            phase__id=self.phase.id,
            project_type__id=self.project_type.id,
            sequence__gt=self.sequence,
        )
        for order in orders:
            order.sequence -= 1
            order.save()
        self.phase = phase
        orders = Method_Order.objects.filter(
            phase__id=self.phase.id,
            project_type__id=self.project_type.id,
            sequence__gte=self.sequence,
        )
        for order in orders:
            order.sequence += 1
            order.save()
        self.save()


###############################################################################
