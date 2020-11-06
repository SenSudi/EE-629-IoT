from django.utils import timezone
from tasks.models import Task

from utils.tools import get_guid

def create_project_tasks(method_list,project):
	task_list 		= []
	for item in method_list:
		# Instantiate task items.
		new_task 				= Task()
		if item:
			new_task.meth_item 	= item
		else:
			new_task.meth_item 	= None
		new_task.status 		= 'open' 
		new_task.phase 			= project.phase_set.get(parent_guid=item.phase.guid)
		new_task.tier			= item.tier
		new_task.parent_guid	= item.guid
		new_task.lineage_guid	= item.lineage_guid
		new_task.project 		= project
		new_task.help_base		= item.help_base
		new_task.title 			= item.title
		new_task.est_time		= item.est_time
		new_task.description    = item.description
		new_task.sequence		= item.sequence
		new_task.tsk_duration	= 0
		new_task.tsk_start		= timezone.now()
		new_task.tsk_end		= timezone.now()
		new_task.base_command	= item.command
		new_task.exec_cmd		= 'sample exec cmd'
		new_task.exec_duration	= '0:00:01'
		new_task.guid 			= get_guid()
		new_task.save()
		item.children.add(new_task)
		for file in item.files.all():
			file.associated_item = new_task
			file.save()
		task_list.append(new_task)
	return task_list