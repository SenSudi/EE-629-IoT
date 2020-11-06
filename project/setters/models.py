from utils.imports import *

# Import Tools
from project.getters.models import get_project_phases

# Import Forms

# Import Models
from project.models import Milestone

context = {}


def new_vip(model, role_id):
    try:
        manager = getattr(sys.modules["project.models"], "Vip")
    except:
        from project.models import Vip

        manager = Vip
    try:
        rm = getattr(sys.modules["utils.models"], "Label")
    except:
        from utils.models import Label

        rm = Label
    try:
        c = getattr(sys.modules["contacts.models"], "Contact")
    except:
        from contacts.models import Contact

        c = Contact
    try:
        u = getattr(sys.modules["django.contrib.auth.models"], "User")
    except:
        from django.contrib.auth.models import User

        u = User

    vip = manager()
    role = get_object_or_404(rm, id=role_id)
    vip.role = role
    vip.person = model
    vip.guid = get_guid()
    vip.save()
    return vip


@login_required(login_url="/login/")
def new_vip_f_npf(request):
    try:
        manager = getattr(sys.modules["project.models"], "Vip")
    except:
        from project.models import Vip

        manager = Vip
    try:
        rm = getattr(sys.modules["utils.models"], "Label")
    except:
        from utils.models import Label

        rm = Label
    try:
        c = getattr(sys.modules["contacts.models"], "Contact")
    except:
        from contacts.models import Contact

        c = Contact
    try:
        u = getattr(sys.modules["django.contrib.auth.models"], "User")
    except:
        from django.contrib.auth.models import User

        u = User

    vip = manager()
    role_id = request.POST.get("r_id", None)
    role = get_object_or_404(rm, id=role_id)
    person_id = request.POST.get("p_id", "")
    if "c" in person_id:
        person = get_object_or_404(c, id=person_id[1:])
    if "u" in person_id:
        person = get_object_or_404(u, id=person_id[1:])
    vip.role = role
    vip.person = person
    vip.guid = get_guid()
    vip.save()
    return JR(
        {"model": {"value": vip.id, "display": "%s - %s" % (vip.role, vip.person)}}
    )


def set_milestone_phases(milestone):
    for phase in get_project_phases(milestone.project):
        milestone.phases.add(phase)
    return milestone.phases.count()


def milestone_constructor(
    project, hours=False, start=False, end=False, title=False, comment=False
):
    TITLE = "Project Completion"
    milestone = Milestone()
    if title:
        milestone.title = title
    else:
        milestone.title = TITLE
    milestone.project = project
    if hours:
        milestone.hours = hours
    else:
        milestone.hours = project.contract_hours
    if start:
        milestone.start_date = start
    else:
        milestone.start_date = project.start_date
    if end:
        milestone.end_date = end
    else:
        milestone.end_date = project.end_date
    if comment:
        milestone.comment = comment
    else:
        milestone.comment = " "
    milestone.save()
    return milestone
