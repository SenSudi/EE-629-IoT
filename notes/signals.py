from django.db.models.signals import post_save
from notes.models import Note
import hv.settings

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


def alert_pm(sender, instance, **kwargs):
    if not hv.settings.SEND_EMAIL_ON_NOTE_SAVE:
        return

    body = "Time for %s:\n%s - %s" % (
        instance.creator.get_full_name(),
        instance.date,
        instance.time,
    )
    msg = MIMEText(body)
    FROM = hv.settings.SEND_EMAIL_ON_NOTE_SAVE_FROM
    TO = hv.settings.SEND_EMAIL_ON_NOTE_SAVE_TO
    msg["Subject"] = "Time for %s" % instance.creator.get_short_name()
    msg["From"] = FROM
    msg["To"] = TO

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(FROM, [TO], msg.as_string())
    s.quit()


post_save.connect(alert_pm, sender=Note)
