import sys
import datetime
from calendar import monthrange
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.utils import timezone
from auditor.views import action_audit
from django.db.models import Q, Sum, Count, F

from .utils import Week, Day

from project.views import get_context_items
from project.models import Project
from forms import TimeEntryForm as TEF
from forms import TaskTimeEntryForm as TTEF

from notes.models import Note
from tasks.models import Task
from timetracker.models import Time_Entry
from auditor.models import Action
from auditor.utils import initial_audits
from django.contrib.auth.models import User

# Define request context
context = {}
###############################################################################
class no_entry:
    def __init__(self):
        self.username = "No Entries"


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
def _get(request, name):
    try:
        lib = getattr(request, "GET")
    except:
        info = False
    else:
        info = lib.get(name, False)

    return info


###############################################################################
def _post(request, name):
    try:
        lib = getattr(request, "POST")
    except:
        info = False
    else:
        info = lib.get(name, False)

    return info


###############################################################################
def get_start_of_week(today):
    idx = (today.weekday() + 1) % 7
    mon = today - timezone.timedelta(6 + idx)
    mon = mon + timezone.timedelta(days=7)
    return mon


###############################################################################
def get_start_of_month(today):
    start = today.replace(day=1)
    return start


###############################################################################
def get_end_of_month(today):
    month = today.month
    year = today.year
    end = monthrange(year, month)[1]
    return end


###############################################################################
@login_required(login_url="/login/")
def tt_get_current(request):
    val = request.GET.get("val", False)
    user = request.user
    uc = user.tester.context
    if val == "week":
        start = get_start_of_week(timezone.now())
        end = start + timezone.timedelta(days=6)
    if val == "month":
        start = get_start_of_month(timezone.now())
        end = start + timezone.timedelta(days=get_end_of_month(timezone.now()) - 1)
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    return JR({"dates": {"start": start, "end": end}})


###############################################################################
@login_required(login_url="/login/")
def tt_filter_submit(request):
    pid = _get(request, "pid")
    val = _get(request, "val")
    f_date = _get(request, "from")
    t_date = _get(request, "to")
    uid = _get(request, "uid")
    user = request.user
    uc = user.tester.context
    flag = False
    if f_date:
        fdate = _parse_date(f_date)
        if fdate:
            uc.tt_date_range_start = fdate
            if not flag:
                flag = True
    if t_date:
        tdate = _parse_date(t_date)
        if tdate:
            uc.tt_date_range_end = tdate
            if not flag:
                flag = True
    if uid:
        uc.tt_user_filter = uid
        if not flag:
            flag = True
    if pid:
        uc.tt_project_filter = pid
        if not flag:
            flag = True
    if val:
        if uc.tt_fields_sort_by[0] != "-":
            val = "-" + val
        uc.tt_fields_sort_by = val
        if not flag:
            flag = True
    if flag:
        uc.save()
    return HRR("/display_time_entries/")


###############################################################################
def _get_week(uc):
    fdate = uc.tt_date_range_start
    tdate = uc.tt_date_range_end
    uid = uc.tt_user_filter
    pid = uc.tt_project_filter
    users = []
    if uid != "all":
        user = User.objects.get(id=uid)
        users.append(user)
    else:
        for u in User.objects.all():
            users.append(u)
    f_man = Time_Entry.objects.filter
    date_range = range((tdate - fdate).days + 1)
    weeks = []
    week = Week()
    end = len(date_range) - 1
    for idx in date_range:
        time_tracker_dict = {}
        times_dict = {}
        totaltime = Decimal(0.00)
        timetrackerlist = []
        allnotes = ""
        date = fdate + timezone.timedelta(days=idx)
        daydate = fdate + timezone.timedelta(days=idx)
        if pid != "all":
            if uid != "all":
                time_tracks = (
                    f_man(date=date)
                     .filter(project__id=pid)
                     .filter(tester__id=uid)
                     .filter(newest=True)
                )
                time_tracker_dict[user.username] = time_tracks
                time = time_tracks.aggregate(Sum("time"))["time__sum"]
                if time == None:
                    time = "----"
                else:
                    totaltime += time
                times_dict[user.username] = time
                timetrackerlist += list(time_tracks)
            else:
                for u in users:
                    time_tracks = (
                        f_man(date=date)
                         .filter(project__id=pid)
                         .filter(tester__id=u.id)
                         .filter(newest=True)
                    )
                    time_tracker_dict[u.username] = time_tracks
                    time = time_tracks.aggregate(Sum("time"))["time__sum"]
                    if time == None:
                        time = "----"
                    else:
                        totaltime += time
                    times_dict[u.username] = time
                    timetrackerlist += list(time_tracks)
        else:
            if uid != "all":
                time_tracks = (
                    f_man(date=date)
                     .filter(tester__id=uid)
                     .filter(newest=True)
                )
                time_tracker_dict[user.username] = time_tracks
                time = time_tracks.aggregate(Sum("time"))["time__sum"]
                if time == None:
                    time = "----"
                else:
                    totaltime += time
                times_dict[user.username] = time
                timetrackerlist += list(time_tracks)
            else:
                for u in users:
                    time_tracks = (
                        f_man(date=date)
                         .filter(tester__id=u.id)
                         .filter(newest=True)
                    )
                    time_tracker_dict[u.username] = time_tracks
                    time = time_tracks.aggregate(Sum("time"))["time__sum"]
                    if time == None:
                        time = "----"
                    else:
                        totaltime += time
                    times_dict[u.username] = time
                    timetrackerlist += list(time_tracks)

        day = Day(daydate, daydate.strftime("%a"), times_dict, totaltime)
        day.time_tracks = time_tracker_dict
        for timetracker in timetrackerlist:
            allnotes += "%s: Project - %s, %s: %s\n" % (
                            timetracker.tester.get_full_name(),
                            timetracker.project.title,
                            timetracker.associated_item.type_label.capitalize(),
                            timetracker.associated_item.title
            )
            allnotes += "%s -\n" % timetracker.title
            allnotes += "%s\n" % timetracker.body
        day.allnotes = allnotes
        week.add_day(day)
        if len(week.days) == 7 or idx == end:
            if week.total == Decimal(0.00):
                ne = no_entry()
                week.users = [ne]
                week.no_entries = True
            else:
                week.users = users
                week.userhours()
            weeks.append(week)
            week = Week()
    return weeks


###############################################################################
@login_required(login_url="/login/")
def get_week(request):
    user = request.user
    uc = user.tester.context
    weeks = _get_week(uc)
    context["weeks"] = weeks
    return render(request, "display_week.html", context)


###############################################################################
@login_required(login_url="/login/")
def timetracker(request):
    today = timezone.now()
    week_start = get_start_of_week(today)
    week_end = week_start + timezone.timedelta(days=6)
    timetracker_list = Time_Entry.objects.all().aggregate(Sum("time"))["time__sum"]
    get_context_items(context,request)
    request.user.tester.project = None
    context.pop("project", None)

    uc = request.user.tester.context
    uc.tt_date_range_start = week_start
    uc.tt_date_range_end = week_end
    uc.tt_user_filter = "all"
    uc.save()

    form = TEF()
    context["form"] = form

    val = request.GET.get("val", False)
    if not val:
        val = request.user.tester.context.tt_fields_sort_by

    context["section"] = "TimeTracker"
    context["entries"] = (
        Time_Entry.objects.filter(date__range=[week_start,week_end])
         .filter(newest=True)
         .order_by(val)
    )
    context["all_projects"] = Project.objects.all()
    context["all_users"] = User.objects.all()
    context["today"] = today
    context["where"] = "timetracker"
    context["title"] = "TimeTracker"
    context["audits"] = initial_audits(False, "timetracker", 10)
    context["time"] = "%s hours" % timetracker_list
    context["context"] = uc
    context["from"] = week_start.strftime("%Y-%m-%d")
    context["to"] = week_end.strftime("%Y-%m-%d")
    context["start"] = week_start
    context["end"] = week_end
    range_total = context["entries"].aggregate(Sum("time"))["time__sum"]
    if range_total == None or range_total == "None":
        range_total = Decimal(0.00)
    context["total_hours"] = range_total
    weeks = _get_week(uc)
    context["weeks"] = weeks
    return render(request, "timetracker.html", context)


###############################################################################
@login_required(login_url="/login/")
def display_time_entries(request):
    user = request.user
    user = User.objects.get(id=user.id)
    uc = user.tester.context
    val = uc.tt_fields_sort_by
    p_id = uc.tt_project_filter
    f_date = uc.tt_date_range_start
    t_date = uc.tt_date_range_end
    u_id = uc.tt_user_filter
    context["search"] = uc.tt_search_bar
    if not val:
        val = "date"

    f_man = Time_Entry.objects.filter
    if p_id != "all":
        if u_id != "all":
            context["entries"] = (
                f_man(date__range=[f_date,t_date])
                 .filter(project__id=p_id)
                 .filter( newest=True).filter(tester__id=u_id)
                 .order_by(val)
            )
        else:
            context["entries"] = (
                f_man(date__range=[f_date,t_date])
                 .filter(project__id=p_id)
                 .filter(newest=True)
                 .order_by(val)
            )
    else:
        if u_id != "all":
            context["entries"] = (
                f_man(date__range=[f_date,t_date])
                 .filter(tester__id=u_id)
                 .filter( newest=True)
                 .order_by(val)
            )
        else:
            context["entries"] = (
                f_man(date__range=[f_date,t_date])
                 .filter( newest=True)
                 .order_by(val)
            )
    return render(request,"display_time_entries.html",context)

###############################################################################
def entry_add_form(request):
    form = TEF()
    context["form"] = form
    return render(request, "entry_add_form.html", context)


###############################################################################
@login_required(login_url="/login/")
def add_time_entry(request):
    # if request.method == 'POST':
    task_id = request.POST.get("task", False)
    if task_id:
        task = Task.objects.get(id=task_id)
    form = TEF(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.time = Decimal(request.POST.get("time", 0))
        entry.date = request.POST.get("date", None)
        entry.tester = request.user
        entry.newest = True
        if task:
            entry.associated_item = task
            task.tsk_duration = task.tsk_duration + entry.time
            task.save()
            audit = action_audit(
                request.user,
                "added time entry - %s to %s" % (entry.title, task.title),
                "timetracker",
                timezone.now(),
                entry.project,
                entry,
            )
        entry.save()
        audit = action_audit(
            request.user,
            "added time entry %s" % (entry.title),
            "timetracker",
            timezone.now(),
            entry.project,
            entry,
        )
        return HRR("/display_time_entries/")
    else:
        return JR(form.errors)
        # else:
        # return HR('Not Authorized!')


###############################################################################
@login_required(login_url="/login/")
def add_time_entry_for_task(request):
    task_id = request.POST.get("task_id", False)
    task = Task.objects.get(id=task_id)
    form = TEF(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.associated_item = task
        entry.project = task.project
        entry.date = request.POST.get("date", None)
        entry.tester = request.user
        entry.save()
        return HR("success")
    else:
        return JR(form.errors)


###############################################################################
@login_required(login_url="/login/")
def task_time_entry_form(request):
    form = TTEF()
    context["form"] = form
    return render(request, "task_time_entry_form.html", context)


###############################################################################
@login_required(login_url="/login/")
def get_tasks_for_project(request):
    p_id = request.GET.get("p_id", False)
    if p_id:
        tasks = Task.objects.filter(project__id=p_id)
        context["tasks"] = tasks
        return render(request, "render_task_options.html", context)
    else:
        return HR("invalid project")


###############################################################################
@login_required(login_url="/login/")
def delete_time_entry(request):
    delete_time_entry = request.POST.get("del_time_entry_id")
    entry = Time_Entry.objects.filter(id=delete_time_entry)
    entry.delete()
    return HR("success")


###############################################################################
@login_required(login_url="/login/")
def time_entry_add(request):
    if request.method == "POST":
        user = request.user
        form = TTEF(request.POST)
        app = request.POST.get("app", False)
        model = request.POST.get("model", False)
        uid = request.POST.get("id", False)
        where = request.POST.get("where", False)
        date = request.POST.get("date", timezone.now())
        time = request.POST.get("time", 0.00)
        if app and model and uid:
            instance = getattr(sys.modules["%s.models"%app], "%s" % model).objects.get(id=uid)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.tester = user
            time_entry.project = user.tester.project
            time_entry.associated_item = instance
            time_entry.date = date
            time_entry.time = Decimal(time)
            time_entry.newest = True
            time_entry.save()
            audit = action_audit(request.user,
                                 "added time entry - for %s" % (instance.audit_label),
                                 where,
                                 timezone.now(),
                                 time_entry.project,
                                 time_entry)
            return JR({"success":"success"})
        else:
            return JR({"errors":form.errors})
    else:
        return HR("Not Authorized")


################################################################################
@login_required(login_url="/login/")
def time_entry_add_form(request):
    form = TTEF()
    context["form"] = form
    context["submit_id"] = request.GET.get("submit_id", "")
    context["action"] = request.GET.get("action", "")
    return render(request,"time_entry_form.html", context)


################################################################################
@login_required(login_url="/login/")
def time_entry_edit_form(request):
    eid = request.GET.get("id", False)
    entry = get_object_or_404(Time_Entry, id=eid)
    form = TTEF(instance=entry)
    form.fields["time"].initial = entry.time
    form.fields["date"].initial = entry.date
    context["timetracker_id"] = eid
    context["form"] = form
    context["action"] = request.GET.get("action", "")
    context["form_id"] = request.GET.get("form_id", "")
    context["submit_id"] = request.GET.get("submit_id", "")
    context["cancel_class"] = request.GET.get("cancel_class", "btn-close-modal")
    return render(request,"time_entry_form.html", context)


################################################################################
@login_required(login_url="/login/")
def time_entry_edit(request):
    get_context_items(context, request)
    if request.method == "POST":
        user = request.user
        uid = request.POST.get("id", False)
        instance = get_object_or_404(Time_Entry, id=uid)
        form = TEF(request.POST)
        date = request.POST.get("date", instance.date)
        time = request.POST.get("time", instance.time)
        title = request.POST.get("title", instance.title)
        body = request.POST.get("body", instance.body)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.date = date
            entry.time = Decimal(time)
            entry.time_entry = True
            entry.associated_item = instance.associated_item
            entry.ancestor = instance
            entry.project = instance.project
            entry.newest = True
            entry.tester = user
            entry.save()
            instance.newest = False
            instance.child = entry
            instance.save()

            audit = action_audit(user,
                                 "updated entry - %s" % (instance.title),
                                 "timetracker",
                                 timezone.now(),
                                 instance.project,
                                 instance)
            return HRR("/display_time_entries/")
        else:
            return JR({"errors": form.errors})
    else:
        return HR("Not Authorized")
