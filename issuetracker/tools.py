from utils.imports import *

from models import Issue as I
from django.contrib.auth.models import User
from contacts.models import Contact

from files.models import Issue_File as IFile
from files.models import Associated_File as AF

###############################################################################
def make_issue_file_name(file, issue):
    ##############
    # Local Vars #
    ##############
    codename = issue.project.codename
    issue_number = issue.issue_number
    extension = file.name[file.name.rfind(".") :]
    date = issue.date
    ##################################################
    # If the issue report has been given a client designation
    if len(issue.client_issue_designation) > 0:
        cid = issue.client_issue_designation
    else:
        cid = False
        # If the issue already contains an Issue File
    if issue.issue_files.all().count() > 0:
        # If the lastest file's date is not the same as today's date
        if issue.latest_issue_file().updated.date() != issue.updated.date():
            # Set the daily version to the baseline value of 01
            daily_version = issue.daily_version = 1
            # Increment the daily version for the next file
            issue.daily_version += 1
            issue.save()
            # If the lastest file's date is the same as today's date
        else:
            # Get the initial version number from the issue report
            daily_version = issue.daily_version
            # Increment the daily version for the next file upload
            issue.daily_version += 1
            issue.save()
            # If the issue does not have an Issue File
    else:
        # Set the daily version to the baseline value of 01
        daily_version = issue.daily_version = 1
        # Increment the daily version for the next file upload
        issue.daily_version += 1
        issue.save()
        # If a client designation is present
    if cid:
        return "Issue%s-%s-%s-%s-v%s%s" % (
            issue_number,
            codename,
            cid,
            date,
            daily_version,
            extension,
        )
        # Otherwise
    else:
        return "Issue%s-%s-%s-v%s%s" % (
            issue_number,
            codename,
            date,
            daily_version,
            extension,
        )


###############################################################################
def get_owner(post):
    if post.get("issue_owner", False):
        value = post["issue_owner"]
        if "u" in value:
            user = User.objects.get(id=value[1:])
            owner = user.tester
        elif "c" in value:
            owner = Contact.objects.get(id=value[1:])
        else:
            owner = None
        return owner


###############################################################################
def get_issues(request):
    if request.method == "GET":
        p_id = request.GET.get("p_id", False)
        val = request.GET.get("val", "issue_number")
    else:
        val = "issue_number"
        # if val == 'issue_owner':
        # 	val = coalesce('tester_owner__user__first_name','contact_owner__first_name')
    if p_id:
        if p_id != "all":
            if val == "issue_owner":
                issues = I.objects.filter(project__id=p_id).order_by(
                    Coalesce(
                        "tester_owner__user__first_name", "contact_owner__first_name"
                    )
                )
            else:
                issues = I.objects.filter(project__id=p_id).order_by(val)
        else:
            if val == "issue_owner":
                issues = I.objects.all().order_by(
                    Coalesce(
                        "tester_owner__user__first_name", "contact_owner__first_name"
                    )
                )
            else:
                issues = I.objects.all().order_by(val)
    else:
        if val == "issue_owner":
            issues = I.objects.all().order_by(
                Coalesce("tester_owner__user__first_name", "contact_owner__first_name")
            )
        else:
            issues = I.objects.all().order_by(val)
    return issues


###############################################################################
def get_and_make_issue_file(request, issue):
    project = issue.project
    number = issue.issue_number
    user = request.user
    if request.FILES.get("issue_file", False):
        raw_file = request.FILES.get("issue_file")
        issue_file = IFile(
            file=raw_file,
            uploader=user,
            issue_number=number,
            associated_project=project,
        )
        issue_file.associated_project = project
        issue_file.filename = make_issue_file_name(raw_file, issue)
        issue_file.save()

        issue.issue_files.add(issue_file)
        # Execute an audit for Issue File Creation
        issue_file_audit = action_audit(
            user,
            "added %s to %s" % (issue_file.filename, issue.title),
            "issue_tracker",
            timezone.now(),
            project,
            issue_file,
        )


###############################################################################
def issue_add_audit(request, issue):
    issue_audit = action_audit(
        request.user,
        "opened issue - %s for %s" % (issue.title, issue.project),
        "issue_tracker",
        timezone.now(),
        issue.project,
        issue,
    )


def get_and_associate_files_to_issue(request, issue):
    # If files were uploaded - Create Asssociated Files
    if request.FILES.get("associated_files", False):
        for raw_file in request.FILES.getlist("associated_files"):
            a_file = AF(
                filename=raw_file.name,
                file=raw_file,
                subdirectory="issues/%s/associated_files" % issue.issue_number,
                associated_item=issue,
            )
            a_file.save()
            a_file_audit = action_audit(
                request.user,
                "added %s to %s" % (a_file.filename, issue.title),
                "issue_tracker",
                timezone.now(),
                issue.project,
                a_file,
            )
            issue.associated_files.add(a_file)
