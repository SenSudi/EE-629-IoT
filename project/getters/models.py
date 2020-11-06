from django.db.models import Q

from methodologies.models import Phase


def get_project_phases(project):
    """
	Returns a queryset of the phases for a given project
	"""
    ptype = project.project_type
    queryset = Phase.objects.filter(Q(project_type=ptype) | Q(project=project))
    return queryset
