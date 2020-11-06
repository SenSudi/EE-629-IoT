from django.core.files import File
from utils.imports import *

from models import *
from forms import *
from files.model_tools import save_new_afile

# Create your views here.
def project_tables(request):
    context = {}
    context["tables"] = DataTable.objects.all()
    context["where"] = "DataTables"
    return render(request, "project_tables.html", context)


def table_add_form(request):
    context = {}
    form = DataTableCreate()
    context["form"] = form
    context["action"] = "/table_add/"
    context["form_id"] = "dt_add_form"
    return render(request, "table_add_modal.html", context)


def table_add(request):
    if request.method == "POST":
        form = DataTableCreate(request.POST)
        if form.is_valid():
            table = form.save()
            table.guid = get_guid()
            return JR({"success": "success", "element": table.html})
        else:
            return JR({"errors": form.errors()})
    else:
        return HR("no")


def manager(request):
    context = {}
    form = DataItemCreate()
    context["form"] = form
    return render(request, "manager.html", context)


def data_type_add_form(request):
    context = {}
    form = DataTypeCreate()
    context["form"] = form
    context["form_id"] = "dt-create-form"
    context["action"] = "/data_type_add/"
    return render(request, "data_type_form.html", context)


def data_type_add(request):
    if request.method == "POST":
        form = DataTypeCreate(request.POST)
        if form.is_valid():
            dtype = form.save()
            dtype.guid = get_guid()
            dtype.save()
            data_type = DataType.objects.get(id=dtype.id)
            return JR(
                {
                    "success": "success",
                    "attrs": data_type.list_attributes,
                    "option": data_type.option,
                }
            )
        else:
            return JR({"errors": form.errors()})
    else:
        return HR("no")


def data_type_update_attr(request):
    did = request.POST.get("id", None)
    data_type = get_object_or_404(DataType, id=did)
    new = request.POST.get("text", False)
    old = request.POST.get("name", None)
    if new and old:
        data_type.attributes[new] = data_type.attributes.pop(old)
        data_type.save()
        return JR({"success": "success"})
    else:
        return JR({"error": "no attr by that name"})


def data_type_add_attr(request):
    context = {}
    did = request.POST.get("id", None)
    data_type = get_object_or_404(DataType, id=did)
    return HR(data_type.add_attribute(context=context))


def data_type_attrs(request):
    context = {}
    did = request.GET.get("id", None)
    data_type = get_object_or_404(DataType, id=did)
    return HR(data_type.list_attributes)


def data_import_form(request):
    context = {}
    form = DataItemImport()
    context["form"] = form
    context["action"] = "/data_item_import/"
    context["form_id"] = "dt_import_form"
    return render(request, "data_import_modal.html", context)


def data_item_import(request):
    if request.method == "POST":
        form = DataItemImport(request.POST)
        if form.is_valid():
            project = request.user.tester.project
            file = File(request.FILES["import_file"])
            save_new_afile(file, "projects/%s" % project.guid, project.guid)
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors()})
    else:
        return HR("no")
