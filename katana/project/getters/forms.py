from utils.imports import *

# Form Imports
from project.forms import ProjectRoleForm as PRF
from utils.forms import RoleForm as RF
from utils.forms import RoleSelectForm as RSF
from project.forms import ProjectVIPForm as PVF

context = {}


@login_required(login_url="/login/")
def get_ProjectRoleForm(request):
    context["form"] = PRF()
    return render(request, "form_project_role.html", context)


@login_required(login_url="/login/")
def gpcfi(request):
    """
	verbose name: get_Project(contact)RoleForm_instance
		using the same RoleForm we return only the contact portion
	"""
    try:
        manager = getattr(sys.modules["clients.models"], "Client")
    except:
        from clients.models import Client

        manager = Client
    model_id = request.GET.get("model_id", None)
    instance = get_object_or_404(manager, id=model_id)
    context["form"] = PRF(instance=instance)
    return render(request, "form_project_role_contact.html", context)


@login_required(login_url="/login/")
def gprf(request):
    """
	verbose name: get_ProjectRoleForm
		using the same RoleForm we return only the role portion
	"""
    form = RSF()
    context["form"] = form
    return render(request, "form_project_role.html", context)


@login_required(login_url="/login/")
def gprfm(request):
    """
	verbose name: get_ProjectRoleForm
		using the same RoleForm we return only the role portion
	"""
    return render(request, "form_project_role_misc.html", context)


# @login_required(login_url='/login/')
# def gpvipf(request):
# 	'''
# 	verbose name: get project vip form
# 		give it an instance of the project to use as the query string
# 	'''
# 	instance =
# 	form = PFV()
