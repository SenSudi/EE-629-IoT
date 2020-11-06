"""hv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from auditor import views as auditor
from clients import views as clients

from issuetracker import views as it
from issuetracker import issue_views as issue
from issuetracker import status_views as status

from project import views as proj
from project.getters import forms as p_g_f
from project.setters import models as p_s_m

from methodologies import views as methods
from notes import views as notes
from contacts import views as contacts
from reports import views as reports
from utils import views as utils
from utils.setters import models as u_s_m
from users import views as users
from tasks import views as tasks
from timetracker import views as tt
from files import views as files

from datatables import views as dt

urlpatterns = [
    # Auditor
    url(r"^get_audits/", auditor.get_audits, name="get_audits"),
    # Clients
    url(r"^clients_db/", clients.clients_db, name="clients_db"),
    url(r"^add_client/", clients.add_client, name="add_client"),
    url(r"^display_clients/", clients.display_clients, name="display_clients"),
    url(r"^client_details/", clients.client_details, name="client_details"),
    url(r"^client_update_form/", clients.client_update_form, name="client_update_form"),
    url(r"^client_update/", clients.client_update, name="client_update"),
    # Contacts
    url(r"^contacts/", contacts.contacts, name="contacts"),
    url(r"^contact_add_form/", contacts.contact_add_form, name="contact_add_form"),
    url(r"^contact_add/", contacts.contact_add, name="contact_add"),
    url(r"^contact_delete/", contacts.contact_delete, name="contact_delete"),
    url(
        r"^contact_update_form/",
        contacts.contact_update_form,
        name="contact_update_form",
    ),
    url(r"^contact_update/", contacts.contact_update, name="contact_update"),
    # ------------------------------------------------------------------------------------
    url(r"^contacts_db/", contacts.contacts_db, name="contacts_db"),
    url(r"^display_contacts/", contacts.display_contacts, name="display_contacts"),
    url(r"^add_contact/", contacts.add_contact, name="add_contact"),
    url(r"^update_contact/", contacts.update_contact, name="update_contact"),
    url(
        r"^contact_db_details/", contacts.contact_db_details, name="contact_db_details"
    ),
    url(r"^acfnpf/", contacts.acfnpf, name="acfnpf"),
    url(r"^contact_details/", contacts.contact_details, name="contact_details"),
    url(
        r"^db_contact_add_form/",
        contacts.db_contact_add_form,
        name="db_contact_add_form",
    ),
    url(r"^db_contact_add/", contacts.db_contact_add, name="db_contact_add"),
    #############################################################################################
    # DataTables #
    ##############
    url(r"^project_tables/", dt.project_tables, name="project_tables"),
    url(r"^table_add_form/", dt.table_add_form, name="table_add_form"),
    url(r"^table_add/", dt.table_add, name="table_add"),
    url(r"^dt_manager/", dt.manager, name="dt_manager"),
    url(r"^data_type_add_form/", dt.data_type_add_form, name="data_type_add_form"),
    url(r"^data_type_add/", dt.data_type_add, name="data_type_add"),
    url(
        r"^data_type_update_attr/",
        dt.data_type_update_attr,
        name="data_type_update_attr",
    ),
    url(r"^data_type_add_attr/", dt.data_type_add_attr, name="data_type_add_attr"),
    url(r"^data_type_attrs/", dt.data_type_attrs, name="data_type_attrs"),
    url(r"^data_import_form/", dt.data_import_form, name="data_import_form"),
    url(r"^data_item_import/", dt.data_item_import, name="data_item_import"),
    #############################################################################################
    # Files #
    #########
    url(
        r"^display_project_files/",
        files.display_project_files,
        name="display_project_files",
    ),
    url(r"^files_list/", files.files_list, name="files_list"),
    url(r"^file_delete/", files.file_delete, name="file_delete"),
    url(r"^afile_form/", files.afile_form, name="afile_form"),
    url(r"^both_files_form/", files.both_files_form, name="both_files_form"),
    url(r"^upload_both_files/", files.upload_both_files, name="upload_both_files"),
    url(r"^get_files_list/", files.get_files_list, name="get_files_list"),
    #############################################################################################
    # IssueTracker #
    ################
    url(r"^issue_tracker/", it.issue_tracker, name="issue_tracker"),
    # --------------------------------------------------------------------------------------------
    url(
        r"^display_tracked_issues/",
        issue.display_tracked_issues,
        name="display_tracked_issues",
    ),
    url(r"^it_issue_details/", issue.it_issue_details, name="it_issue_details"),
    url(r"^it_issue_add_form/", issue.it_issue_add_form, name="it_issue_add_form"),
    url(r"^it_issue_add/", issue.it_issue_add, name="it_issue_add"),
    url(
        r"^it_issue_update_form/",
        issue.it_issue_update_form,
        name="it_issue_update_form",
    ),
    url(r"^it_issue_update/", issue.it_issue_update, name="it_issue_update"),
    # --------------------------------------------------------------------------------------------
    url(r"^it_status_add_form/", status.it_status_add_form, name="it_status_add_form"),
    url(r"^it_status_add/", status.it_status_add, name="it_status_add"),
    url(r"^it_status_add_form/", status.it_status_add_form, name="it_status_add_form"),
    url(r"^it_status_edit/", status.it_status_edit, name="it_status_edit"),
    url(r"^it_status_delete/", status.it_status_delete, name="it_status_delete"),
    url(r"^it_status_manage/", status.it_status_manage, name="it_status_manage"),
    url(
        r"^status_select_field/", status.status_select_field, name="status_select_field"
    ),
    url(r"^display_statuses/", status.display_statuses, name="display_statuses"),
    url(r"^status_new_obj/", status.status_new_obj, name="status_new_obj"),
    #############################################################################################
    # Methods #
    ###########
    url(r"^method/", methods.method, name="method"),
    url(r"^methodologies/", methods.methodologies, name="methodologies"),
    url(r"^method_data_tree/", methods.method_data_tree, name="method_data_tree"),
    url(r"^method_details/", methods.method_details, name="method_details"),
    url(r"^method_update", methods.method_update, name="method_update"),
    url(r"^get_method_form/", methods.get_method_form, name="get_method_form"),
    url(
        r"^method_reorder_update",
        methods.method_reorder_update,
        name="method_reorder_update",
    ),
    url(r"^db_manage_methods", methods.db_manage_methods, name="db_manage_methods"),
    url(r"^method_delete/", methods.method_delete, name="method_delete"),
    url(r"^method_remove/", methods.method_remove, name="method_remove"),
    #############################################################################################
    url(r"^add_phase/", methods.add_phase, name="add_phase"),
    url(r"^get_phases/", methods.get_phases, name="get_phases"),
    url(r"^phase_details/", methods.phase_details, name="phase_details"),
    url(r"^phase_update", methods.phase_update, name="phase_update"),
    url(r"^display_phases/", methods.display_phases, name="display_phases"),
    url(
        r"^add_phase_to_project/",
        methods.add_phase_to_project,
        name="add_phase_to_projects",
    ),
    url(
        r"^get_phase_total_time/",
        methods.get_phase_total_time,
        name="get_phase_total_time",
    ),
    url(r"^phase_edit_form/", methods.phase_edit_form, name="phase_edit_form"),
    url(r"^suggest_phase/", methods.suggest_phase, name="suggest_phase"),
    url(r"^db_manage_phases", methods.db_manage_phases, name="db_manage_phases"),
    url(r"^phase_delete/", methods.phase_delete, name="phase_delete"),
    url(r"^phase_remove/", methods.phase_remove, name="phase_remove"),
    #############################################################################################
    url(r"^add_ptype/", methods.add_ptype, name="add_ptype"),
    url(r"^get_ptypes/", methods.get_ptypes, name="get_ptypes"),
    url(r"^ptype_details/", methods.ptype_details, name="ptype_details"),
    url(r"^ptype_update", methods.ptype_update, name="ptype_update"),
    url(
        r"^ptype_reorder_update",
        methods.ptype_reorder_update,
        name="ptype_reorder_update",
    ),
    url(r"^project_type_remove/", methods.project_type_remove, name="project_type_remove"),
    #############################################################################################
    url(r"^db_ptype_add_form/", methods.db_ptype_add_form, name="db_ptype_add_form"),
    url(r"^db_ptype_edit_form/", methods.db_ptype_edit_form, name="db_ptype_edit_form"),
    url(r"^db_ptype_add/", methods.db_ptype_add, name="db_ptype_add"),
    url(r"^db_ptype_details/", methods.db_ptype_details, name="db_ptype_details"),
    url(r"^db_ptype_update/", methods.db_ptype_update, name="db_ptype_update"),
    url(r"^db_phase_add_form/", methods.db_phase_add_form, name="db_phase_add_form"),
    url(r"^db_phase_edit_form/", methods.db_phase_edit_form, name="db_phase_edit_form"),
    url(r"^db_phase_add/", methods.db_phase_add, name="db_phase_add"),
    url(r"^db_phase_update/", methods.db_phase_update, name="db_phase_update"),
    url(r"^db_phase_details/", methods.db_phase_details, name="db_phase_details"),
    url(r"^db_phase_decline/", methods.db_phase_decline, name="db_phase_decline"),
    url(r"^db_phase_approve/", methods.db_phase_approve, name="db_phase_approve"),
    url(r"^db_method_add_form/", methods.db_method_add_form, name="db_method_add_form"),
    url(r"^db_method_add/", methods.db_method_add, name="db_method_add"),
    url(r"^db_method_details/", methods.db_method_details, name="db_method_details"),
    url(
        r"^db_method_edit_form/",
        methods.db_method_edit_form,
        name="db_method_edit_form",
    ),
    url(r"^db_method_update/", methods.db_method_update, name="db_method_update"),
    url(r"^db_method_decline/", methods.db_method_decline, name="db_method_decline"),
    url(r"^db_method_approve/", methods.db_method_approve, name="db_method_approve"),
    url(r"^db_method_deploy/", methods.db_method_deploy, name="db_method_deploy"),
    url(
        r"^db_get_phases_for_ptypes/",
        methods.db_get_phases_for_ptypes,
        name="db_get_phases_for_ptypes",
    ),
    url(
        r"^export_project_type/",
        methods.export_project_type,
        name="export_project_type",
    ),
    url(
        r"^import_project_type/",
        methods.import_project_type,
        name="import_project_type",
    ),
    url(r"^import_pt_form/", methods.import_pt_form, name="import_pt_form"),
    #############################################################################################
    # Notes #
    #########
    url(r"^get_note_form", notes.get_note_form, name="get_note_form"),
    url(r"^get_notes_list", notes.get_notes_list, name="get_notes_list"),
    url(r"^add_note/", notes.add_note, name="add_note"),
    url(r"^note_info/", notes.note_info, name="note_info"),
    url(r"^update_note/", notes.update_note, name="update_note"),
    url(r"^project_notes/", notes.project_notes, name="project_notes"),
    # -------------------------------------------------------------------------
    url(r"^note_add_form/", notes.note_add_form, name="note_add_form"),
    url(r"^note_add/", notes.note_add, name="note_add"),
    url(r"^note_edit_form/", notes.note_edit_form, name="note_edit_form"),
    url(r"^note_edit/", notes.note_edit, name="note_edit"),
    # -------------------------------------------------------------------------
    url(r"^scratch_pad/", notes.scratch_pad, name="scratch_pad"),
    url(r"^scratchpad/", notes.scratchpad, name="scratchpad"),
    url(r"^scratchpad_update/", notes.scratchpad_update, name="scratchpad_update"),
    # --------------------------------------------------------------------------
    url(r"^narrative/", notes.narrative, name="narrative"),
    #############################################################################################
    # Project #
    ###########
    url(r"^projects/(?P<uid>.*)/(?P<info>.*)", proj.project),
    url(r"^new_project/", proj.new_project, name="new_project"),
    url(r"^add_project/", proj.add_project, name="add_project"),
    url(r"^projects_db/", proj.projects_db, name="projects_db"),
    url(r"^project_status", proj.project_status, name="project_status"),
    url(r"^project_files/", proj.project_files, name="project_files"),
    # Getters
    url(r"^p_gpcfi/", p_g_f.gpcfi, name="p_gpcfi"),
    url(r"^p_gprf/", p_g_f.gprf, name="p_gprf"),
    url(r"^p_gprfm/", p_g_f.gprfm, name="p_gprfm"),
    # Setters
    url(r"^p_spvip/", p_s_m.new_vip_f_npf, name="p_spvip"),
    url(r"^display_milestones", proj.display_milestones, name="display_milestones"),
    url(r"^milestone_add", proj.milestone_add, name="milestone_add"),
    url(r"^milestone_delete/", proj.milestone_delete, name="milestone_delete"),
    url(r"^milestone_state/", proj.milestone_state, name="milestone_state"),
    url(r"^ms_filter_submit/", proj.ms_filter_submit, name="ms_filter_submit"),
    url(r"^ms_filter_clear/", proj.ms_filter_clear, name="ms_filter_clear"),
    url(r"^ms_sort/", proj.ms_sort, name="ms_sort"),
    url(r"^home_milestones/", proj.home_milestones, name="home_milestones"),
    url(r"^get_milestone_tasks", proj.get_milestone_tasks, name="get_milestone_tasks"),
    url(r"^projects_dropdown/", proj.projects_dropdown, name="projects_dropdown"),
    # ------------------------------------------------------------------------------------
    url(
        r"^open_projects_checklist/",
        proj.open_projects_checklist,
        name="open_projects_checklist",
    ),
    #############################################################################################
    # Reports #
    ###########
    url(r"^template_manager/", reports.template_manager, name="template_manager"),
    url(
        r"^wizard_template_modal/",
        reports.wizard_template_modal,
        name="wizard_template_modal",
    ),
    url(
        r"^wizard_template_create/",
        reports.wizard_template_create,
        name="wizard_template_create",
    ),
    url(
        r"^wizard_template_edit/",
        reports.wizard_template_edit,
        name="wizard_template_edit",
    ),
    url(
        r"^wizard_modal_step_content/",
        reports.wizard_modal_step_content,
        name="wizard_modal_step_content",
    ),
    url(
        r"^wizard_template_step_add/",
        reports.wizard_template_step_add,
        name="wizard_template_step_add",
    ),
    url(r"^db_display_wizards/", reports.db_display_wizards, name="db_display_wizards"),
    url(
        r"^wizard_template_deploy/",
        reports.wizard_template_deploy,
        name="wizard_template_deploy",
    ),
    url(
        r"^db_wt_variable_list/",
        reports.db_wt_variable_list,
        name="db_wt_variable_list",
    ),
    url(
        r"^db_wt_variable_search/",
        reports.db_wt_variable_search,
        name="db_wt_variable_search",
    ),
    url(
        r"^db_wizard_step_var_add/",
        reports.db_wizard_step_var_add,
        name="db_wizard_step_var_add",
    ),
    url(
        r"^wizard_step_var_remove/",
        reports.wizard_step_var_remove,
        name="wizard_step_var_remove",
    ),
    url(
        r"^wizard_vriable_edit/",
        reports.wizard_vriable_edit,
        name="wizard_vriable_edit",
    ),
    url(
        r"^wizard_template_file_add/",
        reports.wizard_template_file_add,
        name="wizard_template_file_add",
    ),
    url(r"^wizard_step_update/", reports.wizard_step_update, name="wizard_step_update"),
    url(r"^report_items/", reports.report_items, name="report_items"),
    url(
        r"^report_items_filter/",
        reports.report_items_filter,
        name="report_items_filter",
    ),
    url(r"^report_items_add/", reports.report_items_add, name="report_items_add"),
    url(r"^report_variable/", reports.report_variable, name="report_variable"),
    url(
        r"^report_variable_add/",
        reports.report_variable_add,
        name="report_variable_add",
    ),
    url(
        r"^report_variable_filter/",
        reports.report_variable_filter,
        name="report_variable_filter",
    ),
    url(r"^update_report_item/", reports.update_report_item, name="update_report_item"),
    url(
        r"^display_report_items/",
        reports.display_report_items,
        name="display_report_items",
    ),
    url(r"^create_item_type/", reports.create_item_type, name="create_item_type"),
    url(
        r"^delete_report_variable/",
        reports.delete_report_variable,
        name="delete_report_variable",
    ),
    url(
        r"^report_item_update_form/",
        reports.report_item_update_form,
        name="report_item_update_form",
    ),
    url(r"^report_item_form/", reports.report_item_form, name="report_item_form"),
    url(
        r"^display_report_files/",
        reports.display_report_files,
        name="display_reports_files",
    ),
    url(r"^report_wizard/", reports.report_wizard, name="report_wizard"),
    url(r"^report_add_form/", reports.report_add_form, name="report_add_form"),
    url(r"^report_add/", reports.report_add, name="report_add"),
    url(r"^display_reports/", reports.display_reports, name="display_reports"),
    url(
        r"^report_wizard_details/",
        reports.report_wizard_details,
        name="report_wizard_details",
    ),
    url(
        r"^report_wizard_content/",
        reports.report_wizard_content,
        name="report_wizard_content",
    ),
    url(
        r"^report_wizard_update/",
        reports.report_wizard_update,
        name="report_wizard_update",
    ),
    url(
        r"^report_wizard_update_step_modified/",
        reports.report_wizard_update_step_modified,
        name="report_wizard_update_step_modified",
    ),
    url(r"^report_delete/", reports.report_delete, name="report_delete"),
    url(r"^report_export/", reports.report_export, name="report_export"),
    url(
        r"^wizard_var_item_add/",
        reports.wizard_var_item_add,
        name="wizard_var_item_add",
    ),
    url(
        r"^wizard_var_item_submit/",
        reports.wizard_var_item_submit,
        name="wizard_var_item_submit",
    ),
    url(r"^delete_report_file/", reports.delete_report_file, name="delete_report_file"),
    url(r"^item_type_attrs/", reports.item_type_attrs, name="item_type_attrs"),
    url(r"^item_type_add_attr/", reports.item_type_add_attr, name="item_type_add_attr"),
    url(r"^item_type_delete/", reports.item_type_delete, name="item_type_delete"),
    url(
        r"^item_type_update_attr/",
        reports.item_type_update_attr,
        name="item_type_update_attr",
    ),
    url(
        r"^report_variable_edit/",
        reports.report_variable_edit,
        name="report_variable_edit",
    ),
    url(r"^ri_update_attr/", reports.ri_update_attr, name="ri_update_attr"),
    url(r"^ridb_manager/", reports.ridb_manager, name="ridb_manager"),
    url(
        r"^type_attr_delete_check/",
        reports.type_attr_delete_check,
        name="type_attr_delete_check",
    ),
    url(r"^type_attr_delete/", reports.type_attr_delete, name="type_attr_delete"),
    url(r"^type_attr_update/", reports.type_attr_update, name="type_attr_update"),
    url(r"^manage_static_attr/", reports.manage_static_attr, name="manage_static_attr"),
    url(r"^static_attr_form/", reports.static_attr_form, name="static_attr_form"),
    url(
        r"^static_attr_add_item",
        reports.static_attr_add_item,
        name="static_attr_add_item",
    ),
    url(r"^static_attr_save", reports.static_attr_save, name="static_attr_save"),
    url(r"^static_attr_delete", reports.static_attr_delete, name="static_attr_delete"),
    url(
        r"^display_static_attrs",
        reports.display_static_attrs,
        name="display_static_attrs",
    ),
    #############################################################################################
    # Tasks
    url(r"^new_task/", tasks.new_task, name="new_task"),
    url(r"^task_state/", tasks.task_state, name="task_state"),
    url(r"^task_vars/", tasks.task_vars, name="task_vars"),
    url(r"^task_update/", tasks.task_update, name="task_update"),
    url(r"^task_file_upload", tasks.task_file_upload, name="task_file_upload"),
    url(r"^workflow/", tasks.workflow, name="workflow"),
    url(r"^task_info/", tasks.task_info, name="task_info"),
    url(r"^display_tasks/", tasks.display_tasks, name="display_tasks"),
    url(r"^task_details/", tasks.task_details, name="task_details"),
    url(r"^task_total_time/", tasks.task_total_time, name="task_total_time"),
    url(r"^get_task_notes/", tasks.get_task_notes, name="get_task_notes"),
    url(r"^task_files_select/", tasks.task_files_select, name="task_files_select"),
    url(r"^task_delete/", tasks.task_delete, name="task_delete"),
    # -----------------------------------------------------------------------------
    url(r"^wf_task_add_form/", tasks.wf_task_add_form, name="wf_task_add_form"),
    url(r"^wf_task_add/", tasks.wf_task_add, name="wf_task_add"),
    url(r"^wf_task_edit_form/", tasks.wf_task_edit_form, name="wf_task_edit_form"),
    url(r"^wf_task_update/", tasks.wf_task_update, name="wf_task_update"),
    url(r"^wf_task_suggest/", tasks.wf_task_suggest, name="wf_task_suggest"),
    url(
        r"^wf_task_files_modal/", tasks.wf_task_files_modal, name="wf_task_files_modal"
    ),
    url(r"^wf_task_file_add/", tasks.wf_task_file_add, name="wf_task_file_add"),
    # url(r'^wf_task_time_add/',   tasks.wf_task_time_add,   name='wf_task_time_add'),
    url(r"^wf_reload_phases/", tasks.wf_reload_phases, name="wf_reload_phases"),
    url(r"^wf_task_files_list/", tasks.wf_task_files_list, name="wf_task_files_list"),
    url(r"^wf_task_notes_list/", tasks.wf_task_notes_list, name="wf_task_notes_list"),
    url(r"^wf_t_n_c/", tasks.wf_t_n_c, name="wf_t_n_c"),
    url(r"^wf_t_f_c/", tasks.wf_t_f_c, name="wf_t_f_c"),
    url(r"^wf_t_t_c/", tasks.wf_t_t_c, name="wf_t_t_c"),
    #############################################################################################
    # TimeTracker
    url(r"^timetracker/", tt.timetracker, name="timetracker"),
    url(r"^get_week/", tt.get_week, name="get_week"),
    url(r"^tt_get_current/", tt.tt_get_current, name="tt_get_current"),
    url(r"^tt_filter_submit/", tt.tt_filter_submit, name="tt_filter_submit"),
    url(r"^add_time_entry/", tt.add_time_entry, name="add_time_entry"),
    url(r"^entry_add_form/", tt.entry_add_form, name="entry_add_form"),
    url(
        r"^display_time_entries/", tt.display_time_entries, name="display_time_entries"
    ),
    url(
        r"^get_tasks_for_project/",
        tt.get_tasks_for_project,
        name="get_tasks_for_project",
    ),
    url(
        r"^task_time_entry_form/", tt.task_time_entry_form, name="task_time_entry_form"
    ),
    url(
        r"^add_time_entry_for_task/",
        tt.add_time_entry_for_task,
        name="add_time_entry_for_task",
    ),
    url(
        r"^time_entry_edit_form/", tt.time_entry_edit_form, name="time_entry_edit_form"
    ),
    url(r"^delete_time_entry/", tt.delete_time_entry, name="delete_time_entry"),
    url(r"^time_entry_add_form/", tt.time_entry_add_form, name="time_entry_add_form"),
    url(r"^time_entry_add/", tt.time_entry_add, name="time_entry_add"),
    url(r"^time_entry_edit/", tt.time_entry_edit, name="time_entry_edit"),

    #############################################################################################
    # Users #
    #########
    url(r"^user_manage/", users.user_manage, name="user_manage"),
    url(r"^user_add_form/", users.user_add_form, name="user_add_form"),
    url(r"^user_add/", users.user_add, name="user_add"),
    url(r"^user_details/", users.user_details, name="user_details"),
    url(r"^user_update/", users.user_update, name="user_update"),
    url(r"^display_users/", users.display_users, name="display_users"),
    url(r"^user_delete/", users.user_delete, name="user_delete"),
    url(
        r"^user_delete_confirm/", users.user_delete_confirm, name="user_delete_confirm"
    ),
    url(r"^user_profile/", users.user_profile, name="user_profile"),
    url(r"^upload_avatar/", users.upload_avatar, name="apload_avatar"),
    url(r"^change_pass/", users.change_pass, name="password_change"),
    url(r"^user_pw_reset/", users.user_pw_reset, name="user_pw_reset"),
    url(
        r"^user_profile_update/", users.user_profile_update, name="user_profile_update"
    ),
    url(r"^ucpp/", users.ucpp, name="ucpp"),
    url(r"^ucgp/", users.ucgp, name="ucgp"),
    url(r"^ucip/", users.ucip, name="ucip"),
    #############################################################################################
    # UI #
    ######
    url(r"^display_sidenav/", proj.display_sidenav, name="display_sidenav"),
    #############################################################################################
    # Utils #
    #########
    url(r"^login/", utils.login_user, name="login_user"),
    url(r"^logout/", utils.logout_user, name="logout_user"),
    url(r"^get_form", utils.get_form, name="get_form"),
    # url(r'^timetracker/', include(tt_urls)),
    url(r"^send_feedback/", utils.send_feedback, name="send_feedback"),
    url(r"^feedback/", utils.feedback, name="feedback"),
    url(r"^admin/", admin.site.urls),
    url(r"^get_project_nav/", proj.get_project_nav, name="get_project_nav"),
    # Setters
    url(r"^u_aprfap", u_s_m.aprfap, name="aprfap"),
    url(r"^$", proj.home, name="home"),
    url(r"^close_project/", proj.close_project, name="close_project"),
    # url(r'^remove_vuln/(?P<report_id>.*)/(?P<uid>.*)', proj.remove_vuln, name='remove_vuln'),
    url(r"^overview/", proj.overview, name="overview"),
    # url(r'^import_table/(?P<uid>.*)', proj.import_table, name='import_table'),
    # url(r'^master_table/(?P<uid>.*)', proj.master_table, name='master_table'),
    # Url(r'^scrap_table/(?P<uid>.*)', proj.scrap_table,  name='scrap_table'),
    # url(r'^type_form/(?P<name>.*)', proj.load_form,     name='load_form'),
    # url(r'^notes/(?P<uid>.*)',  proj.notes,             name='notes'),
    # url(r'^calendar/',          proj.calendar,          name='calendar'),
    # url(r'^new_data/(?P<name>.*)/(?P<table>.*)', proj.new_data, name='new_data'),
    # url(r'^update_data_item/',  proj.update_data_item,  name='update_data_item'),
    # url(r'^remove_table_item/', proj.remove_table_item, name='remove_table_item'),
    # url(r'^find_model/',        proj.find_model,        name='find_model'),
    url(r"^startsession/", utils.startsession, name="startsession"),
    url(r"^pausesession/", utils.pausesession, name="pausesession"),
    url(r"^stopsession/", utils.stopsession, name="stopsession"),
    url(r"^getsession/", utils.getsession, name="getsession"),
    url(r"^temp/", proj.temp, name="temp"),
    url(
        r"^generic_delete_form/", utils.generic_delete_form, name="generic_delete_form"
    ),
    url(r"^generic_delete/", utils.generic_delete, name="generic_delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
+static(
         settings.STATIC_URL,document_root=settings.STATIC_ROOT
        )+static(
         settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
"""
try:
    from utils import consumers

    channel_routing = {
        "websocket.receive": consumers.ws_message,
        "websocket.connect": consumers.ws_connect,
        "websocket.disconnect": consumers.ws_disconnect,
    }
except:
    pass
