from models import Associated_File as AF
from models import Issue_File
from issuetracker.models import Issue as I

# from utils.imports import *

from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from django.utils.safestring import mark_safe
from django.utils import timezone

from auditor.views import action_audit
from auditor.utils import initial_audits
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from forms import FileUploadForm as FUF
from forms import BothFilesForm as BFF

from issuetracker.tools import get_and_make_issue_file, get_and_associate_files_to_issue

context = {}

# Create your views here.
@login_required(login_url="/login/")
def display_project_files(request):
    project = request.user.tester.project
    user = request.user
    all_assod_files = project.associated_files.all()
    val = request.GET.get("val", False)
    if not val:
        val = "updated"
    if val == "extension":
        context["associated_files"] = sorted(
            all_assod_files, key=lambda f: f.extension, reverse=False
        )
    elif val == "size":
        context["associated_files"] = sorted(
            all_assod_files, key=lambda f: f.file.size, reverse=True
        )
    else:
        context["associated_files"] = all_assod_files.order_by("-%s" % val)
    return render(request, "display_files.html", context)


@login_required(login_url="/login/")
def files_list(request):
    app = request.GET.get("app", False)
    model_type = request.GET.get("model_type", False)
    model_id = request.GET.get("model_id", False)
    model = getattr(sys.modules["%s.models" % app], "%s" % model_type).objects.get(
        id=model_id
    )
    context["files"] = model.files.all()
    return render(request, "files_list.html", context)


@login_required(login_url="/login/")
def file_delete(request):
    try:
        from utils import permtools as pt
    except:
        return JR({"error": "no tools"})
    user = request.user
    if user.is_authenticated:
        fid = request.POST.get("fid", False)
        if request.method == "POST":
            if fid:
                file = AF.objects.get(id=fid)
                if (
                    is_hv_admin(user)
                    or is_project_admin(user)
                    or is_db_admin(user)
                    or user == file.uploader
                ):
                    file.delete()
                    success = "File successfully deleted!"
                    return JR({"success": success})
                else:
                    error = "You do not have permission to delete this file!"
                    return JR({"error": error})
        else:
            if fid:
                file = AF.objects.get(id=fid)
                if (
                    is_hv_admin(user)
                    or is_project_admin(user)
                    or is_db_admin(user)
                    or user == file.uploader
                ):
                    success = "Are you sure you want to delete:<br>%s?" % file.filename
                    return JR({"success": success})
                else:
                    error = "You do not have permission to delete this file!"
                    return JR({"error": error})


###############################################################################
@login_required(login_url="/login/")
def afile_form(request):
    submit_id = request.GET.get("submit_id", "")
    action = request.GET.get("action", "")
    form_id = request.GET.get("form_id", "")
    cancel_class = request.GET.get("cancel_class", "")
    form = FUF()
    context["form"] = form
    context["action"] = action
    context["submit_id"] = submit_id
    context["form_id"] = form_id
    context["cancel_class"] = cancel_class
    return render(request, "afile_form.html", context)


@login_required(login_url="/login/")
def both_files_form(request):
    form = BFF()
    context["form"] = form
    context["action"] = "/upload_both_files/"
    context["form_id"] = "form-both-files"
    context["cancel_class"] = "it-modal-form-cancel"
    context["submit_id"] = "btn-modal-files-submit"
    return render(request, "both_files_form.html", context)


@login_required(login_url="/login/")
def upload_both_files(request):
    iid = request.POST.get("id", False)
    issue = get_object_or_404(I, id=iid)
    i_file = request.FILES.get("issue_file", False)
    if i_file:
        get_and_make_issue_file(request, issue)
    if len(request.FILES.getlist("associated_files", [])) > 0:
        get_and_associate_files_to_issue(request, issue)
    return JR({"success": "success"})


@login_required(login_url="/login/")
def get_files_list(request):
    iid = request.GET.get("id", False)
    issue = get_object_or_404(I, id=iid)
    context["files"] = issue.get_files()
    return render(request, "display_files_list.html", context)
