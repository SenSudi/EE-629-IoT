from methodologies.models import Method
from methodologies.models import Phase
from models import Task

from utils.tools import get_guid
from methodologies.setters.models import project_phase_from_method_phase


def task_to_method(task):
    method = Method()
    method.title = task.title
    method.tier = task.tier
    method.sequence = task.sequence
    method.command = task.base_command
    method.description = task.description
    method.mangle = task.mangle
    method.help_base = task.help_base
    method.est_time = task.est_time
    method.new_guid = get_guid()
    method.lineage_guid = task.lineage_guid
    method.save()
    method.children.add(task)
    return method


def task_from_method(method, project):
    task = Task()
    task.title = method.title
    task.tier = method.tier
    task.sequence = method.sequence
    task.base_command = method.command
    task.description = method.description
    task.mangle = method.mangle
    task.help_base = method.help_base
    task.est_time = method.est_time
    task.lineage_guid = method.lineage_guid
    task.parent_guid = method.guid
    task.meth_item = method
    task.project = project
    phase = project.get_phase(method.phase.lineage_guid)
    if phase is None:
        phase = project_phase_from_method_phase(method.phase, project)
    task.phase = phase
    task.guid = get_guid()
    task.save()

    return task
