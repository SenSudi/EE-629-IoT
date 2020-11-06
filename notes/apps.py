from __future__ import unicode_literals

from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = "notes"

    def ready(self):
        import notes.signals
