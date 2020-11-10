from django.shortcuts import render, get_object_or_404
from project.views import get_context_items
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR
from django.utils import timezone

from tools import get_issues

# from auditor.views import action_audit

# from models import Issue as I
# from models import Status as S

# from forms import IssueForm as IF
# from forms import IssueUpdateForm as IUF
# from forms import StatusForm as SF

from project.models import Project

# from django.contrib.auth.models import User
# from contacts.models import Contact
# from files.models import Issue_File as IFile
# from files.models import Associated_File as AF

# from auditor.models import Action
from auditor.utils import initial_audits

context = {}

# Create your views here.
###############################################################################
###############################################################################
###									MAIN VIEW 								###
###############################################################################
###############################################################################
@login_required(login_url="/login/")
def issue_tracker(request):
    get_context_items(context, request)
    context["section"] = "Issue Tracker"
    context["all_projects"] = Project.objects.all()
    issues = get_issues(request)
    context["tracked_issues"] = issues
    context["where"] = "issue_tracker"
    context["title"] = "Issue Tracker"
    context["audits"] = initial_audits(False, "issue_tracker", 10)
    try:
        project = user.tester.project
    except:
        pass
    else:
        context["current_project"] = project
    return render(request, "issue_tracker.html", context)


###############################################################################
# @login_required(login_url='/login/')
# def it_status_add_form(request):
# 	form 								= SF()
# 	context['form'] 					= form
# 	context['action'] 					= S.submit_url
# 	context['form_id'] 					= 'form-it-status-add'
# 	context['cancel_btn_type'] 			= 'status'
# 	context['add_btn_type'] 			= 'status'
# 	return render(request,'it_status_add_modal.html',context)
###############################################################################
# @login_required(login_url='/login/')
# def it_status_add(request):
# 	#add accounting for multi-selects
# 	form = SF(request.POST)
# 	if form.is_valid():
# 		status = form.save()
# 		return HRR('/status_select_field/?id=%s'%status.id)
# 	else:
# 		return JR({'errors':form.errors})
###############################################################################
# @login_required(login_url='/login/')
# def status_select_field(request):
# 	sid = request.GET.get('id',False)
# 	context['selection'] = get_object_or_404(S,id=sid)
# 	context['statuses'] = S.objects.all()
# 	return render(request,'status_select_field.html',context)
###############################################################################
# @login_required(login_url='/login/')
# def issue_details(request):
#     issue = get_object_or_404(I,id=request.GET.get('item_id',None))
#     form = IUF(instance=issue)
#     context['form'] = form
#     return render(request,'model_form.html',context)
###############################################################################
# @login_required(login_url='/login/')
# def issue_update(request):
# 	issue = get_object_or_404(I,id=request.POST.get('id',None))
# 	form = IUF(request.POST or None,instance=issue)
# 	if form.is_valid():
# 		updated = form.save()
# 		updated.issue_owner = get_owner(request.POST)
# 		updated.save()
# 		audit = action_audit(request.user,
# 							 'updated %s'%(updated.title),
# 							 'issue_tracker',
# 							 timezone.now(),
# 							 updated.project,
# 							 updated)
# 		if request.FILES.getlist('issue_file',False):
# 			for item in request.FILES.getlist('issue_file'):
# 					new_file = IFile(file=item,
# 									 uploader=request.user,
# 									 issue_number=updated.issue_number,
# 									 associated_project=updated.project)
# 					new_file.filename = make_issue_file_name(item,updated)
# 					new_file.save()
# 					updated.issue_files.add(new_file)
# 					updated.save()
# 					audit = action_audit(request.user,
# 										 'added %s to %s'%(new_file.filename,updated.title),
# 										 'issue_tracker',
# 										 timezone.now(),
# 										 new_file.project.get(),
# 										 new_file)
# 		if request.FILES.get('associated_files',False):
# 				for item in request.FILES.getlist('associated_files'):
# 					new_file = AF(filename=item.name,
# 								  file=item,
# 								  subdirectory='issues/%s/associated_files'%updated.issue_number,
# 								  project=updated.project)
# 					new_file.save()
# 					audit = action_audit(request.user,
# 										 'added %s to %s'%(new_file.filename,updated.title),
# 										 'issue_tracker',
# 										 timezone.now(),
# 										 new_file.project,
# 										 new_file)
# 					new_issue.associated_files.add(new_file)
# 		return HRR('/display_tracked_issues/')
# 	else:
# 		return JR(form.errors)
###############################################################################
