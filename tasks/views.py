import time
from django.shortcuts import render, get_object_or_404
from project.views import get_context_items
from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from auditor.views import action_audit
from auditor.utils import initial_audits

from forms import TaskForm as TF
from forms import TaskEditForm as TEF

from notes.forms import NoteForm as NF
from files.forms import FileUploadForm as FUF

from notes.models import Note
from files.models import Associated_File as AF

from task_utils import *

context = {}

###############################################################################
@login_required(login_url="/login/")
def workflow(request):
    get_context_items(context, request)
    project = request.user.tester.project
    context["section"] = "Workflow"
    if request.method == "POST":
        form = TF(request.POST)
        if form.is_valid():
            phase = Phase.objects.get(title=str(request.POST.get("phase", "")))
            new_task = form.save(commit=False)
            new_task.phase = phase
            new_task.project = project
            new_task.status = "open"
            new_task.save()
            task = Task.objects.get(title=request.POST.get("title", ""))
            task_dict = vars(task)
            task_dict.pop("_state", None)
            task_dict["phase"] = str(request.POST.get("phase", ""))
            return JR({"task": task_dict})
    note_form = NF()
    context["note_form"] = note_form
    form = TF()
    fileform = FUF()
    context["fileform"] = fileform
    context["form"] = form
    context["project"] = project
    context["audits"] = initial_audits(project, "workflow", 10)
    context["where"] = "workflow"
    context["title"] = "Workflow"
    context["workflow"] = True
    context["phases"] = project.phase_set.all().order_by("sequence")
    return render(request, "new_workflow.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_t_n_c(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    context["task"] = task
    return render(request, "task_notes_panel.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_t_f_c(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    context["task"] = task
    return render(request, "task_files_panel.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_t_t_c(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    context["task"] = task
    context["edit_class"] = "btn-modal-entry-edit"
    return render(request, "task_entries_panel.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_reload_phases(request):
    ph = request.GET.get("phase_filter", False)
    project = request.user.tester.project
    if ph != "False" and ph != "all":
        context["phases"] = project.phase_set.filter(id=ph)
    else:
        context["phases"] = project.phase_set.all().order_by("sequence")
    return render(request, "display_phases.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_add_form(request):
    form = TF()
    form.fields["title"].required = True
    user = request.user
    project = user.tester.project
    context["project"] = project
    context["form"] = form
    context["action"] = "/wf_task_add/"
    context["phases"] = project.phase_set.all().order_by("sequence")
    context["add"] = True
    context["multiple"] = False
    context["select"] = [int(request.GET.get("pid", -1))]
    context["form_id"] = "form-wf-task-add"
    return render(request, "wf_task_add_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_add(request):
    if request.method == "POST":
        project = request.user.tester.project
        phases = request.POST.getlist("phases", [])
        if len(phases) > 0:
            for pid in phases:
                phase = Phase.objects.get(id=pid)
                form = TF(request.POST)
                if form.is_valid():
                    task = form.save(commit=False)
                    task.guid = get_guid()
                    task.lineage_guid = get_guid()
                    task.phase = phase
                    task.project = project
                    task.save()
                    for file in request.FILES.getlist("associated_files", []):
                        new_file = AF()
                        new_file.filename = file.name
                        new_file.file = file
                        new_file.subdirectory = "%s/tasks/%s" % (project.id, task.id)
                        new_file.uploader = request.user
                        new_file.associated_item = task
                        new_file.guid = get_guid()
                        new_file.a_i_guid = task.guid
                        new_file.save()
                        # Accout for audit -> user added task with # files (if > 0) to phase
                    return JR({"success": "success"})
                else:
                    return JR({"errors": form.errors})
        else:
            return JR({"errors": {"phases": "Please select a phase!"}})
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def wf_task_edit_form(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    form = TEF(instance=task)
    context["form"] = form
    context["task"] = task
    context["edit"] = True
    context["action"] = "/wf_task_update/"
    context["form_id"] = "form-wf-task-update"
    context["recommend"] = True
    context["project"] = task.project
    return render(request, "wf_task_edit_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_update(request):
    if request.method == "POST":
        tid = request.POST.get("id", False)
        task = get_object_or_404(Task, id=tid)
        project = request.user.tester.project
        form = TEF(request.POST, instance=task)
        if form.is_valid():
            updated = form.save()
            fids = request.POST.getlist("files", [])
            # return JR({'errors':{'files':fids}})
            if len(fids) > 0:
                for fi in updated.files.all():
                    # fi.content_type = None
                    fi.object_id = None
                    fi.save()
                for fid in fids:
                    current_file = AF.objects.get(id=fid)
                    current_file.associated_file = updated
                    current_file.save()
                    updated.files.add(current_file)
            else:
                for fi in updated.files.all():
                    # fi.content_type = None
                    fi.object_id = None
                    fi.save()
            for file in request.FILES.getlist("associated_files", []):
                new_file = AF()
                new_file.filename = file.name
                new_file.file = file
                new_file.subdirectory = "%s/tasks/%s" % (project.id, updated.id)
                new_file.uploader = request.user
                new_file.associated_item = updated
                new_file.guid = get_guid()
                new_file.a_i_guid = updated.guid
                new_file.save()
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors})
    else:
        return HR("not authorized")


###############################################################################
@login_required(login_url="/login/")
def task_files_select(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    context["task"] = task
    context["files"] = task.files.all()
    return render(request, "task_files_select.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_suggest(request):
    user = request.user
    project = user.tester.project
    tid = request.POST.get("id", False)
    task = get_object_or_404(Task, id=tid)
    fids = request.POST.getlist("file_ids[]", [])
    # Method creation from task data
    new_method = task_to_method(task)
    new_method.recommend = True
    new_method.suggestor = user
    new_method.save()
    # If the task has a parent method: handle liniage ordering
    if task.has_parent():
        parent = task.meth_item
        new_method.ancestor = parent
        parent.descendant = new_method
        new_method.phase = parent.phase
        new_method.save()
        parent.save()
        for pt in parent.project_type.all():
            new_method.project_type.add(pt)
    else:
        if task.phase.parent_guid != None:
            new_method.phase = Phase.objects.get(guid=task.phase.parent_guid)
        new_method.save()
        new_method.project_type.add(project.project_type)
        # If the user chose to submit files with recommended task
    for fid in fids:
        file = AF.objects.get(id=int(fid))
        new_file = AF()
        new_file.guid = get_guid()
        new_file.filename = file.filename
        new_file.file = file.file
        new_file.subdirectory = "methodology"
        new_file.uploader = request.user
        new_file.associated_item = new_method
        new_file.save()
        new_method.files.add(new_file)

    return JR({"success": "Task was sent to Admin for review!", "sidenav": "reload"})


###############################################################################
@login_required(login_url="/login/")
def wf_task_files_modal(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    files = task.files.all()
    form = FUF()
    context["title"] = "Files for task <b>%s</b>" % task.title
    context["files"] = files
    context["action"] = "/wf_task_file_add/"
    context["form_id"] = "form-task-file-add"
    context["form"] = form
    return render(request, "task_files_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_files_list(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    files = task.files.all()
    context["files"] = files
    return render(request, "files_list.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_notes_list(request):
    tid = request.GET.get("id", False)
    task = get_object_or_404(Task, id=tid)
    notes = task.notes.filter(newest=True)
    container_class = request.GET.get("container_class", False)
    context["container_class"] = container_class
    context["notes"] = notes
    return render(request, "note_list_display.html", context)


###############################################################################
@login_required(login_url="/login/")
def wf_task_file_add(request):
    if request.method == "POST":
        tid = request.POST.get("id", False)
        task = get_object_or_404(Task, id=tid)
        files = request.FILES.getlist("associated_files", [])
        project = request.user.tester.project
        if files:
            for file in files:
                new_file = AF()
                new_file.filename = file.name
                new_file.file = file
                new_file.subdirectory = "%s/tasks/%s" % (project.id, task.id)
                new_file.uploader = request.user
                new_file.associated_item = task
                new_file.guid = get_guid()
                new_file.a_i_guid = task.guid
                new_file.save()
            return JR({"success": "success"})
        else:
            return JR(
                {"errors": {"associated_files": "Please select a file to upload"}}
            )
    else:
        return HR("not authorized")


###############################################################################
@login_required(login_url="/login/")
def new_task(request):
    if request.method == "POST":
        project = request.user.tester.project  # context['project']
        phase_id = request.POST.get("phase", False)
        form = TF(request.POST)
        if form.is_valid():
            if phase_id:
                new_task = form.save(commit=False)
                phase = Phase.objects.get(id=phase_id)
                new_task.project = project
                new_task.phase = phase
                new_task.status = "open"
                new_task.save()
                audit = action_audit(
                    request.user,
                    "added %s to %s" % (new_task.title, phase.title),
                    "workflow",
                    timezone.now(),
                    project,
                    new_task,
                )
                return HRR("/display_tasks/?id=%s" % phase_id)
            else:
                return HR("No Phase Selected!")
        else:
            return HR("Invalid Form!")
    else:
        return HR("Not Authorized!")


@login_required(login_url="/login/")
def task_info(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        if task_id:
            task = Task.objects.get(pk=task_id)
            notes_list = []
            if Note.objects.filter(task__id=task_id).count() > 0:
                # for note in task.note_set.all():
                for note in Note.objects.filter(task__id=task_id):
                    note_dict = {}
                    note_dict = note.__dict__
                    note_dict["creator"] = note.creator.username
                    note_dict.pop("_state", None)
                    note_dict.pop("_task_cache", None)
                    note_dict.pop("_creator_cache", None)
                    notes_list.append(note_dict)
            file_list = []
            if AF.objects.filter(task__id=task_id).count() > 0:
                for file in AF.objects.filter(task__id=task_id):
                    file_dict = {}
                    idx = file.file.name.rfind(".")
                    slash = file.file.name.rfind("/")
                    file_dict["name"] = file.file.name[slash + 1 : idx]
                    file_dict["url"] = file.file.url
                    file_dict["type"] = file.file.name[idx:]
                    try:
                        file_dict["uploader"] = file.uploader.username
                    except:
                        file_dict["uploader"] = "System"
                    file_dict["updated"] = file.updated.date()
                    file_list.append(file_dict)
            task_info = task.__dict__
            task_info.pop("_state", None)
            return JR({"task": task_info, "notes": notes_list, "files": file_list})
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def task_details(request):
    task_id = request.GET.get("id", False)
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        context["task"] = task
        return render(request, "task_details.html", context)
    else:
        return HR("No Task!")


@login_required(login_url="/login/")
def task_total_time(request):
    task_id = request.GET.get("id", False)
    task = get_object_or_404(Task, id=task_id)
    total_time = task.total_time
    return HR(total_time)


@login_required(login_url="/login/")
def task_file_upload(request):
    if request.method == "POST":
        file_list = []
        # print request.POST
        model_id = request.POST.get("model_id", None)
        model_type = request.POST.get("model_type", None)
        app = request.POST.get("app", None)
        task = get_object_or_404(Task, id=model_id)
        for file in request.FILES.getlist("associated_files", []):
            new_file = AF()
            new_file.filename = file.name
            new_file.file = file
            new_file.subdirectory = "%s/tasks/%s" % (
                request.user.tester.project.id,
                task.id,
            )
            new_file.uploader = request.user
            new_file.associated_item = task
            new_file.save()
            audit = action_audit(
                request.user,
                "added %s to %s" % (new_file.filename, task.title),
                "workflow",
                timezone.now(),
                request.user.tester.project,
                new_file,
            )
        return HRR(
            "/files_list/?app=%s&model_id=%s&model_type=%s"
            % (app, model_id, model_type)
        )
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def task_vars(request):
    if request.method == "POST":
        var_name = request.POST.get("var_name", False)
        if var_name:
            task_id = request.POST.get("task_id", False)
            if task_id:
                var_dict = {}
                var_list = []
                task = Task.objects.get(id=task_id)
                task_vars = task.variables.all()
                for item in task_vars:
                    var_list.append(str(item.value))
                var_dict["variables"] = var_list
                return JR(var_dict)
            else:
                return HR("No Task ID!")
        else:
            return HR("No Variable Name!")
    else:
        return HR("Not Authorized!")


@login_required(login_url="/login/")
def task_update(request):
    tid = request.POST.get("id", None)
    sequence = request.POST.get("seq", False)
    if sequence:
        task = get_object_or_404(Task, id=tid)
        task.sequence = sequence
        task.save()
        return JR({"success": "success"})
    else:
        return JR({"error": "no sequence"})


@login_required(login_url="/login/")
def task_state(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", False)
        if task_id:
            task = Task.objects.get(id=task_id)
            old_state = task.status
            state = request.POST.get("state", False)
            if state:
                task.status = state
                task.save()
                # task_dict = vars(task)
                # task_dict.pop('_state',None)
                # return JR(task_dict)
                context["task"] = task
                audit = action_audit(
                    request.user,
                    "changed the state of %s from %s to %s"
                    % (task.title, old_state, task.status),
                    "workflow",
                    timezone.now(),
                    task.project,
                    task,
                )
                return render(request, "task_state.html", context)
            else:
                return HR("No State!")
        else:
            return HR("No Task!")
    else:
        return HR("Not Authorized!")


@login_required(login_url="/login/")
def display_tasks(request):
    phase_id = request.GET.get("id", False)
    if phase_id:
        phase = get_object_or_404(Phase, id=phase_id)
        context["tasks"] = phase.task_set.filter(
            project=request.user.tester.project
        ).order_by("sequence")
    return render(request, "display_tasks.html", context)


@login_required(login_url="/login/")
def get_task_notes(request):
    time.sleep(5)
    task_id = request.GET.get("id", False)
    task = get_object_or_404(Task, id=task_id)
    task = Task.objects.get(id=task.id)
    notes = task.notes.filter(newest=True)
    context["notes"] = notes
    context["edit_class"] = "modal-task-note-edit"
    return render(request, "display_notes.html", context)


@login_required(login_url="/login/")
def task_delete(request):
    task_id = request.POST.get("id", False)
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JR({"success": "success"})
