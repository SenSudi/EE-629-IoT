from utils.imports import *
from project.views import get_context_items
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from models import Report_Item_Type
from models import Report_Item as RI
from models import Report_Item_Attribute
from models import Static_Attribute
from models import Wizard_Template
from models import Wizard_Step
from models import Report_Variable
from models import Wizard_Variable
from models import Report
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from forms import ReportItemForm as RIF
from forms import ReportItemTypeForm as RITF
from forms import ReportItemSimpleForm as RISF
from forms import WizardForm as WF
from forms import StepForm as SF
from forms import ReportVariableForm as RVF
from forms import ReportTypeForm as RTF

from files.models import Associated_File

from docxtpl import DocxTemplate

context = {}

# Create your views here.


def prep_JSON(model):
    json = {}
    json["title"] = model.title
    # obj_attrs.title     = object.attr('data-obj-title');
    json["type"] = model.type_label
    # obj_attrs.type      = object.attr('data-obj-type');
    json["app"] = model.app_label
    # obj_attrs.app       = object.attr('data-obj-app');
    json["model"] = model.model_class
    # obj_attrs.model     = object.attr('data-obj-model');
    json["id"] = model.id
    # obj_attrs.id        = object.attr('data-obj-id');
    json["edit"] = model.edit_url
    # obj_attrs.edit      = object.attr('data-edit');
    # obj_attrs.details   = object.attr('data-details');
    # obj_attrs.delete    = object.attr('data-delete');
    # obj_attrs.note_form = object.attr('data-note-form');
    # obj_attrs.file_form = object.attr('data-file-form');
    return json


################################################################################
################################################################################
## PAGES ##
###########
@login_required(login_url="/login/")
def template_manager(request):
    get_context_items(context, request)
    context["section"] = "Wizard Template Manager"
    context["wizards"] = Wizard_Template.objects.all().order_by("-title")
    context["add_url"] = Wizard_Template.add_url
    return render(request, "db_template_manager.html", context)


################################################################################
@login_required(login_url="/login/")
def report_wizard(request):
    get_context_items(context, request)
    context["section"] = "Report Wizard"
    context["wizards"] = Wizard_Template.objects.all().order_by("-title")
    context["reports"] = Report.objects.all()
    context["add_url"] = Report.add_url
    context["report_files"] = Associated_File.objects.filter(subdirectory="reports")
    return render(request, "report_wizard.html", context)


################################################################################
################################################################################
## FORMS ##
###########
# ADD #
#######
@login_required(login_url="/login/")
def report_add_form(request):
    form = RTF()
    context = {}
    context["form"] = form
    return render(request, "report_add_form.html", context)


################################################################################
@login_required(login_url="/login/")
def report_add(request):
    title = request.GET.get("title", False)
    wizard_id = request.GET.get("wizard", False)
    wizard = get_object_or_404(Wizard_Template, id=wizard_id)
    report = Report(
        guid=get_guid(),
        lineage_guid=get_guid(),
        title=title,
        wizard=wizard,
        author=request.user,
    )
    report.save()
    for step in report.wizard.steps.all():
        variables = step.variables.all()
        scopy = step.copy()
        scopy.wizard = None
        scopy.report = report
        scopy.save()
        for variable in variables:
            vcopy = variable.copy()
            vcopy.step = scopy
            vcopy.save()
    context["report"] = report
    context["wizard"] = report.wizard
    return render(request, "report_add_form.html", context)


################################################################################
@login_required(login_url="/login/")
def wizard_var_item_add(request):
    vid = request.GET.get("id", False)
    var = get_object_or_404(Wizard_Variable, id=vid)
    label = var.variable
    form = RISF()
    context["var"] = var
    context["label"] = label
    context["form"] = form
    return render(request, "wizard_var_item_add.html", context)


################################################################################
@login_required(login_url="/login/")
def wizard_var_item_submit(request):
    vid = request.POST.get("id", False)
    var = get_object_or_404(Wizard_Variable, id=vid)
    tid = request.POST.get("extra", False)
    item_type = get_object_or_404(Report_Item_Type, id=tid)
    form = RISF(request.POST)
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.item_type = item_type
        new_item.contributor = request.user
        new_item.newest = True
        new_item.attrs["Title"] = [{"value": new_item.title, "input_type": "text"}]
        new_item.save()
        return JR(
            {
                "success": {
                    "item_type": new_item.item_type.label,
                    "id": new_item.id,
                    "title": new_item.title,
                }
            }
        )
    else:
        return JR({"errors": form.errors})


################################################################################
@login_required(login_url="/login/")
def wizard_template_modal(request):
    wid = request.GET.get("id", False)
    if wid:
        wt = get_object_or_404(Wizard_Template, id=wid)
        wf = WF(instance=wt)
        context["wt"] = wt
        try:
            context["first_step"] = wt.steps.get(sequence=1)
            context["steps"] = wt.steps.all().order_by("sequence")
        except:
            context["sf"] = SF()
        else:
            context["sf"] = SF(instance=context["first_step"])

    else:
        wf = WF()
        wf.fields["title"].intial = "New Wizard"
        sf = SF()
        context["sf"] = sf
        context["new"] = True
        context["wt"] = None
        context["first_step"] = None
        context["steps"] = None
    rvf = RVF()
    context["wf"] = wf
    context["rvf"] = rvf
    context["lf"] = RITF()
    return render(request, "wizard_template_modal.html", context)


################################################################################
@login_required(login_url="/login/")
def wizard_template_create(request):
    wt = Wizard_Template()
    wt.guid = get_guid()
    wt.lineage_guid = get_guid()
    wt.creator = request.user
    wt.save()
    response = prep_JSON(wt)
    return JR(response)


################################################################################
@login_required(login_url="/login/")
def wizard_template_step_add(request):
    wid = request.POST.get("id", False)
    wizard = get_object_or_404(Wizard_Template, id=wid)
    sequence = wizard.next_step()
    step = Wizard_Step()
    step.sequence = sequence
    step.guid = get_guid()
    step.lineage_guid = get_guid()
    step.save()
    wizard.steps.add(step)
    context["step"] = step
    return render(request, "wizard_template_step_tab.html", context)


################################################################################
@login_required(login_url="/login/")
def wizard_template_file_add(request):
    file = File(request.FILES.get("template", None))
    wid = request.POST.get("id", False)
    wizard = get_object_or_404(Wizard_Template, id=wid)
    wfile = Associated_File(
        guid=get_guid(),
        filename=file.name,
        file=file,
        subdirectory="wizards/%s" % wizard.title,
        uploader=request.user,
        associated_item=wizard,
    )
    wfile.save()
    wizard.template = wfile
    wizard.save()
    return JR({"success": "success"})


################################################################################
################################################################################
# EDIT #
########
@login_required(login_url="/login/")
def report_wizard_update(request):
    rid = request.POST.get("id", False)
    report = get_object_or_404(Report, id=rid)
    field = request.POST.get("field", False)
    value = request.POST.get("value", None)
    obj_type = request.POST.get("object", False)
    oid = request.POST.get("obj_id", False)
    if obj_type == "wizard_variable":
        var = get_object_or_404(Wizard_Variable, id=oid)
        if var.selectable:
            var.selected = []
            values = request.POST.getlist("value[]", [])
            for value in values:
                var.selected.append(value)
            var.save()
            report.save()
            return JR({"success": "updated selected"})
        if field and value:
            var.content = value
            var.save()
            report.save()
            return JR({"success": "updated content"})
        return JR({"error": "No field and value"})
    else:
        return JR({"error": "No object"})


################################################################################
@login_required(login_url="/login/")
def report_wizard_update_step_modified(request):
    rid = request.POST.get("id", False)
    report = get_object_or_404(Report, id=rid)
    sequence = request.POST.get("sequence", False)
    report.step_modified = sequence
    report.save()
    return JR({"success": "success"})


################################################################################
@login_required(login_url="/login/")
def wizard_template_edit(request):
    oid = request.POST.get("object_id", False)
    om = request.POST.get("object", "")
    fn = request.POST.get("field", "")
    content = request.POST.get("content", False)
    model = getattr(sys.modules["reports.models"], "%s" % str(om))
    instance = get_object_or_404(model, id=oid)
    field = getattr(instance, "%s" % str(fn))
    old_val = field
    if content:
        setattr(instance, "%s" % str(fn), content)
        instance.save()
        new_val = getattr(instance, "%s" % str(fn))
        return JR(
            {
                "success": "success updating %s from %s to %s for %s"
                % (fn, old_val, new_val, instance)
            }
        )
    else:
        return HR("Nothing to Save")


@login_required(login_url="/login/")
def wizard_template_deploy(request):
    wid = request.POST.get("id", False)
    deploy = request.POST.get("deploy", None)
    wizard = get_object_or_404(Wizard_Template, id=wid)
    if deploy is not None:
        if str(deploy) == "true":
            deploy = True
        elif str(deploy) == "false":
            deploy = False
        if type(deploy) == type(True):
            wizard.active = not deploy
            wizard.save()
            return JR({"success": "success"})
        else:
            return HR("No action!")


@login_required(login_url="/login/")
def db_wizard_step_var_add(request):
    sid = request.POST.get("id", False)
    step = get_object_or_404(Wizard_Step, id=sid)
    wizard = step.wizard
    var_type = request.POST.get("var_type", False)
    wv = Wizard_Variable()
    wv.guid = get_guid()
    wv.lineage_guid = get_guid()
    wv.step = step
    if var_type == "nc":
        display = request.POST.get("display", False)
        input_type = request.POST.get("input_type", False)
        limit = request.POST.get("limit", False)
        template = request.POST.get("template", False)
        new_var = Report_Variable()
        new_var.display = display
        new_var.input_type = input_type
        new_var.limit = limit
        new_var.template = template
        new_var.save()
        wv.variable = new_var
        wv.input_type = input_type
        wv.limited = True
        wv.limit = int(limit)
        wv.template_var = template
        wv.save()
    elif var_type == "c":
        var_ids = request.POST.getlist("var_ids[]", [])
        for var_id in var_ids:
            var = get_object_or_404(Report_Variable, id=var_id)
            wv = Wizard_Variable()
            wv.guid = get_guid()
            wv.lineage_guid = get_guid()
            wv.step = step
            wv.variable = var
            wv.input_type = var.input_type
            wv.limited = True
            wv.limit = var.limit
            wv.template_var = var.template
            wv.save()
    elif var_type == "np":
        var_label = request.POST.get("label", False)
        var = Report_Item_Type(title=var_label)
        var.guid = get_guid()
        var.lineage_guid = get_guid()
        var.save()
        select_type = request.POST.get("select", False)
        template_tag = request.POST.get("template", False)
        wv.variable = var
        if select_type and str(select_type) == "m":
            wv.selectable = True
            wv.multiple = True
            wv.input_type = "multi-select"
        elif select_type and str(select_type) == "s":
            wv.selectable = True
            wv.input_type = "single-select"
        if template_tag:
            wv.template_var = template_tag
        wv.save()
    elif var_type == "p":
        var_ids = request.POST.getlist("var_ids[]", [])
        for var_id in var_ids:
            var = get_object_or_404(Report_Item_Type, id=var_id)
            wv = Wizard_Variable()
            wv.guid = get_guid()
            wv.lineage_guid = get_guid()
            wv.step = step
            select_type = request.POST.get("select", False)
            template_tag = request.POST.get("template", False)
            wv.variable = var
            wv.template_var = template_tag
            if select_type and str(select_type) == "m":
                wv.selectable = True
                wv.multiple = True
                wv.input_type = "multi-select"
            elif select_type and str(select_type) == "s":
                wv.selectable = True
                wv.input_type = "single-select"
            wv.save()
    else:
        return JR({"error": "variable type not defined"})
    reports = Report.objects.filter(wizard__id=wizard.id)
    for report in reports:
        rstep = report.steps.get(lineage_guid=step.lineage_guid)
        vcopy = wv.copy()
        vcopy.step = rstep
        vcopy.save()
        if rstep.sequence < report.step_modified:
            report.step_modified = rstep.sequence
            report.save()
    return JR({"success": "success"})


@login_required(login_url="/login/")
def wizard_vriable_edit(request):
    vid = request.POST.get("id", False)
    var = get_object_or_404(Wizard_Variable, id=vid)
    field = request.POST.get("field", "")
    content = request.POST.get("content", False)
    step = var.step
    if content:
        reports = Report.objects.filter(wizard__id=step.wizard.id)
        for report in reports:
            rstep = report.steps.get(lineage_guid=step.lineage_guid)
            rvar = rstep.variables.get(lineage_guid=var.lineage_guid)
            setattr(rvar, "%s" % str(field), content)
            if content == "multi-select":
                rvar.multiple = True
            else:
                rvar.multiple = False
            rvar.save()
            if rstep.sequence < report.step_modified:
                report.step_modified = rstep.sequence
                report.save()
        setattr(var, "%s" % str(field), content)
        if content == "multi-select":
            var.multiple = True
        else:
            var.multiple = False
        var.save()
        return JR({"success": "success"})
    else:
        return HR("NO CONTENT!!!")


################################################################################
## DELETE ##
############
@login_required(login_url="/login/")
def wizard_step_var_remove(request):
    vid = request.POST.get("id", False)
    var = get_object_or_404(Wizard_Variable, id=vid)
    var.delete()
    report_variables = Wizard_Variable.objects.filter(lineage_guid=var.lineage_guid)
    for rvar in report_variables:
        rvar.delete()
    return JR({"success": "success"})


################################################################################
@login_required(login_url="/login/")
def report_delete(request):
    rid = request.POST.get("id", False)
    report = get_object_or_404(Report, id=rid)
    report.delete()
    return JR({"success": "report deleted"})


################################################################################
@login_required(login_url="/login/")
def delete_report_file(request):
    rid = request.POST.get("id", False)
    report_file = get_object_or_404(Associated_File, id=rid)
    report_file.delete()
    return JR({"success": "report_file deleted"})


################################################################################
## CONTENT ##
#############
@login_required(login_url="/login/")
def report_wizard_details(request):
    rid = request.GET.get("id", False)
    report = get_object_or_404(Report, id=rid)
    context = {}
    context["report"] = report
    context["wizard"] = report.wizard
    if report.step_modified == 0:
        context["last_step_modified"] = report.step_modified + 1
    else:
        context["last_step_modified"] = report.step_modified
    return render(request, "report_wizard_details.html", context)


################################################################################
@login_required(login_url="/login/")
def report_wizard_content(request):
    rid = request.GET.get("id", False)
    report = get_object_or_404(Report, id=rid)
    context["report"] = report
    context["wizard"] = report.wizard
    context["last_step_modified"] = report.step_modified
    return render(request, "report_wizard_content.html", context)


################################################################################
@login_required(login_url="/login/")
def display_reports(request):
    reports = Report.objects.all()
    context["reports"] = reports
    return render(request, "display_reports.html", context)


################################################################################
def display_report_files(request):
    context["report_files"] = Associated_File.objects.filter(subdirectory="reports")
    return render(request, "display_report_files.html", context)


################################################################################
@login_required(login_url="/login/")
def wizard_modal_step_content(request):
    sid = request.GET.get("id", False)
    step = get_object_or_404(Wizard_Step, id=sid)
    context["sf"] = SF(instance=step)
    context["step"] = step
    return render(request, "wizard_modal_step_content.html", context)


################################################################################
@login_required(login_url="/login/")
def db_display_wizards(request):
    context["wizards"] = Wizard_Template.objects.all().order_by("-title")
    return render(request, "db_display_wizards.html", context)


################################################################################
@login_required(login_url="/login/")
def db_wt_variable_list(request):
    context["variables"] = Report_Variable.objects.all()
    context["items"] = Report_Item_Type.objects.all()
    form = RVF()
    form.fields["display"].required = True
    form.fields["input_type"].required = True
    form.fields["limit"].required = True
    form.fields["template"].required = True
    context["rvf"] = form
    return render(request, "db_wt_variable_list.html", context)


################################################################################
@login_required(login_url='/login/')
def db_wt_variable_search(request):
    get_context_items(context, request)
    search_string = request.GET.get('search_string', None)
    type_select    = request.GET.get('type', None)
    if request.GET.get('exact_match', False) == 'true':
        exact_match = True
    else:
        exact_match = False
    if type_select =="report_item":
        context['items'] = []
        if exact_match:
            item_types = Report_Item_Type.objects.filter(Q(title__contains=search_string)).order_by('title')
        else:
            item_types = Report_Item_Type.objects.filter(Q(title__icontains=search_string)).order_by('title')
        context['items'] = item_types
        return render(request, 'wt_step_items.html', context)
    else:
        context['variables'] = []
        if exact_match:
             variables = Report_Variable.objects.filter(Q(display__contains=search_string)|Q(template__contains=search_string)|Q(input_type__contains=search_string)).order_by('display')
        else:
             variables = Report_Variable.objects.filter(Q(display__icontains=search_string)|Q(template__icontains=search_string)|Q(input_type__icontains=search_string)).order_by('display')
        context['variables'] = variables
        return render(request, 'wt_step_variables.html', context)


################################################################################
################################################################################
################################################################################


################################################################################
@login_required(login_url="/login/")
def report_items(request):
    get_context_items(context, request)
    context["section"] = "Report Items DB"
    item_types = Report_Item_Type.objects.all()
    context["items"] = []
    report_item_list = []
    for item_type in item_types:
        context["items"].append((item_type.id, item_type.title))
        report_item_list = RI.objects.filter(newest=True).order_by("title")
    paginator = Paginator(report_item_list, 20)
    page = request.GET.get("page")
    try:
        report_items = paginator.page(page)
    except PageNotAnInteger:
        report_items = paginator.page(1)
    except EmptyPage:
        report_items = paginator.page(paginator.num_pages)
    context["report_items"] = report_items
    return render(request, "report_items.html", context)


################################################################################
def report_items_add(request):
    if request.method == "GET":
        context = {}
        form = RIF()
        context["form"] = form
        context["item_type"] = Report_Item_Type.objects.all()
        return render(request, "report_variable_add_form.html", context)
    else:
        title = request.POST.get("title", None)
        attr_names = request.POST.getlist("names[]")
        attr_values = request.POST.getlist("values[]")
        attr_seq = request.POST.getlist("seq[]")
        attr_type = request.POST.getlist("type[]")
        form = RIF(request.POST)
        if form.is_valid():
            if title:
                item = form.save(commit=False)
                item.contributor = request.user
                item.save()
                report_item = RI.objects.get(id=item.id)
                ri_init = Report_Item_Attribute.objects.create(
                    title="Title",
                    value=[item.title],
                    input_type="text",
                    sequence=0,
                    item=report_item,
                )
                ri_init.save()
                for count in range(len(attr_names)):
                    if attr_values[count]:
                        attribute = Report_Item_Attribute.objects.create(
                            title=attr_names[count],
                            value=[attr_values[count]],
                            sequence=attr_seq[count],
                            input_type=attr_type[count],
                            item=report_item,
                        )
                    else:
                        attribute = Report_Item_Attribute.objects.create(
                            title=attr_names[count],
                            value=[""],
                            sequence=attr_seq[count],
                            input_type=attr_type[count],
                            item=report_item,
                        )
                    attribute.save()
                    if attribute.input_type == "list":
                        static_attr = Static_Attribute.objects.get(
                            title=attribute.title
                        )
                        for val in static_attr.values:
                            if [val] == attribute.value:
                                attribute.selected = static_attr.values.index(val)
                                attribute.value = static_attr.values
                                attribute.save()
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors})


################################################################################
@login_required(login_url="/login/")
def report_variable(request):
    get_context_items(context, request)
    variable = Report_Variable.objects.all().order_by("display")
    page = request.GET.get("page")
    paginator = Paginator(variable, 20)
    try:
        variable_page = paginator.page(page)
    except PageNotAnInteger:
        variable_page = paginator.page(1)
    except EmptyPage:
        variable_page = paginator.page(paginator.num_pages)
    context["variable_page"] = variable_page
    return render(request, "report_variable.html", context)


################################################################################
@login_required(login_url="/login/")
def display_report_items(request):
    report_items = RI.objects.all()
    context["report_items"] = report_items
    return render(request, "display_report_items.html", context)


@login_required(login_url="/login/")
def create_item_type(request):
    if request.method == "POST":
        item_type_label = request.POST.get("new-item-type", False)
        if item_type_label:
            new_item_type = Report_Item_Type(title=item_type_label)
            new_item_type.save()
            item_type_dict = {}
            type_init = Report_Item_Attribute.objects.create(
                title="Title",
                item_type=new_item_type,
                value=[""],
                input_type="text",
                sequence=0,
            )
            type_init.save()
            new_item_type.attributes = Report_Item_Attribute.objects.filter(
                item_type=new_item_type
            ).order_by("sequence")
            new_item_type.save()
            for item in Report_Item_Type.objects.all():
                item_type_dict[item.id] = item.title
            return JR({"success": item_type_dict})
        else:
            return JR({"errors": "Please enter a label"})
    else:
        return HR("Not Authorized")


@login_required(login_url="/login/")
def report_item_update_form(request):
    rid = request.GET.get("id", False)
    ri = get_object_or_404(RI, id=rid)
    type = request.GET.get("selected", False)
    item_type = get_object_or_404(Report_Item_Type, id=int(type))
    form = RIF(instance=ri)
    context["form"] = form
    context["type_label"] = [int(type)]
    context["items"] = Report_Item_Type.objects.all()
    context["item_type"] = item_type
    context["attributes"] = Report_Item_Attribute.objects.filter(item=ri).order_by(
        "sequence"
    )
    context["ri"] = ri
    return render(request, "report_item_update_form.html", context)


def ri_attributes_update(ri, item_type):
    alist = []
    type_attributes = Report_Item_Attribute.objects.filter(
        item_type=item_type
    ).order_by("sequence")
    item_attributes = Report_Item_Attribute.objects.filter(item=ri).order_by("sequence")
    for attribute in item_attributes:
        for type_attribute in type_attributes:
            if attribute.title == type_attribute.title:
                alist.append(attribute.title)
                attribute.input_type = type_attribute.input_type
                attribute.sequence = type_attribute.sequence
                attribute.save()
    for attribute in item_attributes:
        if attribute.title not in alist and attribute.title != "Title":
            attribute.delete()
    for attribute in type_attributes:
        if attribute.title not in alist and attribute.title != "Title":
            attribute_add = Report_Item_Attribute.objects.create(
                item=ri,
                title=attribute.title,
                value=attribute.value,
                input_type=attribute.input_type,
            )
            attribute_add.save()
    return Report_Item_Attribute.objects.filter(item=ri).order_by("sequence")


@login_required(login_url="/login/")
def report_item_form(request):
    form = RIF()
    context["form"] = form
    context["items"] = Report_Item_Type.objects.all()
    return render(request, "report_item_form.html", context)


@login_required(login_url="/login/")
def update_report_item(request):
    title = request.POST.get("title", None)
    attr_names = request.POST.getlist("names[]")
    attr_values = request.POST.getlist("values[]")
    rid = request.POST.get("report_id", False)
    type_id = request.POST.get("type_id", False)
    form = RIF(request.POST)
    if form.is_valid():
        report_item = RI.objects.get(id=rid)
        report_item.title = title
        if type_id:
            report_item.item_type = get_object_or_404(Report_Item_Type, id=type_id)
        report_item.save()
        attributes = Report_Item_Attribute.objects.filter(item__id=rid).order_by(
            "sequence"
        )
        attr = Report_Item_Attribute.objects.get(item__id=rid, title="Title")
        attr.value = [title]
        attr.save()
        for attribute in attributes:
            for count in range(len(attr_names)):
                if attribute.title == attr_names[count]:
                    attribute.value = [attr_values[count]]
                    attribute.save()
                if attribute.input_type == "list":
                    static_attr = Static_Attribute.objects.get(title=attribute.title)
                    for val in static_attr.values:
                        if [val] == attribute.value:
                            attribute.selected = static_attr.values.index(val)
                            attribute.value = static_attr.values
                            attribute.save()
        return JR({"success": "success"})
    else:
        return JR({"errors": form.errors})


@login_required(login_url="/login/")
def report_items_filter(request):
    item_type = request.GET.get("item_type", "all")
    items_per_page = request.GET.get("items_per_page", 20)
    if request.GET.get("exact_match", False) == "true":
        exact_match = True
    else:
        exact_match = False
    search_string = request.GET.get("search_string", False)
    if item_type != "all":
        report_item = RI.objects.filter(item_type__title=item_type, newest=True)
    else:
        report_item = RI.objects.filter(newest=True)

    if exact_match:
        report_item = report_item.filter(
            (
                Q(title__contains=search_string)
                | Q(item_type__title__contains=search_string)
                | Q(contributor__first_name__contains=search_string)
                | Q(contributor__last_name__contains=search_string)
            )
        ).order_by("title")
    else:
        report_item = report_item.filter(
            (
                Q(title__icontains=search_string)
                | Q(item_type__title__icontains=search_string)
                | Q(contributor__first_name__icontains=search_string)
                | Q(contributor__last_name__icontains=search_string)
            )
        ).order_by("title")

    paginator = Paginator(report_item, items_per_page)
    page = request.GET.get("page")
    try:
        report_items = paginator.page(page)
    except PageNotAnInteger:
        report_items = paginator.page(1)
    except EmptyPage:
        report_items = paginator.page(paginator.num_pages)
    context["report_items"] = report_items
    return render(request, "display_report_items.html", context)


################################################################################
def report_export(request):
    from utils.tools import check_or_make_dir

    rid = request.POST.get("id", False)
    report = get_object_or_404(Report, id=rid)
    report.save()
    # refresh from db
    r = Report.objects.get(id=report.id)
    # report context
    rc = {}

    PATH_PREFIX = "media/"
    EXTENSION = ".docx"
    SLASH = "/"
    REPORT_CREATED = str(r.created)[:18]
    REPORT_UPDATED = str(r.updated)[:18]

    rc["title"] = str(r.title)
    rc["created"] = r.report_date
    rc["created_by"] = str(r.author)

    # structure report context
    for step in r.steps.all():
        for var in step.variables.all():
            if var.selectable:
                rc[var.template_var] = var.get_selected_items()
            else:
                rc[var.template_var] = var.content
    r.template_context = rc
    r.save()
    doc = DocxTemplate(r.wizard.template.path)

    doc.render(rc)

    DIR = settings.MEDIA_ROOT + "/reports"

    DOC_NAME = r.title + EXTENSION

    check_or_make_dir(DIR)

    doc.save(DIR + SLASH + DOC_NAME)
    rf = File(open(DIR + SLASH + DOC_NAME))

    a = Associated_File(
        filename=DOC_NAME,
        file=rf,
        guid=get_guid(),
        subdirectory="reports",
        a_i_guid=r.guid,
        uploader=request.user,
    )
    a.save()
    a.associated_item = r
    a.save()

    r.file_url = DIR + SLASH + DOC_NAME
    r.file_name = DOC_NAME
    r.save()
    return JR({"success": "success"})
    # r.report_file.save(DOC_NAME,DIR+SLASH+DOC_NAME, save=True)


def item_type_attrs(request):
    context = {}
    iid = request.GET.get("id", None)
    item_type = get_object_or_404(Report_Item_Type, id=iid)
    if request.GET.get("no_val", False):
        context["no_val"] = True
    if request.GET.get("form_val", False):
        context["form_val"] = True
    context["attributes"] = Report_Item_Attribute.objects.filter(
        item_type=item_type
    ).order_by("sequence")
    context["item_type"] = item_type
    return render(request, "type_attrs.html", context)


def item_type_add_attr(request):
    context = {}
    iid = request.POST.get("id", None)
    item_type = get_object_or_404(Report_Item_Type, id=iid)
    item_type_ri = RI.objects.filter(item_type=item_type)
    count = Report_Item_Attribute.objects.filter(item_type=item_type).count() + 1
    context["attributes"] = []
    context["attr"] = []
    if request.POST.get("no_val", False):
        context["no_val"] = True
    if request.POST.get("static", False):
        context["static"] = True
        static_attr_id = request.POST.get("staticAttrId", False)
        static_attr = get_object_or_404(Static_Attribute, id=static_attr_id)
        attr = Report_Item_Attribute.objects.create(
            title=static_attr.title,
            item_type=item_type,
            value=static_attr.values,
            input_type="list",
            sequence=count,
        )
        attr.save()
        context["staticAttr"] = static_attr
        context["item_type"] = item_type
        for report_item in item_type_ri:
            ri_attributes_update(report_item, item_type)
        context["attr"] = attr
        return render(request, "type_attr.html", context)
    else:
        context["static"] = False
        attr = Report_Item_Attribute.objects.create(
            title="new attribute", item_type=item_type, value=[""], sequence=count
        )

        attr.save()
        context["item_type"] = item_type
        for report_item in item_type_ri:
            ri_attributes_update(report_item, item_type)
        context["attr"] = attr
        return render(request, "type_attr.html", context)


def item_type_update_attr(request):
    iid = request.POST.get("id", None)
    item_type = Report_Item_Type.objects.get(id=iid)
    item_type_ri = RI.objects.filter(item_type=item_type)
    title = request.POST.get("text", False)
    input_type = request.POST.get("input_type", None)
    attr_id = request.POST.get("aid", None)
    attribute = Report_Item_Attribute.objects.get(id=attr_id)
    if title:
        attribute.title = title
        attribute.item_type = item_type
        attribute.save()
    elif input_type:
        attribute.input_type = input_type
        attribute.item_type = item_type
        attribute.save()
    else:
        return JR({"error": "no attr by that name"})
    for report_item in item_type_ri:
        ri_attributes_update(report_item, item_type)
    return JR({"success": "success"})


def item_type_delete(request):
    type_id = request.POST.get("id", None)
    item_type = get_object_or_404(Report_Item_Type, id=type_id)
    item_type.delete()
    return HRR("/ridb_manager/")


def ri_update_attr(request):
    rid = request.POST.get("id", None)
    ri = get_object_or_404(RI, id=rid)
    name = request.POST.get("name", False)
    value = request.POST.get("value", False)
    if name and value:
        ri.attrs[name] = value
        ri.save()
        return JR({"success": "success"})
    else:
        return JR({"error": "no name or value"})


def ridb_manager(request):
    context = {}
    context["no_val"] = True
    form = RIF()
    context["form"] = form
    context["items"] = Report_Item_Type.objects.all()
    context["item_type"] = Report_Item_Type.objects.all()
    return render(request, "ridb_manager_modal.html", context)


def type_attr_delete_check(request):
    context = {}
    context["id"] = request.GET.get("id", None)
    context["app"] = request.GET.get("app", None)
    context["model"] = request.GET.get("model", None)
    context["name"] = request.GET.get("name", None)
    return render(request, "type_attr_delete_check.html", context)


def type_attr_delete(request):
    aid = request.POST.get("aid", None)
    tid = request.POST.get("id", None)
    item_type = get_object_or_404(Report_Item_Type, id=tid)
    item_type_ri = RI.objects.filter(item_type=item_type)
    attr = get_object_or_404(Report_Item_Attribute, id=aid)
    attr.delete()
    for report_item in item_type_ri:
        ri_attributes_update(report_item, item_type)
    return JR({"success": "success"})


def type_attr_update(request):
    order = request.POST.getlist("order[]", False)
    tid = request.POST.get("id", None)
    item_type = get_object_or_404(Report_Item_Type, id=tid)
    attributes = Report_Item_Attribute.objects.filter(item_type=item_type)
    item_type_ri = RI.objects.filter(item_type=item_type)
    order = filter(None, order)
    if order:
        for attribute in attributes:
            for item in order:
                if attribute.title == item:
                    attribute.sequence = order.index(item) + 1
                    attribute.save()
    for report_item in item_type_ri:
        ri_attributes_update(report_item, item_type)
    return JR({"success": order})


def wizard_step_update(request):
    wid = request.POST.get("id", None)
    sequence = request.POST.get("seq", None)
    if sequence:
        step = get_object_or_404(Wizard_Step, id=wid)
        step.sequence = sequence
        step.save()
        return JR({"success": "success"})
    else:
        return JR({"error": "error"})


def report_variable_add(request):
    if request.method == "GET":
        context = {}
        form = RVF()
        context["form"] = form
        return render(request, "report_variable_add_form.html", context)
    else:
        display = request.POST.get("display", False)
        form = RVF(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            return JR(
                {"success": "/report_variable/%s" % (report.id), "sidenav": "reload"}
            )
        else:
            return JR({"errors": form.errors})


def delete_report_variable(request):
    delete_report_var = request.POST.get("id")
    entry = Report_Variable.objects.filter(id=delete_report_var)
    entry.delete()
    return HR("success")


def report_variable_edit(request):
    if request.method == "GET":
        rid = request.GET.get("id", False)
        entry = get_object_or_404(Report_Variable, id=rid)
        form = RVF(instance=entry)
        context["var_id"] = rid
        context["form"] = form
        return render(request, "report_var_edit_form.html", context)
    else:
        id = request.POST.get("id", None)
        display = request.POST.get("display", None)
        input_type = request.POST.get("input_type", False)
        limit = request.POST.get("limit", False)
        template = request.POST.get("template", False)
        form = RVF(request.POST)
        if form.is_valid():
            entry = get_object_or_404(Report_Variable, id=id)
            entry.display = display
            entry.input_type = input_type
            entry.limit = limit
            entry.template = template
            entry.save()
            return JR({"success": "/report_variable/%s" % (entry.id)})
        else:
            return JR({"errors": form.errors})


def report_variable_filter(request):
    get_context_items(context, request)
    input = request.GET.get("input_type", False)
    search_string = request.GET.get("search_string", "")
    nvar_per_page = request.GET.get("nvar_per_page", 20)
    if request.GET.get("exact_match", False) == "true":
        exact_match = True
    else:
        exact_match = False
    if exact_match:
        if input == "all":
            variable = Report_Variable.objects.filter(
                Q(display__contains=search_string)
                | Q(template__contains=search_string)
                | Q(limit__contains=search_string)
                | Q(input_type__contains=search_string)
            ).order_by("display")
        else:
            variable = Report_Variable.objects.filter(
                Q(input_type=input)
                & (
                    Q(display__contains=search_string)
                    | Q(template__contains=search_string)
                    | Q(limit__contains=search_string)
                    | Q(input_type__contains=search_string)
                )
            ).order_by("display")
    else:
        if input == "all":
            variable = Report_Variable.objects.filter(
                Q(display__icontains=search_string)
                | Q(template__icontains=search_string)
                | Q(limit__icontains=search_string)
                | Q(input_type__icontains=search_string)
            ).order_by("display")
        else:
            variable = Report_Variable.objects.filter(
                Q(input_type=input)
                & (
                    Q(display__icontains=search_string)
                    | Q(template__icontains=search_string)
                    | Q(limit__icontains=search_string)
                    | Q(input_type__icontains=search_string)
                )
            ).order_by("display")
    page = request.GET.get("page")
    paginator = Paginator(variable, nvar_per_page)
    try:
        variable_page = paginator.page(page)
    except PageNotAnInteger:
        variable_page = paginator.page(1)
    except EmptyPage:
        variable_page = paginator.page(paginator.num_pages)
    context["variable_page"] = variable_page
    return render(request, "display_report_variable.html", context)


def manage_static_attr(request):
    context = {}
    context["attrs"] = Static_Attribute.objects.all().order_by("title")
    return render(request, "manage_static_attr.html", context)


def static_attr_form(request):
    context = {}
    id = request.GET.get("id", None)
    if id:
        context["attr"] = get_object_or_404(Static_Attribute, id=id)
    return render(request, "static_attr_form.html", context)


def static_attr_add_item(request):
    return render(request, "static_attr_input_field.html")


def static_attr_save(request):
    id = request.POST.get("id", None)
    title = request.POST.get("title")
    values = request.POST.getlist("values[]", [])
    if not id:
        static_attr = Static_Attribute(title=title, values=values)
        static_attr.save()
    else:
        attr = get_object_or_404(Static_Attribute, id=id)
        attr.title = title
        attr.values = values
        attr.save()
    return HRR("/manage_static_attr/")


def static_attr_delete(request):
    id = request.POST.get("id", None)
    attr = get_object_or_404(Static_Attribute, id=id)
    attr.delete()
    return HRR("/manage_static_attr/")


def display_static_attrs(request):
    context = {}
    context["attrs"] = Static_Attribute.objects.all().order_by("title")
    return render(request, "display_static_attrs.html", context)
