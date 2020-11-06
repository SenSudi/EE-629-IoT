from utils.imports import *

from project.views import get_context_items

from forms import MethodForm as MF
from forms import MethodUpdateForm as MUF
from forms import ProjectTypeForm as PTF
from forms import PhaseForm as PhF
from forms import PhaseUpdateForm as PhUF
from files.forms import ImportFileForm as IFF

from models import Method as M
from models import Method_Order
from models import Project_Type as PT
from models import Phase as Ph

from project.models import Project

from files.models import Associated_File as AF
from files.model_tools import save_new_afile

from tasks.task_utils import task_from_method

context = {}

# Create your views here.
###############################################################################
@login_required(login_url="/login/")
def suggest_method(request):
    user = request.user
    project = user.tester.project
    ptype = project.project_type
    # FINISH THIS
    return JR({"success": "Method was sent to Admin for review!"})


@login_required(login_url="/login/")
def suggest_phase(request):
    user = request.user
    project = user.tester.project
    ptype = project.project_type
    pid = request.POST.get("id", False)
    phase = get_object_or_404(Ph, id=pid)
    # If the phase is inherited from a methodology.
    if phase.parent_guid:
        # Call the methodology phase using the parent_guid.
        method_phase = Ph.objects.get(guid=phase.parent_guid)
        # Instantiate a new phase.
        new_phase = Ph()
        # Set the recommended flag to true.
        new_phase.recommend = True
        # Assign the methodology phase as the ancestor to the new one.
        new_phase.ancestor = method_phase
        # Set the title of the new phase to the title of the recommended phase.
        new_phase.title = phase.title
        # Set the sequence of the new phase to that of the recommended phase.
        new_phase.sequence = phase.sequence
        # Set the suggestor to the user making the request.
        new_phase.suggestor = user
        # Set a new guid for the new phase.
        new_phase.guid = get_guid()
        # Set the parent guid to the guid of the recommended phase.
        new_phase.parent_guid = phase.parent_guid
        new_phase.version = method_phase.version + Decimal(0.01)
        # Save the new phase.
        new_phase.save()
        # Set the descendant of the method phase to the new phase.
        method_phase.descendant = new_phase
        # Set the newest flag to false on the method phase.
        method_phase.newest = False
        method_phase.save()
        # Move all the methods to the new phase.
        # for method in method_phase.method_set.all():
        #     method.phase = new_phase
        #     method.save()
    else:
        new_phase = Ph()
        new_phase.recommend = True
        new_phase.title = phase.title
        new_phase.sequence = phase.sequence
        new_phase.suggestor = user
        new_phase.parent_guid = phase.guid
        new_phase.guid = get_guid()
        new_phase.save()
    ptype.phase.add(new_phase)
    return JR({"success": "Phase was sent to Admin for review!"})


###############################################################################
@login_required(login_url="/login/")
def get_method_form(request):
    context["form"] = MF()
    return render(request, "add_item_form.html", context)


###############################################################################
@login_required(login_url="/login/")
def method(request):
    get_context_items(context, request)
    form = MF()
    context["form"] = form
    methods_list = M.objects.all()
    context["Methods"] = methods_list
    return render(request, "method.html", context)


###############################################################################
@login_required(login_url="/login/")
def methodologies(request):
    user = request.user
    get_context_items(context, request)
    exports = AF.objects.filter(subdirectory="methodology/exports")
    context["exports"] = exports
    context["where"] = "methodologies"
    context["section"] = "Methodologies DB"
    context["project_types"] = PT.objects.filter(newest=True)
    context["methods"] = M.objects.all().order_by("orders__sequence")
    context["unassociated_methods"] = M.objects.filter(project_type=None, newest=True)
    if M.objects.filter(recommend=True).count() > 0:
        context["recommended"] = True
    return render(request, "methodologydb.html", context)


###############################################################################
@login_required(login_url="/login/")
def method_data_tree(request):
    context["project_types"] = PT.objects.all()
    context["methods"] = M.objects.all().order_by("orders__sequence")
    context["unassociated_methods"] = M.objects.filter(project_type=None, newest=True)
    return render(request, "db_display_method_tree.html", context)


###############################################################################
@login_required(login_url="/login/")
def method_details(request):
    method_id = request.GET.get("item_id", None)
    try:
        method = M.objects.get(id=method_id)
    except:
        pass
    if method:
        form = MUF(instance=method)
        context["form"] = form
        return render(request, "model_form.html", context)
    else:
        return HR("Failed to load form")


###############################################################################
@login_required(login_url="/login/")
def db_method_add_form(request):
    context = {}
    selected_ptypes = []
    if request.method == "POST":
        form = MF(request.POST)
        form.is_valid()
        p_types = form.cleaned_data["project_type"]
        choices = dict(form.fields["project_type"].choices)
        choice_keys = list(choices.keys())
        for p_type in p_types:
            selected_ptypes.append(choice_keys[choices.values().index(str(p_type))])
        phid = request.POST.getlist("id[]", False)
    else:
        form = MF()
        phid = request.GET.getlist("id[]", False)
    context["form"] = form
    context["action"] = "/db_method_add/"
    context["add"] = True
    context["form_id"] = "form-db-add-method"
    if phid:
        phid = int(phid[0])
        phase = get_object_or_404(Ph, id=phid)
        selected_phase = phase.id
        if not selected_ptypes:
            selected_ptypes = phase.project_type_set.values_list("id", flat=True)
        context["selected_phase"] = [selected_phase]
        context["selected_ptypes"] = selected_ptypes
        context["methods"] = M.objects.filter(phase__id=phid)
        form.fields["method"].choices = [("", "--------")] + [
            (x.id, x) for x in context["methods"]
        ]
    phases = Ph.objects.filter(newest=True).filter(project=None).order_by("sequence")
    ptypes = PT.objects.all().order_by("title")
    context["phases"] = phases
    context["ptypes"] = ptypes
    return render(request, "db_method_add_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_method_add(request):
    if request.method == "POST":
        form = MF(request.POST)
        if form.is_valid():
            position = form.cleaned_data["position"]
            method_position_id = form.cleaned_data["method"]

            method = form.save(commit=False)
            method.guid = get_guid()
            method.sequence = 1
            method.save()

            for pid in request.POST.getlist("project_type", []):
                ptype = get_object_or_404(PT, id=pid)
                method.project_type.add(ptype)
                if method_position_id:
                    method_position = M.objects.get(id=method_position_id)
                    if position == "before":
                        sequence = Method_Order.objects.get(
                            method__id=method_position.id,
                            phase__id=method.phase.id,
                            project_type__id=pid,
                        ).sequence
                    else:
                        sequence = (
                            Method_Order.objects.get(
                                method__id=method_position.id,
                                phase__id=method.phase.id,
                                project_type__id=pid,
                            ).sequence
                            + 1
                        )
                else:
                    sequence = 1
                method.set_sequence(sequence, method.phase.id, pid)

            if request.FILES.getlist("associated_files", False):
                for file in request.FILES.getlist("associated_files", False):
                    subdirectory = "methodology"
                    guid = method.guid
                    new_file = save_new_afile(file, subdirectory, guid)
                    method.files.add(new_file)
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors})
    else:
        return HR("not authorized")


###############################################################################
@login_required(login_url="/login/")
def db_method_details(request):
    mid = request.GET.get("id", False)
    method = get_object_or_404(M, id=mid)
    context["method"] = method
    guid = method.guid
    time = Decimal(0.00)
    if method.get_total_task_time != None:
        time += method.get_total_task_time
    context["all_time"] = time
    context["deploy"] = method.can_deploy()
    return render(request, "db_method_details_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_method_edit_form(request):
    context = {}
    phid = None
    if request.method == "POST":
        mid = request.POST.get("id", False)
        phid = request.POST.get("phase_id", False)
    else:
        mid = request.GET.get("id", False)
    method = get_object_or_404(M, id=mid)
    form = MUF(instance=method)
    context["id"] = mid
    context["method"] = method
    context["form"] = form
    context["action"] = "/db_method_update/"
    context["ptypes"] = PT.objects.all().order_by("title")
    m_ptypes = method.project_type.values_list("id", flat=True)
    context["selected_ptypes"] = m_ptypes
    phases = []
    if len(m_ptypes) > 0:
        for pid in m_ptypes:
            ptype = get_object_or_404(PT, id=pid)
            pt_phases = list(ptype.phase.filter(newest=True).order_by("sequence"))
            phases += pt_phases
    else:
        phases = Ph.objects.filter(newest=True).order_by("sequence")
    context["phases"] = phases
    try:
        if phid:
            context["selected_phase"] = [int(phid)]
            existing_methods = M.objects.filter(phase__id=phid)
        else:
            context["selected_phase"] = [method.phase.id]
            existing_methods = M.objects.filter(phase__id=method.phase.id)
        form.fields["method"].choices = [("", "--------")] + [
            (x.id, x) for x in existing_methods
        ]
    except:
        pass
    context["edit"] = True
    context["multiple"] = True
    context["form_id"] = "form-db-method-update"
    return render(request, "db_method_update_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_method_update(request):
    if request.method == "POST":
        mid = request.POST.get("id", False)
        method = get_object_or_404(M, id=mid)
        original_phase_id = method.phase.id
        form = MUF(request.POST, instance=method)
        if form.is_valid():
            position = form.cleaned_data["position"]
            method_position_id = form.cleaned_data["method"]
            updated = form.save(commit=False)
            phid = int(request.POST.get("phase", False))
            updated.sequence = 1
            updated.save()
            pids = request.POST.getlist("project_types", [])
            fids = request.POST.getlist("files", [])
            if len(fids) > 0:
                updated.files.clear()
                for fid in fids:
                    current_file = get_object_or_404(AF, id=fid)
                    updated.files.add(current_file)
            else:
                updated.files.clear()
            if len(pids) > 0:
                updated.project_type.clear()
                for pid in pids:
                    ptype = get_object_or_404(PT, id=pid)
                    updated.project_type.add(ptype)
                    if phid:
                        phase = get_object_or_404(Ph, id=phid)
                        updated.phase = phase
                        try:

                            method_order = Method_Order.objects.get(
                                method__id=updated.id,
                                phase__id=original_phase_id,
                                project_type__id=pid,
                            )
                            method_order.update_phase(phase)
                        except:
                            pass
                    else:
                        try:
                            method_order = Method_Order.objects.get(
                                method__id=updated.id,
                                phase__id=original_phase_id,
                                project_type__id=pid,
                            )
                            method_order.remove()
                        except:
                            pass
                        updated.phase = None
                    updated.save()
                    if method_position_id:
                        method_position = M.objects.get(id=method_position_id)
                        if position == "before":
                            sequence = (
                                Method_Order.objects.get(
                                    method__id=method_position.id,
                                    phase__id=updated.phase.id,
                                    project_type__id=pid,
                                ).sequence
                                - 1
                            )
                        else:
                            sequence = Method_Order.objects.get(
                                method__id=method_position.id,
                                phase__id=updated.phase.id,
                                project_type__id=pid,
                            ).sequence
                        method.set_sequence(sequence, updated.phase.id, pid)
                    elif original_phase_id != updated.phase.id:
                        method.set_sequence(1, updated.phase.id, pid)
            else:
                updated.project_type.clear()
            if request.FILES.getlist("associated_files", False):
                for file in request.FILES.getlist("associated_files", False):
                    subdirectory = "methodology"
                    guid = updated.guid
                    new_file = save_new_afile(file, subdirectory, guid)
                    new_file.associated_item = updated
                    new_file.save()
                    updated.files.add(new_file)
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors})
    else:
        return HR("not authorized")


###############################################################################
@login_required(login_url="/login/")
def method_update(request):
    if request.method == "POST":
        method = get_object_or_404(M, id=request.POST.get("id", None))
        form = MUF(request.POST or None, instance=method)
        if form.is_valid():
            form.save()
            if request.FILES.getlist("associated_files", False):
                for file in request.FILES.getlist("associated_files", False):
                    new_file = AF()
                    new_file.filename = file.name
                    new_file.file = file
                    new_file.subdirectory = "methodology"
                    new_file.save()
                    method.files.add(new_file)
                    method.save()
            return HRR("/method_data_tree/")
        else:
            return HR("Invalid Form")
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def db_method_approve(request):
    mid = request.POST.get("id", False)
    method = get_object_or_404(M, id=mid)
    method.recommend = False
    if method.phase != None and method.project_type.count() > 0:
        if method.ancestor != None:
            if method.phase == method.ancestor.phase:
                method.ancestor.newest = False
                method.ancestor.save()
    method.save()
    return JR({"success": "method recommendation approved", "sidenav": "reload"})


###############################################################################
@login_required(login_url="/login/")
def db_method_decline(request):
    mid = request.POST.get("id", False)
    method = get_object_or_404(M, id=mid)
    method.delete()
    return JR({"declined": "method recommendation declined", "sidenav": "reload"})


###############################################################################
@login_required(login_url="/login/")
def db_method_deploy(request):
    mid = request.POST.get("id", False)
    method = get_object_or_404(M, id=mid)
    lineage = method.lineage_guid
    pids = request.POST.getlist("projects[]", [])
    for pid in pids:
        project = get_object_or_404(Project, id=pid)
        # check for the existence of an old version of the task
        try:
            old_task = project.get_newest_task(lineage)
        except:
            new_task = task_from_method(method, project)
        else:
            new_task = task_from_method(method, project)
            old_task.newest = False
            old_task.save()
            # Associate notes and files to new task
            for note in old_task.notes.all():
                note.associated_item = new_task
                note.save()
            for file in old_task.files.all():
                file.associated_item = new_task
                file.a_i_guid = new_task.guid
                file.save()
        audit = action_audit(
            request.user,
            "deployed a new task/version -> %s" % (new_task.title),
            "workflow",
            timezone.now(),
            project,
            new_task,
        )
    return JR({"success": "new tasks depoloyed"})


###############################################################################
# PHASES #
##########
@login_required(login_url="/login/")
def db_phase_add_form(request):
    pid = request.GET.getlist("id[]", [])
    pids = [int(n) for n in pid]
    title = request.GET.get("title", False)
    form = PhF()
    context["id"] = pid
    context["title"] = title
    context["form"] = form
    context["action"] = "/db_phase_add/"
    context["ptypes"] = PT.objects.all().order_by("title")
    context["add"] = True
    context["multiple"] = True
    context["select"] = pids
    context["form_id"] = "form-db-add-phase"
    return render(request, "db_phase_add_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_get_phases_for_ptypes(request):
    pids = request.GET.getlist("ids[]", [])
    selected = request.GET.get("selected", False)
    phases = []
    for pid in pids:
        ptype = get_object_or_404(PT, id=pid)
        pt_phases = list(ptype.phase.filter(newest=True).order_by("sequence"))
        phases += pt_phases
    context["phases"] = phases
    context["selected"] = selected
    return render(request, "db_phase_select_options.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_phase_add(request):
    form = PhF(request.POST)
    if form.is_valid():
        phase = form.save(commit=False)
        phase.guid = get_guid()
        phase.save()
        for pid in request.POST.getlist("ptypes", []):
            ptype = get_object_or_404(PT, id=pid)
            ptype.phase.add(phase)
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
@login_required(login_url="/login/")
def db_phase_details(request):
    pid = request.GET.get("id", False)
    phase = get_object_or_404(Ph, id=pid)
    context["phase"] = phase
    guid = phase.guid
    all_phases = Ph.objects.filter(parent_guid=guid)
    time = Decimal(0.00)
    for phase in all_phases:
        time += phase.billed_total_time
    context["all_time"] = time
    return render(request, "db_phase_details_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_phase_edit_form(request):
    pid = request.GET.get("id", False)
    phase = get_object_or_404(Ph, id=pid)
    form = PhUF(instance=phase)
    ptypes_ids = phase.project_type_set.values_list("id", flat=True)
    methods = []
    methods_ids = []
    # Add all methods to ids list uniquly
    for ptype in PT.objects.all():
        pt_method_ids = list(
            ptype.method_set.filter(newest=True).values_list("id", flat=True)
        )
        for mid in pt_method_ids:
            if mid not in methods_ids:
                methods_ids.append(mid)
                # Add all the methods from the ids list to methods list
                method = get_object_or_404(M, id=mid)
                methods.append(method)
    selected_methods = phase.method_set.filter(newest=True).values_list("id", flat=True)
    # form.fields['associated_methods'].queryset = methods
    context["id"] = pid
    context["phase"] = phase
    context["action"] = "/db_phase_update/"
    context["ptypes"] = PT.objects.all().order_by("title")
    context["selected_ptypes"] = ptypes_ids
    context["methods"] = methods
    context["selected_methods"] = selected_methods
    context["edit"] = True
    context["multiple"] = True
    context["form_id"] = "form-db-phase-update"
    context["form"] = form
    return render(request, "db_phase_update_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_phase_update(request):
    phid = request.POST.get("id")
    phase = get_object_or_404(Ph, id=phid)
    form = PhF(request.POST, instance=phase)
    if form.is_valid():
        updated = form.save()
        pids = request.POST.getlist("ptypes", [])
        mids = request.POST.getlist("methods", [])
        if len(pids) > 0:
            updated.project_type_set.clear()
            for pid in pids:
                ptype = get_object_or_404(PT, id=pid)
                updated.project_type_set.add(ptype)
        else:
            updated.project_type_set.clear()
        if len(mids) > 0:
            updated.method_set.clear()
            for mid in mids:
                method = get_object_or_404(M, id=mid)
                updated.method_set.add(method)
        else:
            updated.method_set.clear()
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
@login_required(login_url="/login/")
def db_phase_approve(request):
    pid = request.POST.get("id", False)
    phase = get_object_or_404(Ph, id=pid)
    if phase.ancestor:
        method_phase = phase.ancestor
        for method in method_phase.method_set.all():
            method.phase = phase
            method.save()
            phase.recommend = False
            phase.save()
    else:
        parent_phase = Ph.objects.get(guid=phase.parent_guid)
        for task in parent_phase.task_set.all():
            # Create Methods for each task in the phase
            new_method = M()
            new_method.title = task.title
            new_method.sequence = task.sequence
            new_method.phase = parent_phase
            new_method.tier = task.tier
            new_method.command = task.command
            new_method.description = task.description
            new_method.automate = task.automate
            new_method.mangle = task.mangle
            new_method.help_base = task.help_base
            new_method.help_import = task.help_import
            new_method.est_time = task.est_time
            new_method.version = task.version
            new_method.save()
            for file in task.files.all():
                subdirectory = "methodology"
                guid = new_method.guid
                new_file = save_new_afile(file, subdirectory, guid)
    return JR({"success": "success"})


###############################################################################
@login_required(login_url="/login/")
def db_phase_decline(request):
    pid = request.POST.get("id", False)
    phase = get_object_or_404(Ph, id=pid)
    if phase.ancestor:
        method_phase = phase.ancestor
        method_phase.newest = True
        method_phase.descendant = None
        method_phase.save()
    phase.delete()
    return JR({"success": "success"})


###############################################################################
@login_required(login_url="/login/")
def add_phase(request):
    if request.method == "POST":
        if request.POST.get("title", False):
            name = request.POST["title"]
            seq = request.POST.get("sequence", 1)
            phase = Ph(title=name, sequence=seq)
            phase.guid = get_guid()
            phase.save()
            if request.POST.getlist("associated_project_types", False):
                ptype_ids = request.POST.getlist("associated_project_types")
                for ptype_id in ptype_ids:
                    ptype = PT.objects.get(id=ptype_id)
                    phase.project_type_set.add(ptype)
                    ptype.save()
                    phase.save()
            # return JR({'status':'success','title':phase.title,'id':phase.id})
            return HRR("/method_data_tree/")
        else:
            return HR("no phase")
    else:
        return HR("not authorized")


###############################################################################
@login_required(login_url="/login/")
def add_phase_to_project(request):
    if request.method == "POST":
        form = PhF(request.POST)
        if form.is_valid():
            phase = form.save(commit=False)
            phase.project = request.user.tester.project
            phase.save()
            audit = action_audit(
                request.user,
                "added %s to %s" % (phase.title, phase.project.title),
                "workflow",
                timezone.now(),
                phase.project,
                phase,
            )
            return HRR("/display_phases/")
        else:
            return JR({"error": "Form Invalid", "form errors": form.errors})
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def get_phases(request):
    phase_list = list(Ph.objects.values_list("id", "title"))
    return JR({"state": "success", "phases": phase_list})


###############################################################################
@login_required(login_url="/login/")
def phase_details(request):
    phase_id = request.GET.get("item_id", None)
    phase = get_object_or_404(Ph, id=phase_id)
    form = PhF(instance=phase)
    context["form"] = form
    context["action"] = "/phase_update/"
    context["ptypes"] = PT.objects.all().order("title")
    return render(request, "phase_form.html", context)


###############################################################################
@login_required(login_url="/login/")
def phase_edit_form(request):
    pid = request.GET.get("id", False)
    phase = phase = get_object_or_404(Ph, id=pid)
    form = PhF(instance=phase)
    context["form"] = form
    context["id"] = pid
    context["title"] = phase.title
    context["action"] = "/phase_update/"
    context["edit"] = True
    context["form_id"] = "form-wf-phase-edit"
    context["recommend"] = True
    return render(request, "phase_form.html", context)


###############################################################################
@login_required(login_url="/login/")
def phase_update(request):
    # if request.method == 'POST':
    #     phase = get_object_or_404(Ph,id=request.POST.get('id',None))
    #     form = PhF(request.POST or None,instance=phase)
    #     if form.is_valid():
    #         form.save()
    #         return HRR('/method_data_tree/')
    #     else:
    #         return HR('Invalid Form')
    # else:
    #     return HR('Not Authorized')
    pid = request.POST.get("id", None)
    sequence = request.POST.get("seq", False)
    if sequence:
        phase = get_object_or_404(Ph, id=pid)
        phase.sequence = sequence
        phase.save()
        return JR({"success": "success"})
    else:
        return JR({"error": "no sequence"})


###############################################################################
@login_required(login_url="/login/")
def ptype_reorder_update(request):
    pid = request.POST.get("id", None)
    sequence = request.POST.get("seq", False)
    if sequence:
        ptype_id = get_object_or_404(PT, id=pid)
        ptype_id.sequence = sequence
        ptype_id.save()
        return JR({"success": "success"})
    else:
        return JR({"error": "no sequence"})


###############################################################################
@login_required(login_url="/login/")
def display_phases(request):
    phase_filter = request.GET.get("phase_id", False)
    project = request.user.tester.project
    if phase_filter and phase_filter != "all":
        project_phases = list(project.phase_set.filter(id=phase_filter))
    else:
        project_phases = list(project.phase_set.all())
    context["phases"] = project_phases
    return render(request, "display_phases.html", context)


###############################################################################
@login_required(login_url="/login/")
def get_phase_total_time(request):
    pid = request.GET.get("id", False)
    phase = get_object_or_404(Ph, id=pid)
    total_time = phase.billed_total_time
    return HR(total_time)


###############################################################################
@login_required(login_url="/login/")
def db_ptype_add_form(request):
    form = PTF()
    context["form"] = form
    context["action"] = "/db_ptype_add/"
    context["phases"] = Ph.objects.filter(recommend=False, newest=True, project=None)
    context["add"] = True
    context["multiple"] = True
    context["select"] = []
    context["form_id"] = "form-db-add-ptype"
    return render(request, "db_ptype_add_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_ptype_edit_form(request):
    pid = request.GET.get("id", False)
    ptype = get_object_or_404(PT, id=pid)
    form = PTF(instance=ptype)
    context["form"] = form
    context["action"] = "/db_ptype_update/"
    context["phases"] = Ph.objects.filter(newest=True, project=None)
    context["methods"] = M.objects.filter(newest=True)
    context["selected_phases"] = ptype.phase.values_list("id", flat=True)
    context["selected_methods"] = ptype.method_set.values_list("id", flat=True)
    context["edit"] = True
    context["multiple"] = True
    context["select"] = []
    context["form_id"] = "form-db-update-ptype"
    return render(request, "db_ptype_update_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def db_ptype_add(request):
    form = PTF(request.POST)
    if form.is_valid():
        ptype = form.save(commit=False)
        ptype.guid = get_guid()
        ptype.save()
        for pid in request.POST.getlist("phases", []):
            phase = get_object_or_404(Ph, id=pid)
            ptype.phase.add(phase)
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
@login_required(login_url="/login/")
def db_ptype_update(request):
    pid = request.POST.get("id")
    ptype = get_object_or_404(PT, id=pid)
    form = PTF(request.POST, instance=ptype)
    if form.is_valid():
        updated = form.save()
        pids = request.POST.getlist("phases", [])
        if len(pids) > 0:
            updated.phase.clear()
            for phase_id in pids:
                phase = get_object_or_404(Ph, id=phase_id)
                updated.phase.add(phase)
        else:
            updated.phase.clear()
        mids = request.POST.getlist("methods", [])
        if len(mids) > 0:
            updated.method_set.clear()
            for mid in mids:
                method = get_object_or_404(M, id=mid)
                updated.method_set.add(method)
        else:
            updated.method_set.clear()
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
@login_required(login_url="/login/")
def db_ptype_details(request):
    pid = request.GET.get("id", False)
    ptype = get_object_or_404(PT, id=pid)
    context["ptype"] = ptype
    guid = ptype.guid
    time = Decimal(0.00)
    context["item_type"] = "ptype"
    # if method.get_total_task_time != None:
    #     time += method.get_total_task_time
    # context['all_time']     = time
    return render(request, "db_ptype_details_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def add_ptype(request):
    if request.method == "POST":
        if request.POST.get("title", False):
            if request.POST.get("shorthand", False):
                name = request.POST["title"]
                shand = request.POST["shorthand"]
                ptype = PT(title=name, shorthand=shand)
                ptype.guid = get_guid()
                ptype.save()
                if request.POST.getlist("id_phase[]", False):
                    phase_ids = request.POST.getlist("id_phase[]")
                    for phase_id in phase_ids:
                        phase = Ph.objects.get(id=phase_id)
                        ptype.phase.add(phase)
                        ptype.save()
                        phase.save()
                # return JR({'status':'success','title':ptype.title,'id':ptype.id})
                return HRR("/method_data_tree/")
            else:
                return HR("no shorthand")
        else:
            return HR("no ptype name")
    else:
        return HR("not authorized")


###############################################################################
@login_required(login_url="/login/")
def get_ptypes(request):
    ptype_list = list(PT.objects.values_list("id", "title"))[::-1]
    return JR({"state": "success", "ptypes": ptype_list})


###############################################################################
@login_required(login_url="/login/")
def ptype_details(request):
    ptype_id = request.GET.get("item_id", None)
    phase = get_object_or_404(PT, id=ptype_id)
    form = PTF(instance=phase)
    context["form"] = form
    return render(request, "model_form.html", context)


###############################################################################
@login_required(login_url="/login/")
def ptype_update(request):
    if request.method == "POST":
        ptype = get_object_or_404(PT, id=request.POST.get("id", None))
        form = PTF(request.POST or None, instance=ptype)
        if form.is_valid():
            form.save()
            return HRR("/method_data_tree/")
        else:
            return HR("Invalid Form")
    else:
        return HR("Not Authorized")


################################################################################
def check_or_make_dir(export_dir):
    """
    PSEUDO CODE:

    check that media_root/exports/ptype_shorthand directory exists
    if not, create directory
    """
    if not os.access(export_dir, os.F_OK):
        os.makedirs(export_dir)


################################################################################
@login_required(login_url="/login/")
def export_project_type(request):
    """
    PSEUDO CODE:

    For a given ptype
    check if export dir exists
    if not, create export dir
    create dict ptype_dict
    create list phase_list
    for a phase in ptype's phases
        create list method_list
        for a method in phase's methods where project_type is ptype
            create list file_list
            for a file in method files
                add file to file list
            create dict(key method value file_list)
            add dict to method_list
        create dictionary(key is phase value is method_list)
        add dict to phase_list
    add (key ptype value phase_list) to ptype_dict
    """
    ####################
    ##   Local Vars   ##
    ####################
    ptype_dict = {}
    phase_list = []
    export_dir = ""
    export_list = []
    file_list = []
    method_list = []
    archive_name = ""
    #####################################
    ##         Local Constants         ##
    #####################################
    MEDIA_ROOT = settings.MEDIA_ROOT
    PID = request.POST.get("id", False)
    USER = request.user
    #####################################
    # Get Desired Project Type
    pt = get_object_or_404(PT, id=PID)
    # Set the archive file name to pt's {shorthand}_{verison}
    archive_name = "%s_%s" % (pt.shorthand, pt.version)
    # Set the export directory path
    export_dir = os.path.join(MEDIA_ROOT, "export", pt.shorthand)
    # Check for export dir, make if it doesn't exist
    check_or_make_dir(export_dir)
    # Loop through the Project Type's Phases excluding suggested Phases
    for phase in pt.phase.filter(
        recommend=False, suggestor=None, project=None, newest=True
    ):
        # Get the Phase's Methods for Project Type that are newest version
        methods = phase.method_set.filter(recommend=False, project_type=pt, newest=True)
        # Loop through the Methods
        for method in methods:
            # Loop through the Method's Files
            for file in method.files.all():
                # Copy the actual file (not model) to the export dir
                shutil.copy(str(file.file.path), export_dir)
                # Add the coppied File to the file list
                file_list.append(file)
            # Add the coppied Method to the method list
            method_list.append(method)

        # Add the coppied Phase to the phase list
        phase_list.append(phase)
    # Add Phases to export list first to account for relational dependancies
    export_list += phase_list
    # Add Project Type to the export list
    export_list.append(pt)
    # Add Files to export list
    export_list += file_list
    # Add Methods to the export list
    export_list += method_list
    # Serialize objects into json based on natural keys (guid)
    export = serializers.serialize(
        "json",
        export_list,
        indent=2,
        use_natural_foreign_keys=True,
        use_natural_primary_keys=True,
    )
    # Open the json fixture file {shorthand}_{version}.json in export dir
    export_file_path = os.path.join(export_dir, archive_name + ".json")
    with open(export_file_path, "w") as export_file:
        # Write the json to the file
        export_file.write(export)
    # Zip the json and associated files into the archive
    zip_file_name = archive_name + ".zip"
    zip_file_path = os.path.join(export_dir, zip_file_name)
    with zipfile.ZipFile(
        zip_file_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True
    ) as zipf:
        # Step through the export dir and write the files to the archive
        for file in [
            f
            for f in os.listdir(export_dir)
            if os.path.isfile(os.path.join(export_dir, f))
            and f.title().lower() != zip_file_name.lower()
        ]:
            zipf.write(os.path.join(export_dir, file), arcname=file)
    # Create File object from the archive file
    archive = File(open("%s/%s.zip" % (export_dir, archive_name), "rb"))
    # Create new Associated File amd store it in methodologies
    new_archive = AF(
        guid=get_guid(),
        filename=archive_name + ".zip",
        file=archive,
        subdirectory="methodology/exports",
        uploader=USER,
        associated_item=pt,
    )
    new_archive.save()
    return JR({"success": "success"})


################################################################################
def import_pt_form(request):
    form = IFF()
    context["form"] = form
    return render(request, "file_import_form.html", context)


################################################################################
def lineage_handler(obj, model, manager):
    """
    PSEUDO CODE:

    If obj has no guid, give it open
    If old exists in database using lineage_guid
        If new and old have same guid
            Save new with new guid
        Else
            Save new with same guid
        Set new ancestor to old
        Set old decendent to new
        New newest field set to true
        Old newest field set to false
    Else
        Save model with same guid
    Set lineage_guid
    """
    # Check if obj has guid
    if not obj["fields"]["guid"]:
        # If no guid, give it one
        obj["fields"]["guid"] = get_guid()
    if not obj["fields"]["lineage_guid"]:
        # If no lineage guid, give it one
        obj["fields"]["lineage_guid"] = get_guid()
    # Try to get newest model with the same lineage from database
    try:
        # Check which model type is being handled
        old = manager.objects.get(guid=obj["fields"]["guid"])
    # If no model from lineage in database
    except:
        # Set model's guid to object's guid
        setattr(model, "guid", obj["fields"]["guid"])
        # Set model's lineage guid to object's lineage guid
        setattr(model, "lineage_guid", obj["fields"]["lineage_guid"])
        # Save model
        model.save()
    # If model from lineage in database
    else:
        return "c"
        # Generate new guid
        new_guid = get_guid()
        # Set model's guid to new guid
        setattr(model, "guid", new_guid)
        setattr(model, "lineage_guid", old.lineage_guid)
        if not old.newest:
            if "phase" in obj["model"]:
                old = manager.objects.get(
                    lineage_guid=obj["fields"]["lineage_guid"],
                    newest=True,
                    project=None,
                )
            else:
                old = manager.objects.get(
                    lineage_guid=obj["fields"]["lineage_guid"], newest=True
                )
        # Set model's ancestor to old
        setattr(model, "ancestor", old)
        # Set old's descendant to model
        setattr(old, "descendant", model)
        # Set model as newest
        setattr(model, "newest", True)
        # Set old as not newest
        setattr(old, "newest", False)
        # Save model
        model.save()
        old.save()


################################################################################
def relationship_handler(obj, model, field, lineage_guid, manager):
    """
    PSEUDO CODE:

    Get newest model from lineage_guid
    Set model field to newest.guid
    """
    # Check which model type is being handled
    # Get newest object with lineage guid
    if field == "phase":
        relate = manager.objects.get(
            lineage_guid=lineage_guid, newest=True, project=None
        )
    else:
        relate = manager.objects.get(lineage_guid=lineage_guid, newest=True)
    # Set model's field to newest object's guid
    setattr(model, field, relate)
    model.save()


################################################################################
def field_handler(obj, model, field):
    """
    PSEUDO CODE:

    If field is in blacklist
        Return false
    Else
        Set new's field to obj's field's value
        Return true
    """
    # Generate blacklisted fields
    BLACKLIST = [
        "ancestor",
        "descendant",
        "recommends",
        "suggestor",
        "newest",
        "project",
        "guid",
        "lineage_guid",
        "phase",
        "ptype",
        "files",
        "children",
        "uploader",
        "file",
        "filename",
        "subdir",
        "associated_item",
        "project_type",
        "content_type",
        "object_id",
    ]
    # Check if field is blacklisted
    if field in BLACKLIST:
        # If field blacklisted, return false
        return False
    else:
        # If not blacklisted, set model's field attr
        setattr(model, field, obj["fields"][field])
        model.save()
        return True


################################################################################
def phase_handler(obj, model, field):
    """
    PSEUDO CODE:

    If project
        Set project to None
    """
    # Check which field type is being handled
    if field == "project":
        # Set model's project field to None
        setattr(model, "project", None)
        model.save()


################################################################################
def ptype_handler(obj, model, field, phase_list):
    """
    PSEUDO CODE:

    If phase
        For phase in phase list
            Add phase to model'sphase field
    """
    # Check which field type is being handled
    if field == "phase":
        # Loop throuh phase list
        for phase in phase_list:
            # Add phase to model's phase attribute
            model.phase.add(phase)


################################################################################
def file_handler(obj, model, field, file_dic, zipf, user):
    """
    PSEUDO CODE:

    If file
        Get filename
        Get save dir
        Extract file from zip to dir
        Set file attr
        Set subdir attr
    Elif uploader
        Set to request's user
    """
    MEDIA_ROOT = settings.MEDIA_ROOT
    # Check which field type is being handled
    if field == "file":
        # Get actual filename without subdir
        # filename = re.search('(?:\/)(.*?$)',obj['fields'][field]).group(1)
        idx = obj["fields"][field].rfind("/")
        filename = obj["fields"][field][idx + 1 :]
        # Get subdir to save file based on associated item guid
        subdir = "methodology"
        # Get full dir path to save file in
        new_dir = os.path.join(MEDIA_ROOT, subdir)  # not yet a path?
        # Extract file from zip into dir
        new_file = zipf.extract(file_dic[filename], new_dir)
        # Set model's file to newly saved file
        setattr(model, "file", File(open(new_file)))
        # Set model's subdir to subdir
        setattr(model, "subdir", subdir)
        setattr(model, "filename", filename)
    elif field == "uploader":
        model.uploader = user
    model.save()


################################################################################
def method_handler(obj, model, field, ptype_guid):
    """
    PSEUDO CODE:

    If ptype
        Call relationship handler passing model, field, ptype's lineage_guid
    Elif phase
        Call relationship handler passing model, field, phase's lineage_guid
    Elif files
        For file in files
            Add file to new's files attr
            Set model as file's associated item
            Set model's guid as file's a_i_guid
    """
    MEDIA_ROOT = settings.MEDIA_ROOT
    # Check which field type is being handled
    if field == "project_type":
        # Get ptype from database matching guid
        ptype = PT.objects.get(guid=ptype_guid)
        model.project_type.add(ptype)
    elif field == "phase":
        # Get phase from database matching guid
        phase = Ph.objects.get(guid=obj["fields"][field][0])
        # Call relationship handler passing phase's lineage_guid
        relationship_handler(obj, model, field, phase.lineage_guid, Ph)
    elif field == "files":
        # Loop through the object's files
        for f in obj["fields"][field]:
            # Get file from database
            file_model = AF.objects.get(guid=f)
            # Add file guid to model's files attribute
            model.files.add(file_model)
            # Set file's associated item to model
            setattr(
                file_model, "associated_item", model
            )  # is this correct use of associated_item
            # Set file model's associated item guid to model's guid
            setattr(file_model, "a_i_guid", model.guid)
            file_model.save()
    model.save()


################################################################################
def import_project_type(request):
    """
    PSEUDO CODE:
    
    Create phase list
    Create file dic
    Creat file dictionary
    Get zip file
    Get json from zip
    For object in json:
        Get model type
        Instantiate new object model
        Call lineage handler passing object, model
        For field in object fields
            If call field handler passing object, model, field
                Continue
            Elif phase
                Call phase handler passing object, model, field
            Elif ptype
                Call ptype handler passing object, model, field, phase list
            Elif file
                Call file handler passing obj, model, field, file_dic, zipf, USER
            Elif method
                Call method handler passing object, model, field
        If model is phase
            Add to phase list
        Save new
    """

    ####################
    ##   Local Vars   ##
    ####################
    phase_list = []
    file_dic = {}
    #####################################
    ##         Local Constants         ##
    #####################################
    USER = request.user
    ZIP_FILE = request.FILES.get("file", [])  # this will be a zip
    # Load zip file
    zipf = zipfile.ZipFile(ZIP_FILE)
    # Get list of zipinfo of files in archive
    zipinfo = zipf.infolist()
    # Loop through the list
    for info in zipinfo:
        # Check if file is a json
        if info.filename.endswith(".json"):
            # open json
            DATA_FILE = zipf.open(info)
        file_dic.update({info.filename: info})
    # Load json file
    DATA = json.load(DATA_FILE)
    # Loop through objects stored in json
    for obj in DATA:
        # Set object's model name
        prep = obj["model"][obj["model"].rfind(".") + 1 :]
        # Set module the object's model is from
        module = obj["model"][: obj["model"].find(".")]
        # Capitalize prep. If separated by '_', capitalize second word as well
        # Problems with more than 1 '_'?
        if "_" in prep:
            # Find index of '_'
            idx = prep.find("_")
            # Capitalize first character
            final = prep[0].capitalize()
            # Append the rest of first word including '_' to final
            final += prep[1 : idx + 1]
            # Capitalize second word
            final += prep[idx + 1].capitalize()
            # Append the rest of second word to final
            final += prep[idx + 2 :]
            # Generate string
            final = str(final)
        else:
            # Capitalize first character
            final = prep[0].capitalize() + prep[1:]
            # Generate string
            final = str(final)
        # Set model's module path
        manager = getattr(sys.modules["%s.models" % str(module)], "%s" % final)
        # Instantiate new model
        model = manager()
        # Call lineage handler
        result = lineage_handler(obj, model, manager)
        if result == "c":
            model = manager.objects.get(guid=obj["fields"]["guid"])
        # Loop through the object's attributes
        for field in obj["fields"]:
            # Call field handler
            if field_handler(obj, model, field):
                # If field is not blacklisted continue to next field
                continue
            # If field blacklisted, check model type and call handler
            elif "phase" in obj["model"]:
                phase_handler(obj, model, field)
            elif "project_type" in obj["model"]:
                ptype_handler(obj, model, field, phase_list)
            elif "file" in obj["model"]:
                file_handler(obj, model, field, file_dic, zipf, USER)
            elif "method" in obj["model"]:
                method_handler(obj, model, field, ptype_guid)
        # Save model to database
        model.save()
        # If model is a phase, add to phase list
        if "phase" in obj["model"]:
            phase_list.append(model)
        elif "project_type" in obj["model"]:
            ptype_guid = model.guid
    # Close zip file
    zipf.close()
    return JR({"success": "success"})


@login_required(login_url="/login/")
def method_reorder_update(request):
    method_id = request.POST.get("id", None)
    sequence = request.POST.get("sequence", False)
    if sequence:
        phase_id = request.POST.get("phaseId", False)
        project_type_id = request.POST.get("projectTypeId", False)
        if phase_id and project_type_id:
            method = get_object_or_404(M, id=method_id)
            method.set_sequence(sequence, phase_id, project_type_id)
            return JR({"success": "success"})
        else:
            return JR({"error": "no phase or project type"})
    else:
        return JR({"error": "no sequence"})


@login_required(login_url="/login/")
def db_manage_phases(request):
    phases = Ph.objects.filter(project=None, newest=True).order_by('sequence')
    context['phases'] = phases
    return render(request, "db_phases_modal.html", context)


@login_required(login_url="/login/")
def db_manage_methods(request):
    methods = M.objects.all()
    context['methods'] = methods
    return render(request, "db_methods_modal.html", context)


@login_required(login_url="/login/")
def phase_delete(request):
    pid = request.POST.get("id", None)
    phase = get_object_or_404(Ph, id=pid)
    phase.delete()
    return JR({"success": "success"})


@login_required(login_url="/login/")
def method_delete(request):
    mid = request.POST.get("id", None)
    method = get_object_or_404(M, id=mid)
    method.delete()
    return JR({"success": "success"})


@login_required(login_url="/login/")
def method_remove(request):
    mid = request.POST.get("id", None)
    method = get_object_or_404(M, id=mid)
    ptype_id = request.POST.get("ptype_id", None)
    ptype = get_object_or_404(PT, id=ptype_id)
    method.project_type.remove(ptype)
    return JR({"success": "success"})


@login_required(login_url="/login/")
def phase_remove(request):
    pid = request.POST.get("id", None)
    phase = get_object_or_404(Ph, id=pid)
    ptype_id = request.POST.get("ptype_id", None)
    ptype = get_object_or_404(PT, id=ptype_id)
    ptype.phase.remove(phase)
    return JR({"success": "success"})


@login_required(login_url="/login/")
def project_type_remove(request):
    ptype_id = request.POST.get("id", None)
    ptype = get_object_or_404(PT, id=ptype_id)
    ptype.delete()
    return JR({"success": "success"})
