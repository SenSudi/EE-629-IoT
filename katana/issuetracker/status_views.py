from utils.imports import *

from models import Status as S

from forms import StatusForm as SF

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
def it_status_add_form(request):
    form = SF()
    context["form"] = form
    context["action"] = S.submit_url
    context["form_id"] = "form-it-status-add"
    context["cancel_btn_type"] = "status"
    context["add_btn_type"] = "status"
    return render(request, "it_status_add_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def status_new_obj(request):
    status = S(title="Add a title..")
    sequence_list = list(S.objects.values_list("sequence", flat=True))
    if 0 in sequence_list:
        return JR({"errors": "Please update the new status before adding another"})
    status.sequence = 0
    status.save()
    context["status"] = status
    return render(request, "status_new_obj.html", context)


###############################################################################
# EDIT #
########
@login_required(login_url="/login/")
def it_status_update_form(request):
    form = SF()
    context["form"] = form
    context["action"] = "/it_status_update/"
    context["form_id"] = "form-it-status-update"
    context["cancel_btn_type"] = "status"
    context["add_btn_type"] = "status"
    return render(request, "it_status_update_modal.html", context)


###############################################################################
# DETAILS #
###########
@login_required(login_url="/login/")
def it_status_details(request):
    return render(request, "it_issue_details.html", context)


###############################################################################
@login_required(login_url="/login/")
def it_status_manage(request):
    context["statuses"] = S.objects.all().order_by("sequence")
    return render(request, "it_status_manage.html", context)


###############################################################################
###############################################################################
###							MODEL HANDELING VIEWS							###
###############################################################################
###############################################################################
# ADD #
#######
@login_required(login_url="/login/")
def it_status_add(request):
    # add accounting for multi-selects
    form = SF(request.POST)
    if form.is_valid():
        status = form.save()
        return HRR("/status_select_field/?id=%s" % status.id)
    else:
        return JR({"errors": form.errors})


###############################################################################
# EDIT #
########
@login_required(login_url="/login/")
def it_status_update(request):
    sid = request.POST.get("id", False)
    status = get_object_or_404(S, id=sid)
    form = SF(request.POST, instance=status)
    if form.is_valid():
        udpated = form.save()
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


###############################################################################
@login_required(login_url="/login/")
def it_status_edit(request):
    sid = request.POST.get("id", False)
    status = get_object_or_404(S, id=sid)
    content = request.POST.get("content", False)
    content_type = request.POST.get("content_type", False)
    seq = request.POST.get("seq", False)
    if content:
        if content_type == "title":
            if content != status.title:
                status.title = content
                status.save()
                return JR({"success": "success"})
            return JR({"errors": {"title": "no change has been made"}})
        elif content_type == "sequence":
            val = int(content)
            sequence_list = list(S.objects.values_list("sequence", flat=True))
            max_sequence = max(sequence_list)
            min_sequence = S.min_sequence
            if val in sequence_list:
                if val < (max_sequence + 1) and val >= min_sequence:
                    statuses = S.objects.filter(sequence__gte=val)
                    for s in statuses:
                        s.sequence = F("sequence") + 1
                        s.save()
                    status.sequence = val
                    status.save()
                    return JR({"success": "success"})
                else:
                    return JR(
                        {
                            "errors": {
                                "sequence": "sequence must be between 1 and %s"
                                % (max_sequence + 1)
                            }
                        }
                    )
            else:
                status.sequence = val
                status.save()
                return JR({"success": "success"})
        else:
            return JR({"errors": "no content type"})

    elif seq:
        if seq == "down":
            lowest = max(S.objects.exclude(id=sid).values_list("sequence", flat=True))
            if status.sequence == lowest + 1:
                pass
            else:
                try:
                    s = S.objects.get(sequence=status.sequence + 1)
                except:
                    pass
                else:
                    s.sequence = F("sequence") - 1
                    s.save()
                    status.sequence = F("sequence") + 1
                    status.save()
            return JR({"success": "success"})
        if seq == "up":
            if status.sequence == S.min_sequence:
                pass
            else:
                try:
                    s = S.objects.get(sequence=status.sequence - 1)
                except:
                    pass
                else:
                    s.sequence = F("sequence") + 1
                    s.save()
                    status.sequence = F("sequence") - 1
                    status.save()
            return JR({"success": "success"})
    else:
        return JR({"errors": "no content was submitted"})


###############################################################################
# DELETE #
##########
@login_required(login_url="/login/")
def it_status_delete(request):
    sid = request.POST.get("id", False)
    status = get_object_or_404(S, id=sid)
    status.delete()
    return JR({"success": "Status successfully deleted"})


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
# STATUS SELECT FIELD OPTIONS #
###############################
@login_required(login_url="/login/")
def status_select_field(request):
    sid = request.GET.get("id", False)
    context["selection"] = get_object_or_404(S, id=sid)
    context["statuses"] = S.objects.all()
    return render(request, "status_select_field.html", context)


###############################################################################
# STATUS OBJECT LIST #
######################
@login_required(login_url="/login/")
def display_statuses(request):
    context["statuses"] = S.objects.all()
    return render(request, "display_statuses.html", context)


###############################################################################
