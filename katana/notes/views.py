import sys
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR
from project.views import get_context_items
from django.utils import timezone
from decimal import Decimal
from django.db.models import F
from auditor.views import action_audit

from models import Note, Narrative
from forms import NoteForm as NF

from issuetracker import models

from tasks.models import Task

from django.contrib.contenttypes.models import ContentType

from utils.formutils import input_list

context = {}

# Create your views here.
################################################################################
@login_required(login_url="/login/")
def narrative(request):
    user = request.user
    project = user.tester.project
    narrative = Narrative()
    narrative.body = request.POST.get("body", " ")
    narrative.creator = user
    narrative.project = project
    narrative.save()
    return JR({"success": "success"})


################################################################################
@login_required(login_url="/login/")
def project_notes(request):
    get_context_items(context, request)
    user = request.user
    project = user.tester.project
    context["notes"] = project.note_set.all()
    context["section"] = "Project Notes"
    context["page_controls"] = True
    return render(request, "project_notes.html", context)


################################################################################
@login_required(login_url="/login/")
def note_add(request):
    if request.method == "POST":
        user = request.user
        form = NF(request.POST)
        app = request.POST.get("app", False)
        model = request.POST.get("model", False)
        uid = request.POST.get("id", False)
        where = request.POST.get("where", False)
        if app and model and uid:
            instance = getattr(
                sys.modules["%s.models" % app], "%s" % model
            ).objects.get(id=uid)
            if form.is_valid():
                note = form.save(commit=False)
                note.creator = user
                note.project = user.tester.project
                note.associated_item = instance
                note.newest = True
                note.save()
                audit = action_audit(
                    request.user,
                    "added note - %s to %s" % (note.title, instance.audit_label),
                    where,
                    timezone.now(),
                    note.project,
                    note,
                )
                return JR({"success": "success"})
            else:
                return JR({"errors": form.errors})
        else:
            return JR({"errors": "incorrect data"})
    else:
        return HR("Not Authorized")


################################################################################
@login_required(login_url="/login/")
def note_add_form(request):
    form = NF()
    context["form"] = form
    context["cancel_class"] = request.GET.get("cancel_class", "")
    context["form_id"] = request.GET.get("form_id", "")
    context["submit_id"] = request.GET.get("submit_id", "")
    return render(request, "note_add_form.html", context)


################################################################################
@login_required(login_url="/login/")
def note_edit(request):
    if request.method == "POST":
        user = request.user
        uid = request.POST.get("id", False)
        where = request.POST.get("where", False)
        instance = get_object_or_404(Note, id=uid)
        form = NF(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.associated_item = instance.associated_item
            note.ancestor = instance
            note.project = instance.project
            note.creator = user
            note.newest = True
            note.save()
            instance.newest = False
            instance.child = note
            instance.save()
            audit = action_audit(
                user,
                "updated note - %s" % (note.title),
                where,
                timezone.now(),
                note.project,
                note,
            )
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors})
    else:
        return HR("Not Authorized")


################################################################################
@login_required(login_url="/login/")
def note_edit_form(request):
    nid = request.GET.get("id", False)
    note = get_object_or_404(Note, id=nid)
    form = NF(instance=note)
    context["form"] = form
    return render(request, "note_edit_form.html", context)


################################################################################
@login_required(login_url="/login/")
def add_note(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        model_id = request.POST.get("id", False)
        model_type = request.POST.get("model_type", False)
        app = request.POST.get("app", False)
        where = request.POST.get("where", False)
        header = request.POST.get("header", False)
        if model_id and model_type:
            # check https://docs.djangoproject.com/en/1.10/ref/contrib/contenttypes/ ContentType.model_class()
            model = getattr(
                sys.modules["%s.models" % app], "%s" % model_type
            ).objects.get(id=model_id)
            form = NF(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.associated_item = model
                note.creator = request.user
                note.project = request.user.tester.project
                note.newest = True
                note.save()
                context["model_type"] = model_type
                context["model_id"] = model_id
                if where:
                    audit = action_audit(
                        request.user,
                        "added note - %s to %s" % (note.title, model.title),
                        where,
                        timezone.now(),
                        note.project,
                        note,
                    )
                if header:
                    return HRR(
                        "/get_notes_list/?app=%s&model_type=%s&model_id=%s&header=%s"
                        % (app, model_type, model_id, header)
                    )
                else:
                    return HRR(
                        "/get_notes_list/?app=%s&model_type=%s&model_id=%s"
                        % (app, model_type, model_id)
                    )
        else:
            return HR("No Item!")
    else:
        return HR("Not Authorized!")


################################################################################
@login_required(login_url="/login/")
def note_info(request):
    note_id = request.GET.get("id", False)
    note = get_object_or_404(Note, id=note_id)
    context["note"] = note
    return render(request, "note_details.html", context)


################################################################################
@login_required(login_url="/login/")
def get_notes_list(request):
    m_type = request.GET.get("model_type", False)
    mid = request.GET.get("model_id", False)
    app = request.GET.get("app", False)
    if m_type and id and app:
        model = getattr(sys.modules["%s.models" % app], "%s" % m_type).objects.get(
            id=mid
        )
        ct = ContentType.objects.get_for_model(model)
        notes = Note.objects.filter(
            object_id=mid, content_type=ct, newest=True
        ).order_by("-created")
        context["notes"] = notes
        return render(request, "note_list.html", context)
    else:
        return HR("Not Authorized")


################################################################################
@login_required(login_url="/login/")
def get_note_form(request):
    form = NF()
    context["form"] = form
    return render(request, "model_form.html", context)


################################################################################
@login_required(login_url="/login/")
def update_note(request):
    if request.method == "POST":
        user = request.user
        note_id = request.POST.get("id", None)
        instance = get_object_or_404(Note, id=note_id)
        form = NF(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.associated_item = instance.associated_item
            note.ancestor = instance
            note.project = instance.project
            note.creator = user
            note.newest = True
            note.save()
            instance.newest = False
            instance.child = note
            instance.save()
            model_id = note.associated_item.id
            model_type = request.POST.get("model_type", "")
            app = request.POST.get("app", "")
            header = request.POST.get("header", "")
            where = request.POST.get("where", False)
            if where:
                audit = action_audit(
                    request.user,
                    "updated note - %s" % (note.title),
                    where,
                    timezone.now(),
                    note.project,
                    note,
                )
            return HRR(
                "/get_notes_list/?app=%s&model_type=%s&model_id=%s&header=%s"
                % (app, model_type, model_id, header)
            )
        else:
            return HR("Form is not valid!")
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def scratch_pad(request):
    user = request.user
    if request.method == "GET":
        scratch = user.tester.scratchpad
        return render(request, "user_scratchpad.html", context)
    if request.method == "POST":
        scratch = request.POST.get("scratch", False)
        # print scratch
        if scratch:
            user.tester.scratchpad.body = scratch
            user.tester.scratchpad.save()
            return HR("success")
        else:
            return HR("nothing to save")
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def scratchpad(request):
    user = request.user
    context["title"] = "Scratch Pad"
    context["body"] = user.tester.scratchpad.body
    return render(request, "scratchpad.html", context)


###############################################################################
@login_required(login_url="/login/")
def scratchpad_update(request):
    if request.method == "POST":
        tester = request.user.tester
        errors = {"errors": "no scratch!"}
        scratch = request.POST.get("scratch", False)
        if scratch:
            try:
                pad = tester.scratchpad
            except:
                errors["errors"] = "You have no scratch pad!"
                return JR(errors)
            else:
                scratch.replace("\\n", "\n")
                scratch.replace("&nbsp;", " ")
                pad.body = scratch
                pad.save()
                return JR({"success": "atuosaving..."})
        else:
            return JR(errors)
    else:
        return HR("not authorized")


###############################################################################
