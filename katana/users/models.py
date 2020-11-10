from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone

from project.models import Project
from issuetracker.models import Issue
from django.contrib.contenttypes.fields import GenericRelation
from notes.models import Scratchpad

from decimal import Decimal
from django.db.models import Q, Sum, Count, F

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.id, filename)


def week_from_now():
    return timezone.now() + timezone.timedelta(days=7)


class Preferences(models.Model):
    remember_me = models.BooleanField(default=False, blank=True)


class Context(models.Model):
    tt_date_range_start = models.DateField(default=timezone.now)
    tt_date_range_end = models.DateField(default=week_from_now)
    tt_fields_sort_by = models.CharField(max_length=50, default="-date")
    tt_search_bar = models.CharField(max_length=50, default="''")
    tt_user_filter = models.CharField(max_length=50, default="all")
    tt_project_filter = models.CharField(max_length=50, default="all")

    ms_project_filter = models.CharField(max_length=50, default="all")
    ms_status_filter = models.CharField(max_length=50, default="all")
    ms_date_range_start = models.DateField(blank=True, null=True)
    ms_date_range_end = models.DateField(blank=True, null=True)
    ms_sort_field = models.CharField(max_length=50, blank=True)
    ms_sort_ascending = models.BooleanField(max_length=50, default=False)

    pulse_state = models.CharField(max_length=50, default="collapse")
    pulse_btn_class = models.CharField(max_length=50, default="fa-plus")
    pulse_body_style = models.CharField(max_length=50, default="display:none;")

    def __str__(self):
        try:
            name = self.tester_set.get().user.username
        except:
            return "None's context"
        else:
            return "%s's context" % (name)


class Tester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.IntegerField(default=1)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    avatar = models.FileField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
        default="%simages/avatar_default.png" % (settings.STATIC_URL),
    )
    scratchpad = models.ForeignKey(Scratchpad, blank=True, null=True)
    last_project = models.CharField(max_length=1000, blank=True, null=True)
    project = models.ForeignKey(
        Project, blank=True, null=True, on_delete=models.SET_NULL
    )
    issues = GenericRelation(Issue, related_query_name="tester_owner")
    context = models.ForeignKey(Context, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    review = models.BooleanField(default=False, blank=True)

    @property
    def avatar_thumb(self):
        return (
            '<img src="%s" width="20px" height="20px" style="margin:0px 5px 3px 0px;">'
            % (self.avatar.url)
        )

    @property
    def phone(self):
        if self.phone_number:
            return "%s-%s-%s" % (
                self.phone_number[:3],
                self.phone_number[3:6],
                self.phone_number[6:],
            )
        else:
            return ""

    def project_count(self):
        return self.user.project_set.count()

    def note_count(self):
        return self.user.note_set.count()

    def issue_count(self):
        technical_poc = list(self.user.technical_poc.values_list("id", flat=True))
        issue_author = list(self.user.issue_set.values_list("id", flat=True))
        issue_owner = list(self.issues.values_list("id", flat=True))
        complete_list = technical_poc + issue_owner + issue_author

        return len(set(complete_list))

    def time_logged(self):
        time = Decimal(0.00)
        time_entries = self.user.timetracker_set.aggregate(
            Sum(F("time"))
        )["time__sum"]
        if time_entries is None:
            return time
        else:
            return time_entries
