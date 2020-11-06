from utils.imports import *

from django.contrib.auth.models import User


from .models import Project
from files.models import Associated_File as AF
from clients.models import Client
from methodologies.models import Method as M

from notes.models import Note
from timetracker.models import Time_Entry
from models import Milestone

import datetime

from forms import FileUploadForm as FUF
from forms import ProjectForm as PF
from forms import MilestoneForm as MF

from project.setters.models import milestone_constructor

from tasks.setters.models import create_project_tasks
from methodologies.setters.models import instantiate_project_phases

# Global Variable
context = {}

# Create your views here.
###############################################################################
def get_context_items(context, request):
    projects_list = Project.objects.all()
    projects_count = Project.objects.all().count()
    open_proj_count = 0
    if M.objects.filter(recommend=True).count() > 0:
        context["recommendations"] = True
    for proj in projects_list:
        if proj.active == True:
            open_proj_count += 1
    try:
        context["project"] = request.user.tester.project
    except:
        pass
    context["open_proj_count"] = open_proj_count
    context["projects"] = projects_list
    context["projects_count"] = projects_count
    return context


###############################################################################
def _get(request, name):
    try:
        lib = getattr(request, "GET")
    except:
        info = False
    else:
        info = lib.get(name, False)

    return info


###############################################################################
def _parse_date(string):
    s = datetime.datetime.strptime
    date = False
    try:
        date = s(string, "%m/%d/%y")
    except:
        try:
            date = s(string, "%m/%d/%Y")
        except:
            try:
                date = s(string, "%Y/%m/%d")
            except:
                try:
                    date = s(string, "%m-%d-%y")
                except:
                    try:
                        date = s(string, "%m-%d-%Y")
                    except:
                        try:
                            date = s(string, "%Y-%m-%d")
                        except:
                            pass
    return date


###############################################################################
@login_required(login_url="/login/")
def get_project_nav(request):
    if request.user.is_authenticated:
        return render(request, "nav_project.html", context)


###############################################################################
@login_required(login_url="/login/")
def open_projects_checklist(request):
    context["projects"] = Project.objects.filter(active=True)
    return render(request, "open_projects_checklist.html", context)


###############################################################################
@login_required(login_url="/login/")
def projects_dropdown(request):
    get_context_items(context, request)
    if request.user.is_authenticated:
        context["projects"] = Project.objects.all()
        return render(request, "projects_dropdown.html", context)


###############################################################################
@login_required(login_url="/login/")
def project_files(request):
    get_context_items(context, request)
    project = request.user.tester.project
    if request.method == "POST":
        if request.FILES.get("associated_files", False):
            for item in request.FILES.getlist("associated_files"):
                new_file = AF(filename=item.name, file=item, associated_item=project)
                new_file.uploader = request.user
                new_file.save()
                audit = action_audit(
                    request.user,
                    "added %s to %s" % (new_file.filename, project.title),
                    "project_files",
                    timezone.now(),
                    project,
                    new_file,
                )
            return HRR("/display_project_files/")
    all_files = list(project.associated_files.all()) + list(project.issue_files.all())
    form = FUF()
    context["form"] = form
    context["section"] = "Project Files"
    context["where"] = "project_files"
    context["title"] = "Project Files"
    context["audits"] = initial_audits(project, "project_files", 10)
    context["files"] = all_files
    context["page_controls"] = True
    context["item_header"] = True
    context["item_name"] = "File(s)"
    context["add_script"] = "pfFileAdd(event)"
    return render(request, "p_files.html", context)


###############################################################################
@login_required(login_url="/login/")
def temp(request):
    get_context_items(context, request)
    return render(request, "temporary.html", context)


###############################################################################
@login_required(login_url="/login/")
def display_sidenav(request):
    get_context_items(context, request)
    context["db_nav"] = True
    return render(request, "display_sidenav.html", context)


###############################################################################
@login_required(login_url="/login/")
def home(request):
    context = {}
    context = get_context_items(context, request)
    user = request.user
    milestones = Milestone.objects.all()
    context["milestones"] = sorted(milestones, key=lambda milestone: milestone.title)
    if is_hv_admin(user) and user.is_authenticated:
        context["userman"] = True
    try:
        user.tester
    except:
        pass
    else:
        try:
            Project.objects.get(id=user.tester.last_project)
        except:
            pass
        else:
            context["last_project"] = Project.objects.get(id=user.tester.last_project)
    user.tester.project = None
    uc = user.tester.context
    uc.ms_date_range_start = None
    uc.ms_date_range_end = None
    uc.save()
    context.pop("project", None)
    context["db_nav"] = True
    context["all_projects"] = Project.objects.all()
    context["client_count"] = Client.objects.all().count()
    context["random"] = random.randint(0, 999)
    if request.GET.get("home", False):
        return render(request, "hv_home.html", context)
    else:
        return render(request, "baseline.html", context)


###############################################################################
@login_required(login_url="/login/")
def overview(request):
    get_context_items(context, request)
    context["section"] = "Project Overview"
    project = request.user.tester.project
    context["issue_count"] = project.issue_count
    context["notes"] = project.notes.filter(newest=True).order_by(
        "-created"
    )
    context["notes_count"] = (
        project.notes.filter(newest=True).order_by("-created").count()
    )
    context["task_count"] = project.task_set.filter(newest=True).count()
    total_time = Time_Entry.objects.filter(project=project).aggregate(Sum(F("time")))[
        "time__sum"
    ]
    if total_time is None or total_time == "0":
        total_time = "0.00"
    context["total_time"] = "%s hours" % total_time
    context["title"] = project.title
    context["audits"] = initial_audits(project, "overview", 20)
    context["where"] = "overview"
    milestones = project.milestone_set.all().order_by("-end_date")
    context["milestones"] = milestones
    return render(request, "overview.html", context)


###############################################################################
@login_required(login_url="/login/")
def display_milestones(request):
    project = request.user.tester.project
    milestones = project.milestone_set.all().order_by("-end_date")
    context["milestones"] = milestones
    return render(request, "display_milestones.html", context)


###############################################################################
@login_required(login_url="/login/")
def home_milestones(request):
    user = request.user
    user = User.objects.get(id=user.id)
    uc = user.tester.context
    p_id = uc.ms_project_filter
    status = uc.ms_status_filter
    f_date = uc.ms_date_range_start
    t_date = uc.ms_date_range_end
    if p_id != "all":
        project = Project.objects.filter(id=p_id)
        context["projects"] = project
        if status != "all":
            milestones = project.first().milestone_set.filter(status=status)
        else:
            milestones = project.first().milestone_set.all()
    else:
        projects = Project.objects.all()
        if status != "all":
            milestones = Milestone.objects.filter(status=status)
        else:
            milestones = Milestone.objects.all()
        context["projects"] = projects
    if f_date:
        milestones = milestones.filter(end_date__range=[f_date, t_date])
    sort_field = uc.ms_sort_field
    sort_order = uc.ms_sort_ascending
    if sort_field == "milestone":
        context["milestones"] = sorted(
            milestones, key=lambda milestone: milestone.title, reverse=sort_order
        )
    elif sort_field == "project":
        context["milestones"] = sorted(
            milestones,
            key=lambda milestone: milestone.project.title,
            reverse=sort_order,
        )
    elif sort_field == "status":
        context["milestones"] = sorted(
            milestones, key=lambda milestone: milestone.status, reverse=sort_order
        )
    elif sort_field == "startDate":
        context["milestones"] = sorted(
            milestones, key=lambda milestone: milestone.start_date, reverse=sort_order
        )
    elif sort_field == "endDate":
        context["milestones"] = sorted(
            milestones, key=lambda milestone: milestone.end_date, reverse=sort_order
        )
    else:
        context["milestones"] = sorted(
            milestones, key=lambda milestone: milestone.title, reverse=True
        )
    return render(request, "home_milestones.html", context)


###############################################################################
@login_required(login_url="/login/")
def get_milestone_tasks(request):
    p = request.user.tester.project
    phases = list(p.phase_set.all()) + list(p.project_type.phase.all())
    choice_list = []
    for phase in phases:
        choice_list.append({"data_id": "%s" % phase.id, "label": "%s" % phase.title})
        for task in phase.task_set.all():
            if task in p.task_set.all():
                choice_list.append(
                    '<option value="%s">%s</option>' % (task.id, task.title)
                )
        choice_list.append("</optgroup>")
    return JR({"choices": choice_list})


###############################################################################
@login_required(login_url="/login/")
def milestone_add(request):
    if request.method == "POST":
        form = MF(request.POST, project=request.user.tester.project)
        if form.is_valid():
            milestone = form.save(commit=False)
            # generate guid here
            # generate audit
            milestone.project = request.user.tester.project
            milestone.save()
            phases = request.POST.getlist("phases", [])
            for phase in phases:
                milestone.phases.add(phase)
            return HRR("/display_milestones/")
        else:
            # Generate error strings
            return JR({"errors": form.errors})
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def milestone_delete(request):
    milestone_id = request.POST.get("milestone_id")
    milestone = get_object_or_404(Milestone, id=milestone_id)
    milestone.delete()
    location = request.POST.get("location")
    if location == "home-milestones":
        return HRR("/home_milestones/")
    else:
        return HRR("/display_milestones/")


###############################################################################
@login_required(login_url="/login/")
def milestone_state(request):
    if request.method == "POST":
        milestone_id = request.POST.get("ms_id", False)
        if milestone_id:
            milestone = Milestone.objects.get(id=milestone_id)
            state = request.POST.get("state", False)
            if state:
                milestone.status = state
                milestone.save()
                context["ms"] = milestone
                return render(request, "milestone_state.html", context)
            else:
                return HR("No State!")
        else:
            return HR("No Milestone!")
    else:
        return HR("Not Authorized!")


###############################################################################
@login_required(login_url="/login/")
def ms_filter_submit(request):
    pid = _get(request, "pid")
    status = _get(request, "status")
    f_date = _get(request, "from")
    t_date = _get(request, "to")
    user = request.user
    uc = user.tester.context
    flag = False
    if f_date:
        fdate = _parse_date(f_date)
        if fdate:
            uc.ms_date_range_start = fdate
            if not flag:
                flag = True
    if t_date:
        tdate = _parse_date(t_date)
        if tdate:
            uc.ms_date_range_end = tdate
            if not flag:
                flag = True
    if pid:
        uc.ms_project_filter = pid
        if not flag:
            flag = True
    if status:
        uc.ms_status_filter = status
        if not flag:
            flag = True
    if flag:
        uc.save()
    return HRR("/home_milestones/")


###############################################################################
@login_required(login_url="/login/")
def ms_filter_clear(request):
    user = request.user
    uc = user.tester.context
    uc.ms_date_range_start = None
    uc.ms_date_range_end = None
    uc.ms_project_filter = "all"
    uc.ms_status_filter = "all"
    uc.save()
    return HRR("/home_milestones/")


###############################################################################
@login_required(login_url="/login/")
def ms_sort(request):
    user = request.user
    is_ascending = _get(request, "isAscending")
    field = _get(request, "field")
    uc = user.tester.context
    if is_ascending == "true":
        uc.ms_sort_ascending = True
    else:
        uc.ms_sort_ascending = False
    uc.ms_sort_field = field
    uc.save()
    return HRR("/home_milestones/")


###############################################################################
@login_required(login_url="/login/")
def close_project(request):
    context = {}
    return HRR("/")


###############################################################################
@login_required(login_url="/login/")
def add_project(request):
    get_context_items(context, request)
    context["section"] = "Add New Project"
    if request.method == "POST":
        title = request.POST.get("title", None)
        form = PF(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            project.vips = form.cleaned_data[
                "vips"
            ]  # to assign values in ManyToManyField, form has to be saved first
            project.project_milestone = milestone_constructor(project)
            project.save()
            # for project vip audit
            for x in project.vips.all():
                action_audit(
                    request.user,
                    "Assigned %s as %s" % (x.person, x.role),
                    "project/%s" % project.id,
                    timezone.now(),
                    project,
                    x,
                )
                # project creation audit
            audit = action_audit(
                request.user,
                "created %s" % (project.title),
                "projects/%s" % project.id,
                timezone.now(),
                project,
                project,
            )
            if request.FILES.get("associated_files", False):
                for item in request.FILES.getlist("associated_files"):
                    new_file = AF(
                        filename=item.name, file=item, associated_item=project
                    )
                    new_file.uploader = request.user
                    new_file.save()
                    audit = action_audit(
                        request.user,
                        "added %s to %s" % (new_file.filename, project.title),
                        "project_files",
                        timezone.now(),
                        project,
                        new_file,
                    )
            instantiate_project_phases(project)
            # method_list 	= project.project_type.method_set.all()
            task_list = []
            for phase in project.project_type.phase.all():
                method_list = []
                method_list = phase.method_set.filter(
                    newest=True, recommend=False, project_type=project.project_type
                )
                phase_tasks = create_project_tasks(method_list, project)
                task_list += phase_tasks
                # task_list		= create_project_tasks(method_list,project)
            context["tasks"] = task_list
        else:
            return JR({"errors": form.errors})
        return JR({"success": "/projects/%s" % (project.id), "sidenav": "reload"})


###############################################################################
@login_required(login_url="/login/")
def new_project(request):
    get_context_items(context, request)
    form = PF()
    context["form"] = form
    return render(request, "new_project.html", context)


###############################################################################
@login_required(login_url="/login/")
def project(request, uid, info=""):
    project_object = Project.objects.get(pk=uid)
    context["project"] = project_object
    context["tasks"] = list(project_object.task_set.all())
    user = request.user
    user.tester.last_project = project_object.id
    user.tester.project = project_object
    user.tester.save()
    context["project"] = user.tester.project
    return HRR("/overview")


###############################################################################
@login_required(login_url="/login/")
def project_status(request):
    if request.method == "POST":
        if request.POST.get("state", False):
            state = request.POST["state"]
            if request.POST.get("proj_id", False):
                proj_id = request.POST["proj_id"]
                project = Project.objects.get(id=proj_id)
                if state == "open":
                    project.active = True
                    project.save()
                    audit = action_audit(
                        request.user,
                        "changed %s status to %s" % (project.title, state),
                        "projects_db",
                        timezone.now(),
                        project,
                        project,
                    )
                    return HR("Project Opened!")
                elif state == "close":
                    project.active = False
                    project.save()
                    audit = action_audit(
                        request.user,
                        "changed %s status to %s" % (project.title, state),
                        "projects_db",
                        timezone.now(),
                        project,
                        project,
                    )
                    return HR("Project Closed!")
                else:
                    return HR("Wrong State!")
            else:
                return HR("No Project!")
        else:
            return HR("No State!")
    else:
        return HR("Not Authorized")


###############################################################################
@login_required(login_url="/login/")
def projects_db(request):
    get_context_items(context, request)
    context["section"] = "Projects DB"
    all_projects = Project.objects.all().order_by("title")
    context["all_projects"] = all_projects
    return render(request, "projects_db.html", context)


###############################################################################
def find_model(request):
    # print request.POST
    val = request.POST.get("val", "")
    client_names = []
    client_list = list(Client.objects.filter(name__icontains=val))
    for client in client_list:
        client_names.append(client.name)
    transmission = {"clients": client_names}
    return JR(transmission)
