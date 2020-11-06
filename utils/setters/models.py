from utils.imports import *

# Import Models
from utils.models import Label as L

# Import Forms
from utils.forms import RoleForm as RF

context = {}


@login_required(login_url="/login/")
def aprfap(request):
    """
	Add Person Role from Add New Project Form
	"""
    form = RF(request.POST)
    if form.is_valid():
        role = form.save(commit=False)
        role.project = True
        role.save()
    return HRR("/p_gprf/")
