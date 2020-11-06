from utils.imports import *
from project.views import get_context_items

from project.setters.models import new_vip

from forms import ContactForm as CF
from forms import ContactOnlyForm as COF
from forms import ContactUpdateForm as CUF
from forms import DBContactForm as DBCF

from models import Contact

from clients.models import Client

# Create your views here.
################################################################################
@login_required(login_url="/login/")
def contact_delete(request):
    cid = request.POST.get("id", False)
    contact = get_object_or_404(Contact, id=cid)
    contact.delete()
    return JR({"success": "contact deleted"})


################################################################################
@login_required(login_url="/login/")
def contacts(request):
    get_context_items(context, request)
    project = request.user.tester.project
    context["section"] = "Contacts"
    context["contacts"] = project.get_contacts().order_by("first_name")
    context["where"] = "/contacts/"
    return render(request, "project_contacts.html", context)


################################################################################
@login_required(login_url="/login/")
def contact_add_form(request):
    form = COF()
    context["form"] = form
    context["submit_text"] = "submit"
    context["action"] = "/contact_add/"
    context["form_id"] = "form-contact-add"
    context["object_type"] = "contact"
    return render(request, "contact_add_modal.html", context)


################################################################################
@login_required(login_url="/login/")
def contact_add(request):
    project = request.user.tester.project
    form = COF(request.POST)
    if form.is_valid():
        updated = form.save()
        updated.project.add(project)
        project.client.contacts.add(updated)
        for rid in request.POST.getlist("roles", []):
            vip = new_vip(updated, rid)
            project.vips.add(vip)
        return JR({"success": OBJECT_FORM_SUCCESS})
    else:
        return JR({"errors": form.errors})


################################################################################
@login_required(login_url="/login/")
def contact_details(request):
    project = request.user.tester.project
    cid = request.GET.get("id", False)
    contact = get_object_or_404(Contact, id=cid)
    ctype = ContentType.objects.get(app_label="contacts", model="contact")
    contact.current_roles = list(project.vips.filter(object_id=cid, content_type=ctype))
    context["contact"] = contact
    return render(request, "contact_details.html", context)


################################################################################
@login_required(login_url="/login/")
def contact_update_form(request):
    cid = request.GET.get("id", False)
    contact = get_object_or_404(Contact, id=cid)
    form = CUF(instance=contact)
    context["form"] = form
    context["contact"] = contact
    context["submit_text"] = "update"
    context["action"] = "/contact_update/"
    context["form_id"] = "form-contact-update"
    context["object_type"] = "contact"
    return render(request, "contact_update_modal.html", context)


################################################################################
@login_required(login_url="/login/")
def contact_update(request):
    project = request.user.tester.project
    cid = request.POST.get("id", False)
    contact = get_object_or_404(Contact, id=cid)
    rids = contact.get_role_ids()
    form = CUF(request.POST, instance=contact)
    if form.is_valid():
        updated = form.save()
        for rid in request.POST.getlist("roles", []):
            if int(rid) not in rids:
                vip = new_vip(updated, rid)
                project.vips.add(vip)
        return JR({"success": OBJECT_FORM_SUCCESS, "updated": updated.get_role_ids()})
    else:
        return JR({"errors": form.errors})


################################################################################
@login_required(login_url="/login/")
def display_contacts(request):
    if request.GET.get("where", "") == "/contacts/":
        project = request.user.tester.project
        context["contacts"] = project.get_contacts().order_by("first_name")
        return render(request, "display_project_contacts.html", context)

    elif request.GET.get("where", "") == "/contacts_db/":
        context["clients"] = Client.objects.all().order_by("-name")
        context["contacts"] = Contact.objects.all().order_by("client")
        return render(request, "db_display_contacts.html", context)
    else:
        return HR("Not Authorized")


################################################################################
@login_required(login_url="/login/")
def add_contact(request):
    if request.method == "POST":
        form = CF(request.POST)
        if form.is_valid():
            contact = form.save()
            # contact.project.add(request.user.tester.project)
            client_id = request.POST.get("client", False)
            if client_id:
                client = Client.objects.get(id=client_id)
                client.contacts.add(contact)
                client.save()
        return HRR("/display_contacts/")


################################################################################
@login_required(login_url="/login/")
def update_contact(request):
    if request.method == "POST":
        model_type = request.POST.get("model_type", False)
        model_id = request.POST.get("model_id", False)
        app = request.POST.get("app", False)
        if model_type and model_id and app:
            instance = getattr(
                sys.modules["%s.models" % app], "%s" % model_type
            ).objects.get(id=model_id)
        form = CF(request.POST, instance=instance)
        if form.is_valid():
            contact = form.save()
            client_id = request.POST.get("client", False)
            if client_id:
                client = Client.objects.get(id=client_id)
                contact.client_set.clear()
                contact.client_set.add(client)
            return HRR("/display_contacts/")
    else:
        return HR("Not Authorized")


################################################################################
@login_required(login_url="/login/")
def contacts_db(request):
    user = request.user
    # only method, admin, hv admin can access
    # if grant_access(user, 'contact_admin', True):
    # 	return PERM_ERROR
    get_context_items(context, request)
    context["section"] = "Contacts DB"
    # context['page_controls'] 	= True
    # context['item_name'] 		= 'Contact'
    # context['add_script'] 		= 'codbContactAdd(this)'
    context["clients"] = Client.objects.all().order_by("-name")
    context["contacts"] = Contact.objects.all().order_by("client")
    context["where"] = "/contacts_db/"
    return render(request, "contacts_db.html", context)


################################################################################
@login_required(login_url="/login/")
def db_contact_add_form(request):
    form = DBCF()
    context["form"] = form
    context["submit_text"] = "submit"
    context["action"] = "/db_contact_add/"
    context["form_id"] = "form-contact-add"
    context["object_type"] = "contact"
    return render(request, "db_contact_add_modal.html", context)


################################################################################
@login_required(login_url="/login/")
def db_contact_add(request):
    cid = request.POST.get("client", False)
    client = get_object_or_404(Client, id=cid)
    form = DBCF(request.POST)
    if form.is_valid():
        contact = form.save()
        client.contacts.add(contact)
        return JR({"success": OBJECT_FORM_SUCCESS})
    else:
        return JR({"errors": form.errors})


################################################################################
@login_required(login_url="/login/")
def contact_db_details(request):
    contact_id = request.GET.get("contact-id", False)
    contact = Contact.objects.get(id=contact_id)
    context["contact"] = contact
    return render(request, "contact_db_details.html", context)


################################################################################
# Add Contact From New Project Form
@login_required(login_url="/login/")
def acfnpf(request):
    if request.method == "POST":
        form = COF(request.POST)
        if form.is_valid():
            contact = form.save()
            c_id = request.POST.get("c_id", False)
            if c_id:
                client = Client.objects.get(id=c_id)
                client.contacts.add(contact)
        return HRR("/p_gpcfi/?model_id=%s" % client.id)


################################################################################
