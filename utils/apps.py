from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class UtilsConfig(AppConfig):
    name = "hv.utils"
    verbose_name = _("utils")

    def ready(self):
        from hv.utils.signals import make_milestone_guid
