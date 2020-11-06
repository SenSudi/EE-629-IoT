function reloadTaskDetails (modal,data) {
	var container = modal.find('.modal-content');
	$.get(data.url,data,function(content){
		container.empty().html(content);
	});
}

$(document).on('click.tasks','.task-nav-tab',function(e){
	e.preventDefault();
	var tab = $(this);
	var pane = tab.closest('.modal').find('.tab-content');
	var data = _getObjModelAttrs(tab);
	$.get(data.url,data,function(returned){
		pane.empty().html(returned);
	});
});

$(document).on('click.tasks','.ctrl-task-edit',function(){
	var btn = $(this);
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	$.get('/wf_task_edit_form/',data,function(returned){
		modal.find('.modal-content').empty().html(returned);
		formatForm();
	});
});

$(document).on('click.tasks','.ctrl-task-refresh',function(){
	var btn 	= $(this);
	var modal 	= btn.closest('.modal');
	var data 	= _getModalModelAttrs(modal);
	$.get(data.url,data,function(returned){
		modal.find('.modal-content').empty().html(returned);
		formatForm();
	});
});

$(document).on('click.tasks','.ctrl-task-files',function(){
	var btn 			= $(this);
	var modal 			= btn.closest('.modal');
	var data 			= _getModalModelAttrs(modal);
	var container 		= modal.find('#task-details-form-container');
	data.action 		= '/wf_task_file_add/';
	data.form_id 		= 'form-wf-task-modal-file-add';
	data.submit_id 		= 'btn-wf-task-modal-file-submit';
	data.cancel_class 	= 'btn-wf-task-details-form-cancel';
	$.get('/afile_form/',data,function(returned){
		container.empty().html(returned);
		formatForm();
	})
});

$(document).on('click.tasks','.ctrl-task-note',function(){
	var btn 			= $(this);
	var modal 			= btn.closest('.modal');
	var data 			= _getModalModelAttrs(modal);
	var container 		= modal.find('#task-details-form-container');
	data.action 		= '/wf_task_note_add/';
	data.form_id 		= 'form-wf-task-modal-note-add';
	data.submit_id 		= 'btn-wf-task-modal-note-submit';
	data.cancel_class 	= 'btn-wf-task-details-form-cancel';
	$.get('/note_add_form/',data,function(returned){
		container.empty().html(returned);
		formatForm();
	})
});

$(document).on('click.tasks','.ctrl-task-time',function(){
	var btn 			= $(this);
	var modal 			= btn.closest('.modal');
	var data 			= _getModalModelAttrs(modal);
	var container 		= modal.find('#task-details-form-container');
	data.action 		= '/wf_task_time_add/';
	data.form_id 		= 'form-wf-task-modal-time-add';
	data.submit_id 		= 'btn-wf-task-modal-time-submit';
	data.cancel_class 	= 'btn-wf-task-details-form-cancel';
	$.get('/time_entry_add_form/',data,function(returned){
		container.empty().html(returned);
		formatForm();
	})
});

$(document).on('click.tasks','#btn-wf-task-modal-note-submit',function(e){
	e.preventDefault();
	var btn 	= $(this);
	var modal 	= btn.closest('.modal');
	var data 	= _getModalModelAttrs(modal);
	var form 	= modal.find('#form-wf-task-modal-note-add');
	var task 	= $(document).find('.task[data-obj-id='+data.id+']');
	var phase 	= task.closest('.phase');
	var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
					populateFormErrors(form,returned.errors);
                } else if (returned.success) {
					reloadTaskDetailsNotes(modal);
					reloadPhaseTasks(phase);
					clearTaskDetailsForm(modal);
                }
              }
  	};
  	form.ajaxSubmit(options);
});

$(document).on('click.tasks','#btn-wf-task-modal-time-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var data 	= _getModalModelAttrs(modal);
	var form 	= modal.find('#form-time-entry-add');
	var task 	= $(document).find('.task[data-obj-id='+data.id+']');
	var phase 	= task.closest('.phase');
	var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
					populateFormErrors(form,returned.errors);
                } else if (returned.success) {
					reloadTaskDetailsNotes(modal);
					reloadPhaseTasks(phase);
					clearTaskDetailsForm(modal);
					modalRefresh(btn);
                }
              }
  	};
  	form.ajaxSubmit(options);
});

$(document).on('click.tasks','.btn-modal-entry-edit',function(){
	var btn 			= $(this);
	var modal 			= btn.closest('.modal');
	var object			= btn.closest('.object');
	var data 			= _getObjModelAttrs(object);
	var container 		= modal.find('#task-details-form-container');
	data.action			= '/time_entry_edit/'
	data.form_id 		= 'form-wf-task-modal-entry-update';
	data.submit_id 		= 'btn-wf-task-modal-entry-update';
	data.cancel_class 	= 'btn-wf-task-details-form-cancel';
	$.get('/time_entry_edit_form/',data,function(returned){
		container.empty().html(returned);
		_setModalModelAttrs(modal.find('#form-wf-task-modal-entry-update'),data);
		formatForm();
	})
});

$(document).on('click.tasks','#btn-wf-task-modal-entry-update',function(e){
	e.preventDefault();
	var btn 	= $(this);
	var modal 	= btn.closest('.modal');
	var data 	= _getModalModelAttrs(modal);
	var form 	= modal.find('#form-wf-task-modal-entry-update');
	var task 	= $(document).find('.task[data-obj-id='+data.id+']');
	var phase 	= task.closest('.phase');
	data = _getModalModelAttrs(form);
	var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
					populateFormErrors(form,returned.errors);
                } else if (returned.success) {
					reloadTaskDetailsNotes(modal);
					reloadPhaseTasks(phase);
					clearTaskDetailsForm(modal);
					modalRefresh(btn);
                }
              }
  	};
  	form.ajaxSubmit(options);
});

function clearTaskDetailsForm (modal) {
	var container = modal.find('#task-details-form-container');
	container.empty();
}

function reloadTaskDetailsFiles (modal) {
	var container 	= modal.find('.task-files');
	var data 		= _getModalModelAttrs(modal);
	$.get('/wf_task_files_list/',data,function(returned){
		container.empty().html(returned);
	});
}

function reloadTaskDetailsNotes (modal) {
	var container 	= modal.find('.task-notes');
	var data 		= _getModalModelAttrs(modal);
	data.container_class = 'task-notes';
	$.get('/wf_task_notes_list/',data,function(returned){
		container.empty().html(returned);
	});
}

$(document).on('click.tasks','.btn-wf-task-details-form-cancel',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	clearTaskDetailsForm(modal);
});



$(document).on('click.tasks','#btn-wf-task-modal-file-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	var form = modal.find('#form-wf-task-modal-file-add');
	var task = $(document).find('.task[data-obj-id='+data.id+']');
	var phase = task.closest('.phase');
	var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
					populateFormErrors(form,returned.errors);
                } else if (returned.success) {
					reloadTaskDetailsFiles(modal);
					reloadPhaseTasks(phase);
					clearTaskDetailsForm(modal);
                }
              }
  };
  form.ajaxSubmit(options);
}); 

$(document).on('click.tasks','#btn-wf-task-update',function(e){
	e.preventDefault();
	var btn 	= $(this);
	//console.log(btn);
	var modal 	= btn.closest('.modal');
	var data 	= _getModalModelAttrs(modal);
	var task 	= $(document).find('.task[data-obj-id='+data.id+']');
	var phase 	= task.closest('.phase');
	var form 	= modal.find('#form-wf-task-update');
	var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  reloadPhaseTasks(phase);
                  reloadTaskDetails(modal,data);
                }
              }
  };
  form.ajaxSubmit(options);
});

$(document).on('click.tasks','#btn-wf-task-update-cancel',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	reloadTaskDetails(modal,data);
});
//#############################################################################
function recommendConfirmModal (data) {
	$.get('/task_files_select/',data,function(returned){
		var heading       = '';
		var content       = returned;
		var strSubmitFunc = 'closeAlertModal(this)';
		var btnText       = 'close';
		alertModal('alertModal',heading,content,strSubmitFunc,btnText);
		var modal 		  = $(document).find('#alertModal').find('.modal');
		_setModalModelAttrs(modal,data);
		modal.find('.modal-footer').append('<button class="btn btn-warning btn-task-recommend-submit">recommed</button>') 
		modal.addClass('modalTransparent');
	});		
}

$(document).on('click.tasks','#btn-wf-task-recommend',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	data.fileids = modal.find('#id_files').find(':selected').val();
	if (data.fileids) {
        recommendConfirmModal (data);
	} else {
        saveTasks(data, modal);
	}
});

function saveTasks(data, modal) {
    $.post('/wf_task_suggest/',data,function(returned){
        if (returned.success) {
            modal.modal('hide');
            reloadTaskDetails($('#taskDetailsModal').find('.modal'),data);
            var heading       = '';
            var content       = returned.success;
            var strSubmitFunc = 'closeAlertModal(this)';
            var btnText       = 'close';
            alertModal('alertModal',heading,content,strSubmitFunc,btnText);
        }
    });
}

$(document).on('click.tasks','.btn-task-recommend-submit',function(e){
	e.preventDefault();
	var btn 		= $(this);
	var modal 		= btn.closest('.modal');
	var data 		= _getModalModelAttrs(modal);
	data.file_ids 	= modal.find('input:checked').map(function(){return parseInt($(this).val())}).get();
	data.file_ids 	= data.file_ids.filter(function(n){ return(!isNaN(parseInt(n))) });
	saveTasks(data, modal);
});

$(document).on('click.tasks','.ctrl-task-add-refresh',function(){
	var btn 	    = $(this);
    var modal       = btn.closest('.modal');
    var form        = modal.find('.modal-content popped');
    var form_id     = modal.find('#form-wf-task-add');
    var phase_id    = form_id.find('#id_phases').val();
	$.get('/wf_task_add_form/',{'pid':phase_id},function(returned){
	    form.empty().html(returned);
	    formatForm();
    });
});
