function pdbProjectOpen (obj) {
	var btn 		= $(obj);
	var project = btn.closest('.project');
	var proj_id = project.attr('data-obj-id');
	var csrf		= $('#page-data').attr('data-csrf');
	var data 		= {'csrfmiddlewaretoken':csrf,'proj_id':proj_id,'state':'open'};
	var url 		= '/project_status/';
	$.post(url,data,function(returned){
	    var header          = "";
        var content         = returned
        var strSubmitFunc   = "closeAlertModal(this)";
        var btnText         = "Close";
        alertModal('dynamicModal', header, content, strSubmitFunc, btnText);
		    if (returned == 'Project Opened!') {
			    project.find('.proj-close').removeAttr('disabled');
			    btn.attr('disabled','disabled');
			    $('#content_paine').load('/projects_db/');
		    }
	});
}

function pdbProjectClose (obj) {
	var btn 		= $(obj);
	var project = btn.closest('.project');
	var proj_id = project.attr('data-obj-id');
	var csrf		= $('#page-data').attr('data-csrf');
	var data 		= {'csrfmiddlewaretoken':csrf,'proj_id':proj_id,'state':'close'};
	var url 		= '/project_status/';
	$.post(url,data,function(returned){
		var header          = "";
        var content         = returned
        var strSubmitFunc   = "closeAlertModal(this)";
        var btnText         = "Close";
        alertModal('dynamicModal', header, content, strSubmitFunc, btnText);
		if (returned == 'Project Closed!') {
			project.find('.proj-open').removeAttr('disabled');
			btn.attr('disabled','disabled');
			$('#content_paine').load('/projects_db/');
        }
	});
}

function project_Delete(obj){
	var object = $(obj).closest('.project');
	var data = _getObjModelAttrs(object);
	$.get('/generic_delete_form/',data,function(returned){
		var modal = formModal(returned);
		modal.attr('data-obj-id',data.id);
		modal.attr('data-obj-app',data.app);
		modal.attr('data-obj-model',data.model);
	});
}

