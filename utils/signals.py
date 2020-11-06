from django.db.models.signals import post_save
from django.dispatch import receiver

from hv.utils.tools import get_guid


@receiver(post_save, sender="project.Milestone")
def make_milestone_guid(sender, instance, created, **kwargs):
    if created:
        instance.guid = get_guid()
        instance.save()
