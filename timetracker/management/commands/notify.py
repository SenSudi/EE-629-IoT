# Standard Library
import os
import shutil
import zipfile
import json
from copy import deepcopy
import datetime
from subprocess import check_output
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

# Django
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Periodically updates the user to notify them of weekly hours'

    def add_arguments(self, parser):
        parser.add_argument(
            '-hn',
            dest='hostname',
            help='system hostname',
        )
        parser.add_argument(
            '-u',
            dest='username',
            help='username of the tester to notify',
        )

    def handle(self, *args, **options):
        if options.get('username',False):
            USER_LIST = [options['username']]
        else:
            USER_LIST = ['jg','cm']
        if options.get('hostname',False):
            HOSTNAME = options['hostname']
        else:
            HOSTNAME = check_output(['hostname']).rstrip()
        
        start = timezone.now() + timezone.timedelta(-7)
        end = timezone.now()

        for username in USER_LIST:
            u = User.objects.get(username=username)
            if not u.tester.review:
                u.tester.review = True
                u.tester.save()
            entries = u.timetracker_set.filter(
                        date__range=[start,end],
                        newest=True
                    )
            hours = entries.aggregate(Sum('time'))['time__sum']
            body = ( 
'''
Hello %s,

Please log in to review and approve your hours for the week.
I calculate your current total on %s to be: %s hours
If this is correct, please visit the time tracker to approve.

Thank you and have a nice day!

Sincerely,
---------------------
Katana
CS Management Arsenal
Leet Cyber Security
'''%(u.get_full_name(),HOSTNAME,hours))
            msg             = MIMEText(body)
            FROM            = 'katana@leetsys.com'
            TO              = u.email
            msg['Subject']  = 'Weekly Commission Approval'
            msg['From']     = FROM
            msg['To']       = TO

            # Send the message via our own SMTP server, but don't include the
            # envelope header.
            s               = smtplib.SMTP()
            s.connect()
            s.sendmail(FROM, [TO], msg.as_string())
            s.quit()