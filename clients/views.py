from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect as HRR
from project.views import get_context_items
from models import Client

from forms import ClientForm as CF

context = {}

# Create your views here.
@login_required(login_url="/login/")
def clients_db(request):
    user = request.user
    # only method, admin, hv admin can access
    # if grant_access(user, 'client_admin', True):
    # 	return PERM_ERROR
    get_context_items(context, request)
    context["section"] = "Clients DB"
    clients = Client.objects.all()
    context["clients"] = clients
    form = CF()
    context["form"] = form
    context["item_header"] = True
    context["item_body"] = True
    context["page_controls"] = True
    context["item_name"] = "Client"
    context["add_script"] = "cldbClientAdd(this)"
    return render(request, "clients_db.html", context)


@login_required(login_url="/login/")
def display_clients(request):
    context["items"] = Client.objects.all()
    context["item_header"] = True
    context["item_body"] = True
    return render(request, "display_clients.html", context)


@login_required(login_url="/login/")
def add_client(request):
    if request.method == "POST":
        form = CF(request.POST)
        if form.is_valid():
            form.save()
    return HRR("/display_clients/")


@login_required(login_url="/login/")
def client_details(request):
    client_id = request.GET.get("item-id", False)
    client = Client.objects.get(id=client_id)
    context["client"] = client
    return render(request, "client_details.html", context)


@login_required(login_url="/login/")
def client_update_form(request):
    client_id = request.GET.get("id", False)
    client = get_object_or_404(Client, id=client_id)
    form = CF(instance=client)
    context["id"] = client_id
    context["client"] = client
    context["form"] = form
    return render(request, "client_update_form.html", context)


@login_required(login_url="/login/")
def client_update(request):
    client_id = request.POST.get("id", False)
    client = get_object_or_404(Client, id=client_id)
    form = CF(request.POST, instance=client)
    if form.is_valid():
        form.save()
    return HRR("/display_clients/")
