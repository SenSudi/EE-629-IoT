from models import Action


def initial_audits(project, where, howmany):
    howmany += 1
    if project and where == "overview":
        audits = list(project.action_set.all().order_by("-when"))[:howmany]
    elif project:
        audits = list(project.action_set.filter(where=where).order_by("-when"))[:howmany]
    else:
        audits = list(Action.objects.filter(where=where).order_by("-when"))[:howmany]
    return audits
