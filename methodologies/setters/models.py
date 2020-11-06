from methodologies.models import Phase
from utils.tools import get_guid

def project_phase_from_method_phase(phase,project):
	new_phase 				= Phase()
	new_phase.guid 			= get_guid()
	new_phase.title 		= phase.title
	new_phase.sequence 		= phase.sequence
	new_phase.project 		= project
	new_phase.version 		= phase.version
	new_phase.parent_guid 	= phase.guid
	new_phase.lineage_guid  = phase.lineage_guid
	new_phase.save()
	return new_phase

def instantiate_project_phases(project):
	for phase in project.project_type.phase.all():
		project_phase_from_method_phase(phase,project)