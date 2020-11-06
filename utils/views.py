from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core import serializers
import datetime as dt
from datetime import datetime

# from os import system as sys
import subprocess
import sys

# Create your views here.
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR
from django.contrib.auth.decorators import login_required

from models import Time_Object as TO
from tasks.models import Task

# from project.views import table_formatter
from project.views import get_context_items

from formutils import input_list

"""
*The User model is how django classifies a person.
*The login_required decorator can be placed just above a view definition
    in order to force django to check for a logged in user.
*Authenticate, login, and logout are predefined django methods for interacting
    with the security context processors.
"""
context = {}
now = datetime.today


def make_time(start, time):
    HH = time / 3600
    MM = (time % 3600) / 60
    SS = (time % 3600) % 60

    final = start - dt.timedelta(seconds=time)
    return final
    # return timezone.make_aware(final,timezone.get_current_timezone())


# def get_timezone.make_aware(now(),time_zone.get_current_timezone()):
#     p = subprocess.Popen(['TZ=America/New_York date'], stdout=subprocess.PIPE, shell=True)
#     (out, err) = p.communicate()
#     if out:
#         #print type(out[:-1])
#         string = out[0:20] + out[24:28]
#         return lt(datetime.strptime(string,'%a %b %d %H:%M:%S %Y'))
#     else:
#         return err


def login_user(request):
    context = {}
    logout(request)
    username = password = ""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HRR("/")
        else:
            context = {"error": "Incorrect User Name or Password"}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return HRR("/")


@login_required(login_url="/login/")
def startsession(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        if task_id:
            task = Task.objects.get(pk=task_id)
            if task.session == False:
                if task.session_time:
                    session = task.session_time
                    session.start_time = make_time(
                        timezone.make_aware(now(), timezone.get_current_timezone()),
                        session.aggregate,
                    )
                    session.save()
                else:
                    new_session = TO(
                        start_time=timezone.make_aware(
                            now(), timezone.get_current_timezone()
                        )
                    )
                    new_session.save()
                    task.session_time = new_session
                # Set the active session flag.
                task.session = True
                task.save()
                # print task.__dict__
                return HR(task.session_time.start_time)
            else:
                return HR("Task already has session!")
        else:
            return HR("No Task!")
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def pausesession(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        if task_id:
            task = Task.objects.get(pk=task_id)
            if task.session:
                session = task.session_time
                session.aggregate = int(
                    (
                        timezone.make_aware(now(), timezone.get_current_timezone())
                        - session.start_time
                    ).total_seconds()
                )
                session.save()
                # Clear the active session flag.
                task.session = False
                task.save()
                return HR(session.aggregate)
            else:
                HR("No Session To Pause!")
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def stopsession(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        if task_id:
            task = Task.objects.get(pk=task_id)
            session = task.session_time

            # Total int seconds of the most current portion of the session.
            current_total = int(
                (
                    timezone.make_aware(now(), timezone.get_current_timezone())
                    - session.start_time
                ).total_seconds()
            )
            if session.aggregate > 0:
                # Total int seconds of the aggregate field.
                aggregate_total = int(session.aggregate)
                # The actual session total in int seconds.
                session_total = aggregate_total + current_total
            else:
                session_total = current_total
            task.tsk_duration += session_total
            # Clear session.
            session.delete()
            # Clear the active session flag
            task.session_time = None
            task.session = False
            task.save()
            return HR("successful stop")
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def getsession(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        if task_id:
            task = Task.objects.get(pk=task_id)
            session = task.session_time
            # Total int seconds of the most current portion of the session.
            current_total = int(
                (
                    timezone.make_aware(now(), timezone.get_current_timezone())
                    - session.start_time
                ).total_seconds()
            )
            if session.aggregate > 0:
                # Total int seconds of the aggregate field.
                aggregate_total = int(session.aggregate)
                # The actual session total in int seconds.
                session_total = aggregate_total + current_total
                return HR(session.start_time)
            else:
                return HR(session.start_time)
    return HR("Not Authorized")


@login_required(login_url="/login/")
def get_import_table_data(request):
    project = context["project"]
    table = project.import_table_set.get()
    return JR({"columns": "blah"})


@login_required(login_url="/login/")
def get_form(request):
    form_name = request.GET.get("form", False)
    app = request.GET.get("app", False)
    form_id = request.GET.get("form_id", False)
    model_id = request.GET.get("id", False)
    model_type = request.GET.get("model_type", False)
    model_app = request.GET.get("model_app", False)
    data_type = request.GET.get("data_type", False)
    arg = request.GET.get("arg", False)
    if form_name and app:
        form = getattr(sys.modules["%s.forms" % app], "%s" % form_name)
        if model_id and model_type and model_app:
            model = getattr(sys.modules["%s.models" % model_app], "%s" % model_type)
            instance = get_object_or_404(model, id=model_id)
            if arg:
                instance_form = form(
                    instance=instance, project=request.user.tester.project
                )
            else:
                instance_form = form(instance=instance)
            if model_type == "Note":
                instance_form.fields["title"].initial = instance.title
                instance_form.fields["body"].initial = instance.body
            for field in instance_form.fields:
                if "date" in field:
                    instance_form.fields[field].input_formats = input_list
            context["form"] = instance_form
        else:
            if arg:
                form = form(project=request.user.tester.project)
            else:
                form = form()
            for field in form.fields:
                if "date" in field:
                    form.fields[field].input_formats = input_list
            context["form"] = form
        if form_id:
            context["form_id"] = form_id
        if data_type:
            if data_type == "json":
                # data = serializers.serialize(data_type,instance_form)
                return JR({"form": str(instance_form)})
        return render(request, "model_form.html", context)
    else:
        return HR("form name:%s app: %s")


# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from forms import FeedbackForm
from models import Feedback


@login_required(login_url="/login/")
def send_feedback(request):
    if request.method == "POST":
        # Constants
        COMMASPACE = ", "
        RECIPIENT = "hv@leetsys.com"
        # Variables
        errors = {}
        subject = request.POST.get("subject", False)
        sender = request.user.email
        body = request.POST.get("body", False)

        if not subject:
            errors["subject"] = "Subject Required"
        if not sender or sender == "" or " " in sender:
            errors["sender"] = "Please Set Your Email Under User Profile"
        if not body:
            errors["body"] = "Please Enter Some Text"

        # If all relevant data is present
        if errors == {}:
            """
            # Create the container (outer) email message.
            msg = MIMEMultipart()
            
            msg['Subject']  = subject
            msg['From']     = sender
            msg['To']       = RECIPIENT
            msg['Date']     = formatdate(timezone.now())
            msg.preamble    = MIMEText(body)

            files = request.FILES.getlist('feedback_files',False)
            if files:
                for file in files:
                    with open(file, 'rb') as f:
                        part = MIMEApplication(
                            f.read(),
                            Name=file.name)
                        part['Content-Disposition'] = 'attachment; filename="%s"'%file.name
                        msg.attach(part)

            # Send the email via our own SMTP server.
            s = smtplib.SMTP('localhost')
            s.sendmail(sender,RECIPIENT,msg.as_string())
            s.close()
            """
            fb = Feedback()
            fb.subject = subject
            fb.body = body
            fb.sender = request.user
            fb.current_page = ("%s") % (
                request.build_absolute_uri(request.META["HTTP_REFERER"])
            )
            files = request.FILES.getlist("feedback_files", False)
            if files:
                for file in files:
                    fb.supporting_file = file
            fb.save()
            return JR({"success": "Thanks for your feedback!"})
        else:
            return JR({"errors": errors})
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def feedback(request):
    get_context_items(context, request)
    request.user.tester.project = None
    context["section"] = "Feedback"
    context["feedback"] = Feedback.objects.all()
    context["page_controls"] = True
    return render(request, "feedback.html", context)


def generic_delete_form(request):
    context = {}
    context["title"] = request.GET.get("title", "A real model instance")
    context["model"] = request.GET.get("model", "Model Type").replace("_", " ").title()
    context["content"] = request.GET.get("content", None)
    return render(request, "generic_delete_modal.html", context)


def generic_delete(request):
    oid = request.POST.get("id", None)
    app = request.POST.get("app", None)
    model = request.POST.get("model", None)
    if app and model:
        manager = getattr(sys.modules["%s.models" % app], model)
        instance = get_object_or_404(manager, id=oid)
        instance.delete()
        return JR({"success": "success"})
    else:
        return JR({"errors": "no app or model"})
