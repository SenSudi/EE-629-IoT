from utils.imports import *
from .tools import get_issues
from .tools import get_owner
from .tools import get_and_make_issue_file
from .tools import issue_add_audit
from .tools import get_and_associate_files_to_issue

from models import Issue as I

from forms import IssueForm as IF
from forms import IssueUpdateForm as IUF

##################
# Global Context #
##################
context = {}
##################

###############################################################################
###############################################################################
###								FORM VIEWS									###
###############################################################################
###############################################################################
# ADD #
#######
@login_required(login_url="/login/")
def it_issue_add_form(request):
    form = IF()
    try:
        project = user.tester.project
    except:
        pass
    else:
        context["current_project"] = project
        form.fields["project"].initial = project.id
    context["form"] = form
    context["action"] = "/it_issue_add/"
    context["form_id"] = "form-it-issue-add"
    context["cancel_btn_type"] = "issue"
    context["add_btn_type"] = "issue"
    return render(request, "it_issue_add_modal.html", context)


###############################################################################
# EDIT #
########
@login_required(login_url="/login/")
def it_issue_update_form(request):
    iid = request.GET.get("id", False)
    issue = get_object_or_404(I, id=iid)
    form = IUF(instance=issue)
    context["form"] = form
    context["issue"] = issue
    context["action"] = "/it_issue_update/"
    context["form_id"] = "form-it-issue-update"
    context["cancel_btn_type"] = "issue"
    context["submit_btn_type"] = "issue"
    context["submit_text"] = "update"
    return render(request, "it_issue_update_modal.html", context)


###############################################################################
# DETAILS #
###########
@login_required(login_url="/login/")
def it_issue_details(request):
    iid = request.GET.get("id", False)
    context["issue"] = get_object_or_404(I, id=iid)
    return render(request, "it_issue_details.html", context)


###############################################################################
###############################################################################
###							MODEL HANDELING VIEWS							###
###############################################################################
###############################################################################
# ADD #
#######
@login_required(login_url="/login/")
def it_issue_add(request):
    user = request.user
    form = IF(request.POST)
    if form.is_valid():
        issue = form.save(commit=False)
        project = issue.project
        issue.author = user
        issue.issue_owner = get_owner(request.POST)
        issue.issue_number = project.issue_number
        issue.save()
        issue.contributors.add(user)

        get_and_make_issue_file(request, issue)
        issue_add_audit(request, issue)
        get_and_associate_files_to_issue(request, issue)

        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
# EDIT #
########
@login_required(login_url="/login/")
def it_issue_update(request):
    iid = request.POST.get("id", False)
    issue = get_object_or_404(I, id=iid)
    form = IUF(request.POST, instance=issue)
    if form.is_valid():
        updated = form.save()
        updated.issue_owner = get_owner(request.POST)
        updated.save()
        audit = action_audit(
            request.user,
            "updated %s" % (updated.title),
            "issue_tracker",
            timezone.now(),
            updated.project,
            updated,
        )
        get_and_make_issue_file(request, updated)
        # if request.FILES.getlist('issue_file',False):
        # 	for item in request.FILES.getlist('issue_file'):
        # 			new_file = IFile(file=item,
        # 							 uploader=request.user,
        # 							 issue_number=updated.issue_number,
        # 							 associated_project=updated.project)
        # 			new_file.filename = make_issue_file_name(item,updated)
        # 			new_file.save()
        # 			updated.issue_files.add(new_file)
        # 			updated.save()
        # 			audit = action_audit(request.user,
        # 								 'added %s to %s'%(new_file.filename,updated.title),
        # 								 'issue_tracker',
        # 								 timezone.now(),
        # 								 new_file.project.get(),
        # 								 new_file)

        # if request.FILES.get('associated_files',False):
        # 		for item in request.FILES.getlist('associated_files'):
        # 			new_file = AF(filename=item.name,
        # 						  file=item,
        # 						  subdirectory='issues/%s/associated_files'%updated.issue_number,
        # 						  project=updated.project)
        # 			new_file.save()
        # 			audit = action_audit(request.user,
        # 								 'added %s to %s'%(new_file.filename,updated.title),
        # 								 'issue_tracker',
        # 								 timezone.now(),
        # 								 new_file.project,
        # 								 new_file)
        # 			new_issue.associated_files.add(new_file)
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
# DELETE #
##########
# @login_required(login_url='/login/')
# def it_issue_add_form(request):
###############################################################################
# EXPORT #
##########
# @login_required(login_url='/login/')
# def it_issue_add_form(request):
###############################################################################
###############################################################################
###							OBJECT DISPLAY VIEWS							###
###############################################################################
###############################################################################
# ISSUES #
##########
@login_required(login_url="/login/")
def display_tracked_issues(request):
    issues = get_issues(request)
    context["tracked_issues"] = issues
    return render(request, "display_tracked_issues.html", context)


###############################################################################
