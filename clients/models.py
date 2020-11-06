from __future__ import unicode_literals

from django.db import models

from contacts.models import Contact

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, default="Default Client")
    contacts = models.ManyToManyField(Contact, blank=True)

    def __str__(self):
        return "%s" % self.name

    @property
    def has_active_project(self):
        flag = False
        for project in self.project_set.all():
            if project.active:
                flag = True
        return flag

    @property
    def contacts_count(self):
        count = self.contacts.all().count()
        return count

    @property
    def projects_count(self):
        count = self.project_set.all().count()
        return count

    @property
    def active_projects_count(self):
        count = 0
        for project in self.project_set.all():
            if project.active:
                count += 1
        return count
