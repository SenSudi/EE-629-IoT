from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from models import Action

context = {}

# Create your views here.
def action_audit(who, what, where, when, project=False, item=False):
    audit = Action(who=who, what=what, where=where, when=when)
    if project:
        audit.project = project
    if item:
        audit.associated_item = item
    audit.save()
    return audit


@login_required(login_url="/login/")
def get_audits(request):
    where = request.GET.get("where", False)
    project = request.user.tester.project
    if where:
        if where == "overview":
            context["audits"] = list(project.action_set.all())[0:-20]
        else:
            audits = project.action_set.filter(where=where).order_by("-when")
            if audits.count() < 10:
                context["audits"] = audits
            else:
                context["audits"] = audits[:10]
    return render(request, "show_audits.html", context)
