from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    subject = models.CharField(max_length=50)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True)
    is_draft = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_sender"
    )
    recipient = models.ManyToManyField(User, related_name="message_recipient")


class Inbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ManyToManyField(Message)
