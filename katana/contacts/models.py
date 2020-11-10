from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models

from project.models import Project
from issuetracker.models import Issue

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    project = models.ManyToManyField(Project, blank=True)
    role = models.ManyToManyField("utils.Label", blank=True)
    issues = GenericRelation(Issue, related_query_name="contact_owner")
    project_roles = GenericRelation("project.VIP")

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    type_label = "contact"
    app_label = "contacts"
    model_class = "Contact"
    details_url = "/contact_details/"
    edit_url = "/contact_update_form/"
    delete_url = "/contact_delete/"

    def get_client(self):
        return list(self.client_set.all())[0]

    @property
    def whole_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_roles(self):
        return list(self.project_roles.all())

    def get_role_ids(self):
        return list(self.project_roles.values_list("role__id", flat=True))
