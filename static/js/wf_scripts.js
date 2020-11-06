function wfOnLoad () {
  // $.each($('.phase'),function(){
  //   var phase = $(this);
  //   wfUpdatePhase(phase);
  // });

  // $(document).find('.phases').sortable({
  //   placeholder: "ui-state-default"
  // });
  // $(document).find('.phase').draggable({
  //   connectToSortable: '.phases',
  //   revert: "invalid"
  // });
  // if($(document).find('.phase').length > 0) {
  //   console.log('yes');
  // }
  $(document).find('#phases').sortable({
    revert: true,
    items: '.phase',
    tolerance: 'pointer',
    container: 'parent',
    stop: phaseSortChange
  });
  $(document).find('.tasks').sortable({
    revert: true,
    items: '.task',
    tolerance: 'pointer',
    // container: 'parent',
    stop: taskSortChange
  });
}

function phaseSortChange (e,ui) {
  // console.log(e);
  // console.log($(ui.item[0]).parent().find('.phase'));
  var phases = $(ui.item[0]).parent().find('.phase');
  $.each(phases,function(index){
    var id = $(this).attr('id');
    // console.log(index + '- ' + id + ': ' + $(this).attr('data-obj-title') + ': ' +$(this).attr('data-sequence'));
    $.post('/phase_update/',{'id':id,'seq':index},function(returned){
      if (returned.error){
        console.log(returned.error);
      }
    });
  });
}

function taskSortChange (e,ui) {
  var tasks = $(ui.item[0]).parent().find('.task');
  $.each(tasks,function(index){
    var id = $(this).attr('id');
    $.post('/task_update/',{'id':id,'seq':index},function(returned){
      if (returned.error){
        console.log(returned.error);
      }
    });
  });
}

$(document).on('click.workflow','#btn-note-submit',function(){
  var where = 'workflow';
  if ($('#page-data').attr('where') == where) {
    var btn = $(this);
    var modal = btn.closest('.modal');
    var model = modal.attr('data-obj-model').toLowerCase();
    var id = modal.attr('data-obj-id');
    var object = $('.'+model+'[data-obj-id='+id+']');
    _updateObject(object);
    updateAudits(where);
    if (model == "phase"){
        wfReloadPhases();
    }
  }
});

$(document).on('click.workflow','#btn-time-entry-submit',function(){
  var where = 'workflow';
  if ($('#page-data').attr('where') == where) {
    var btn = $(this);
    var modal = btn.closest('.modal');
    var model = modal.attr('data-obj-model').toLowerCase();
    var id = modal.attr('data-obj-id');
    var object = $('.'+model+'[data-obj-id='+id+']');
    if(model == 'phase') {
        reloadPhaseTasks(object);
    } else {
       updateTaskTimeCount(object);
    }
    updateAudits(where);
  }
});

$(document).on('click.workflow','.wf-task-title',function(){
  var task = $(this).closest('.object');
  var data = _getObjModelAttrs(task);
  $.get(data.url,data,function(returned){
    var modal = taskDetailsModal(returned);
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.workflow','.modal-task-note-edit',function(){
  var btn = $(this);
  var note = btn.closest('.note');
  var modal = btn.closest('.modal');
  var data = _getObjModelAttrs(note);
  modal.focus();
  $.get('/note_edit_form/',data,function(returned){
    var note_form_div = modal.find('.notes-form');
    if (note_form_div.children().length > 0) {
      modal.focus();
    } else {
      note_form_div.empty().html(returned);
      note_form_div.prepend('<b>Edit - '+data.title+' </b>');
      note_form_div.addClass('task-modal-form-active');
      modal.find('#btn-note-update').attr('id','modal-task-note-update');
      modal.find('#btn-note-update-cancel').attr('id','modal-task-note-update-cancel');
      formatForm();
      var form = note_form_div.find('#form-note-edit');
      _setModalModelAttrs(form,data);
      modal.focus();
    }
  });
});

$(document).on('click.workflow','#modal-task-note-update-cancel',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var note_form_div = modal.find('.notes-form');
  note_form_div.empty();
  note_form_div.removeClass('task-modal-form-active');
  modal.focus();
});

$(document).on('click.workflow','#modal-task-note-update',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-note-edit');
  var data = _getModalModelAttrs(form);
  data.where = $(document).find('#page-data').attr('where');
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form.attr('id'),returned.errors);
                } else {
                  var note_form_div = modal.find('.notes-form');
                  note_form_div.empty();
                  note_form_div.removeClass('task-modal-form-active');
                  $.get('/task_details/',{'id':modal.attr('data-obj-id')},function(task){
                    modal.find('.modal-content').empty().html(task);
                  });
                }
              }
  };
  form.ajaxSubmit(options);
});
//###################################################################################
$(document).on('click.workflow','.workflow-phase-title',function(){
  var phase = $(this).closest('.object');
  var data = _getObjModelAttrs(phase);
  $.get('/phase_edit_form/',data,function(returned){
    var header        = 'Edit '+data.type+' <b>'+data.title+'</b>';
    var content       = returned;
    var strSubmitFunc = '';
    var btnText       = '';
    var footer        = false;
    doModal('dynamicModal',header,content,strSubmitFunc,btnText,footer);
    formatForm();
    var modal = $('#dynamicModal').find('.modal');
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.workflow','#btn-phase-update',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  //ADD RELOAD ALL PHASES
                  reloadPhases();
                  modal.modal('hide');
                }
              }
  };
  form.ajaxSubmit(options);
});

$(document).on('click.workflow','#btn-phase-recommend',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  $.post('/suggest_phase/',data,function(returned){
    if (returned.success) {
      var heading       = '';
      var content       = returned.success;
      var strSubmitFunc = 'closeAlertModal(this)';
      var btnText       = 'close';
      alertModal('alertModal',heading,content,strSubmitFunc,btnText);
      modal.modal('hide');
    }
  });
});
//###################################################################################
function _refreshTaskModalNotes (modal) {
  var task_id = modal.attr('data-obj-id');
  $.get('/get_task_notes/',{'id':task_id},function(returned){
    modal.find('.task-notes').empty().html(returned);
  });
}

function _updateObject (object) {
  if (object.attr('data-obj-type') == 'phase') {
    wfUpdatePhase(object);
  } else if (object.attr('data-obj-type') == 'task') {
    updateTaskNoteCount(object);
    updateTaskTimeCount(object);
  }
}

function updatePhaseTimeCount(phase) {
  attrs = _getObjModelAttrs(phase);
  id = attrs.id;
  $.get('/get_phase_total_time/',{'id':id},function(returned){
    phase.find('.phase-time').text(returned);
  });
}

function updateTaskTimeCount(task) {
  attrs = _getObjModelAttrs(task);
  id = attrs.id;
  $.get('/task_total_time/',{'id':id},function(returned){
    task.find('.task-time').text(returned);
    var phase = task.closest('.phase')
    reloadPhaseTasks(phase);
  });
}

function wfUpdatePhase (obj) {
	$.each($(obj),function(){
    var phase = $(this);
    updatePhaseTaskCount(phase);
    updatePhaseTimeCount(phase);
    updatePhaseNoteCount(phase);
  });
}

$(document).on('click.workflow','.btn-task-files',function(){
  var btn = $(this);
  var task = btn.closest('.object');
  var data = _getObjModelAttrs(task);
  data.url = '/wf_task_files_modal/';
  $.get(data.url,data,function(returned){
    var modal = formModal(returned);
    formatForm();
    _setModalModelAttrs(modal,data);
  });
});

function reloadFilesModal (modal,data) {
  var modal_content = modal.find('.modal-content');
  $.get(data.url,data,function(content){
    modal_content.empty().html(content);
    formatForm();
  });
}

$(document).on('click.workflow','#btn-modal-files-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-task-file-add');
  var data = _getModalModelAttrs(modal);
  var task = $(document).find('.task[data-obj-id='+data.id+']');
  var phase = task.closest('.phase');
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  reloadFilesModal(modal,data);
                  reloadPhaseTasks(phase);
                }
              }
  };
  form.ajaxSubmit(options);
});

function wfFilesModal (obj) {
  var item        = $(obj).closest('.item');
  if (item.length == 0) {
    var item = $(obj).closest('.modal').find('.item-data');
    var isModal = true;
  } else {
    var isModal     = false;
  }
  var item_title  = item.find('.item-title').text();
  var item_id     = item.attr('id');
  var model_type  = item.attr('data-model');
  var app         = item.attr('data-app');
  $.get('/get_form/',{'app':'files','form':'FileUploadForm','form_id':'file-form'},function(returned) {
    if (isModal == false) {
      var header        = item_title+" - Files";
      var content       = returned;
      var strSubmitFunc = "wfSubmitFile()";
      var btnText       = "Add File(s)";
      doModal('dynamicModal', header, content, strSubmitFunc, btnText);
      var modal         = $('#modalWindow');
      modal.find('#btn-modal-form-submit').attr('id','btn-submit-file');
      modal.find('.modal-body').append('<div id="files"></div>');
    } else {
      var modal         = $('#modalWindow');
      modal.find('.files-form').empty().html(returned);
      modal.find('.files-form').append('<button class="btn btn-success" id="btn-submit-file" onclick="wfSubmitFile(this)">Submit File(s)</button>')
    }
    var form            = modal.find('#file-form');
    form.attr('action','/task_file_upload/');
    form.attr('method','POST');
    form.append('<input type="hidden" name="model_id" value="'+item_id+'">');
    form.append('<input type="hidden" name="model_type" value="'+model_type+'">');
    form.append('<input type="hidden" name="app" value="'+app+'">');
    form.append('<input type="hidden" name="where" value="workflow">')
    formatForm();
    $.get('/files_list/?app='+app+'&model_id='+item_id+'&model_type='+model_type,function(returned) {
      var files = modal.find('#files');
      if (files.length = 0) {
        modal.find('.task-files').empty().html(returned);
      } else {
        files.empty().html(returned);
      }
    });
  });
}

function wfSubmitFile (obj) {
  var btn   	= $(obj);
  var modal 	= btn.closest('.modal');
	var form  	= modal.find('#file-form');
  var task_id = form.find('input[name=model_id]').val();
  var task 		= $('.task[id='+task_id+']');
	form.ajaxSubmit(function(returned){
    var files = modal.find('#files');
    if (files.length > 0){
      files.empty().html(returned);
    } else {
      modal.find('.task-files').empty().html(returned);
      modal.find('.files-form').empty();
    }
    updateTaskFileCount(task);
    updateAudits('workflow');
  });
  return false;
}

function wfNoteModal (obj) {
  var item        			= $(obj).closest('.item');
  if (item.length == 0) {
    var item 						= $(obj).closest('.modal').find('.item-data');
    var isModal 				= true;
  } else {
    var isModal     		= false;
  }
  var item_id     			= item.attr('id');
  var model_type  			= item.attr('data-model');
  var app         			= item.attr('data-app');
  var data 							= {};
  data['model_id']    	= item_id;
  data['model_type']  	= model_type;
  data['app']         	= app;
  $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'note-form'},function(returned) { 
    if (isModal == false) {
      var header        = model_type+" Notes";
      var content       = returned;
      var strSubmitFunc = "wfSubmitNote(this)";
      var btnText       = "";
      doModal('dynamicModal', header, content, strSubmitFunc, btnText);
      var modal 				= $('#dynamicModal').find('#modalWindow');
      modal.find('#modal-form-div').append('<button class="btn btn-success btn-add-note" onclick="wfSubmitNote(this)">Add Note</button><hr>');

    } else {
      var modal 				= $('#dynamicModal').find('#modalWindow');
      modal.find('.notes-form').empty().html(returned);
      modal.find('.notes-form').prepend('<hr>');
      modal.find('.notes-form').append('<button class="btn btn-success btn-add-note" onclick="wfSubmitNote(this)">Add Note</button><hr>');
    }
    var form 						= modal.find('#note-form')
    form.attr('action','/add_note/');
    form.attr('method','POST');
    form.append('<input type="hidden" name="id" value="'+item_id+'">');
    form.append('<input type="hidden" name="model_type" value="'+model_type+'">');
    form.append('<input type="hidden" name="app" value="'+app+'">');
    form.append('<input type="hidden" name="where" value="workflow">')
    formatForm();
    data['header'] 			= true;
    var url 						= '/get_notes_list/';
    $.get(url,data,function(returned){
      if (isModal) {
        modal.find('.task-notes').empty().html(returned);
      } else {
        modal.find('.modal-body').append(returned);
      }
    });
  });
}

function wfSubmitNote (obj) {
  var btn = $(obj);
  var modal = btn.closest('.modal');
  var form = modal.find('#note-form');
  var item_id = form.find('input[name=id]').val()
  var model = form.find('input[name=model_type]').val().toLowerCase();
  form.ajaxSubmit(function(returned){
    if (returned == 'Form is not valid!') {
      btn.parent().append(returned);
    } else {
      var notes = modal.find('.task-notes');
      if (notes.length > 0) {
        modal.find('.task-notes').empty().html(returned);
        modal.find('.notes-form').empty();
      } else {
        modal.find('.notes').empty();
        modal.find('.modal-notes-div').append(returned);
      }
      if (model != 'phase') {
        var phase = $('.'+model+'[id='+item_id+']').closest('.phase');
        reloadPhaseTasks(phase);
      } else {
        reloadPhases();
      }
      form[0].reset();
      updateAudits('workflow');
    }
  });
}

function wfNoteDetails (obj) {
    // var note_id = $(obj).closest('.note').attr('id');
    // var data = {'csrfmiddlewaretoken':'{{csrf_token}}','note_id':note_id}
    // var url = '/note_info/';
    // $.post(url,data,function(returned){
    //   var header 				= '<b>'+returned['title']+'</b>';
    //   var content 			= formatTextBlobNewlines(returned['body']);
    //   var strSubmitFunc = "";
    //   var btnText 			= "";
    //   doModal('noteDetailsModal', header, content, strSubmitFunc, btnText);
    //   var modal = $('#notesModal').find('#modalWindow');
    //   modal.find('.modal-footer').append('<div class="row"><div class="col-md-3">Author: '+returned['creator']+'</div><div class="col-md-3"></div><div class="col-md-3"></div><div class="col-md-3">'+returned['created']+'</div></div>')
    //   modal.modal('show');
    //   modal.css('margin-top','150px');
    //   modal.find('.modal-content').css('background-color','white');
    //   modal.find('.modal-header').css('border-bottom','none');
    //   modal.find('.modal-footer').css('border-top','none');
    //   modal.find('.modal-content').css('min-width','30%');
    // });
    noteTitleDetailsModal (obj);
}

function wfNoteEdit (obj) {
    var btn         = $(obj);
    var modal       = btn.closest('.modal');
    if (modal.length > 0) {
      var item_data   = modal.find('.item-data');
      if (item_data.length > 0) {
        var item_id     = item_data.attr('id');
        var model_type  = item_data.attr('data-model');
        var app         = item_data.attr('data-app');
      } else {
        var item_id     = modal.find('form').find('input[name=id]').val()
        var model_type  = modal.find('form').find('input[name=model_type]').val();
        var app         = modal.find('form').find('input[name=app]').val();
      }
      var item        = btn.closest('.note');
      var note_id     = item.attr('id');
      $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'edit-note-form','id':note_id,'model_app':'notes','model_type':'Note'},function(returned){
        if (item_data.length > 0) {
          modal.find('.notes-form').empty().html(returned);
          modal.find('.notes-form').prepend('<hr>');
          modal.find('.notes-form').append('<button class="btn btn-success btn-update-note" onclick="wfUpdateNote(this)">Update Note</button><hr>');
        } else {
          modal.find('#modal-form-div').empty().html(returned);
          modal.find('#modal-form-div').append('<button class="btn btn-success btn-update-note" onclick="wfUpdateNote(this)">Update Note</button><hr>');
        }
        var form = modal.find('#edit-note-form');
        form.attr('action','/update_note/');
        form.attr('method','POST');
        form.append('<input type="hidden" name="id" value="'+note_id+'">');
        form.append('<input type="hidden" name="model_id" value="'+item_id+'">');
        form.append('<input type="hidden" name="model_type" value="'+model_type+'">');
        form.append('<input type="hidden" name="app" value="'+app+'">')
        form.append('<input type="hidden" name="where" value="workflow">')
        formatForm();
      });
    } else {
      var phase       = $(obj).closest('.phase');
      var item_id     = phase.attr('id');
      var model_type  = phase.attr('data-model');
      var app         = phase.attr('data-app');
      var item        = btn.closest('.note');
      var note_id     = item.attr('id');
      var note_title  = item.find('.note-title').text();
      $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'edit-note-form','id':note_id,'model_app':'notes','model_type':'Note'},function(returned){
        var header        = "Edit - "+note_title;
        var content       = returned;
        var strSubmitFunc = "submitForm()";
        var btnText       = "Submit Changes";
        doModal('dynamicModal', header, content, strSubmitFunc, btnText);
        var modal = $('#modalWindow');
        var btn = modal.find('#btn-modal-form-submit');
        btn.attr('id','btn-update-note');
        btn.addClass('btn-update-note');
        btn.attr('onclick','wfUpdateNote(this)');
        form = modal.find('form');
        form.attr('action','/update_note/');
        form.attr('method','POST');
        form.append('<input type="hidden" name="id" value="'+note_id+'">');
        form.append('<input type="hidden" name="model_id" value="'+item_id+'">');
        form.append('<input type="hidden" name="model_type" value="'+model_type+'">');
        form.append('<input type="hidden" name="app" value="'+app+'">');
        form.append('<input type="hidden" name="where" value="workflow">')
        formatForm();
      });
    }
}

function wfUpdateNote (obj) {
  var form      = $(obj).closest('.modal').find('#edit-note-form');
  var item_id   = form.find('input[name=model_id]').val();
  var model     = form.find('input[name=model_type]').val().toLowerCase();
  var modal     = form.closest('.modal');
  form.ajaxSubmit(function(returned){
    if (returned == 'Form is not valid!') {
      $('.modal-body').append(returned);
    } else {
      if (model != 'phase') {
        if (modal.find('.task-notes').length > 0) {
          modal.find('.notes-form').empty();
          modal.find('.task-notes').empty().html(returned);
        } else {
          modal.find('.modal-notes-div').remove();
          $('.modal-body').append(returned);
        }
        var phase = $('.'+model+'[id='+item_id+']').closest('.phase');
        reloadPhaseTasks(phase);
      } else {
        reloadPhases();
        modal.modal('hide');
      }
      form[0].reset();
      updateAudits('workflow');
    }
  });
  return false;
}

function wfAddPhase (obj) {
	var project_title = $(document).find('#project_title').text();
	var btn 					= $(obj);
	$.get('/get_form/',{'app':'methodologies','form':'PhaseForm','form_id':'add-phase-form'},function(returned){
		var header 				= "Add Phase to "+project_title;
		var content 			= returned;
		var strSubmitFunc = "wfSubmitPhase(this)";
		var btnText 			= "Add New Phase";
		doModal('dynamicModal', header, content, strSubmitFunc, btnText);
		var modal 				= $('#modalWindow');
		var form 					= modal.find('form');
		modal.find('#btn-modal-form-submit').attr('id','btn-submit-phase');
		form.attr('action','/add_phase_to_project/');
		form.attr('method','POST');
		formatForm();
  });
}

function wfSubmitPhase (obj) {
	var btn 	= $(obj);
	var modal = btn.closest('.modal');
	var form 	= modal.find('form');
	form.ajaxSubmit(function(returned){
		$('#phases').empty().html(returned);
		$('#showing').empty().text('All Phases');
        $.each($('.phase'),function(){
            var phase = $(this);
            updatePhaseTaskCount(phase);
            updatePhaseTimeCount(phase);
        });
		modal.modal('hide');
		var container = document.getElementById("phase-select");
        var content = container.innerHTML;
        container.innerHTML= content;
         wfOnLoad();
		updateAudits('workflow');
	});
	return false;
}

function wfPhaseFilter (obj) {
  var option 		= $(obj).find(':selected');
  var text 			= option.text()
  var phase_id 	= option.val();
  var url 			= '/display_phases/';
  $.get(url,{'phase_id':phase_id},function(returned){
    $('#phases').empty().html(returned);
    if (phase_id != 'all'){
      $('#showing').empty().text(text);
    } else {
      $('#showing').empty().text('All Phases');
    }
  });
}

//Create new addTask form and call it
$(document).on('click.workflow','#btn-wf-task-add',function(){
  var btn = $(this);
  $.get('/wf_task_add_form/',function(returned){
    modal = formModal(returned);
  });
});

$(document).on('click.workflow','.btn-wf-phase-task-add',function(){
  var btn = $(this);
  var phase = btn.closest('.phase');
  var phase_id = phase.attr('data-obj-id');
  $.get('/wf_task_add_form/',{'pid':phase_id},function(returned){
    modal = formModal(returned);
  });
});

$(document).on('click.workflow','.btn-delete-task',function(e){
    e.preventDefault();
    var btn     = $(this);
    var object  = btn.closest('.object');
    var modal   = btn.closest('.modal');
    var data    = _getObjModelAttrs(object);
    var phase   = btn.closest('.phase');
    $.post(data.delete,data,function(returned){
        if (returned.success) {
	        if (btn.closest('.object').siblings().length > 0) {
	    	    object.remove();
	    	    updatePhaseTaskCount(phase);
	        }
	        else {
                reloadPhases();
	        }
        }
    });
});

function wfReloadPhases () {
  var phase_filter = $('#phase-select').val();
  $.get('/wf_reload_phases/',{'phase_filter':phase_filter}, function(returned){
    $('#phases').empty().html(returned);
    $(document).find('.tasks').sortable({
        revert: true,
        items: '.task',
        tolerance: 'pointer',
        stop: taskSortChange
    });

  });
}

$(document).on('click.workflow','#btn-modal-task-add-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-wf-task-add');
  // var data = _getModalModelAttrs(form);
  var data = {}
  data.where = $(document).find('#page-data').attr('where');
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form.attr('id'),returned.errors);
                } else {
                  wfReloadPhases();
                  modal.modal('hide');
                }
    }
  };
  form.ajaxSubmit(options);
});

$(document).on('click.workflow','#btn-modal-task-add-cancel',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  modal.modal('hide');
});
// function wfAddTask (obj) {
//   $.get('/get_form/',{'app':'tasks','form':'TaskForm','form_id':'add-task-form'},function(returned){
//     var header        = "Add New Task";
//     var content       = returned;
//     var strSubmitFunc = "wfSubmitTask(this)";
//     var btnText       = "Add Task";
//     var footer        = true;
//     doModal('dynamicModal', header, content, strSubmitFunc, btnText,footer);
//     var modal 				= $('#modalWindow');
//     modal.find('#btn-modal-form-submit').attr('id','btn-submit-task');
//     var form 					= modal.find('#add-task-form');
//     form.attr('action','/new_task/');
//     form.attr('method','POST');
//     form.append('<div class="form-group"><label for="phase"></label><div class="input-group"><div class="input-group-addon"></div><select id="phase" name="phase" class="form-control"></select></div></div>')
//     var select        = form.find('#phase');
//     select.css('width','30%');
//     $.each($('.phase'),function(){
//       var phase_id = $(this).attr('id');
//       var phase_title = $(this).find('.phase-title').text();
//       select.append('<option value="'+phase_id+'">'+phase_title+'</option>');
//     });
//     formatForm();
//   });
// }

function wfSubmitTask (obj) {
  var btn       = $(obj);
  var modal     = btn.closest('.modal');
  var form      = modal.find('#add-task-form');
  var phase_id  = form.find('#phase').find(':selected').val();
  var phase     = $('.phase[id='+phase_id+']');
  form.ajaxSubmit(function(returned){
    phase.find('.tasks').empty().html(returned);
    updatePhaseTaskCount(phase);
    updatePhaseTimeCount(phase);
    updateAudits('workflow');
    modal.modal('hide');
  });
  return false;
}

// function wfTaskDetails (obj) {
//   var item        		= $(obj).closest('.object');
//   var item_id     		= item.attr('data-obj-id');
//   var item_title  		= item.attr('data-obj-title');
//   $.get('/task_details/?item_id='+item_id,function(returned){
//     var header        = $('#sample-header').html();
//     var content       = returned;
//     var strSubmitFunc = "";
//     var btnText       = "";
//     doModal('dynamicModal', header, content, strSubmitFunc, btnText);
//     var modal 				= $('#modalWindow');
//     modal.find('.header-text').text(item_title);
//     modal.find('.modal-header').css('padding-bottom','5px');
//     modal.find('.modal-header').find('h4').css('margin-bottom','0px');
//     modal.find('.modal-footer').css('border-top','none');
//     modal.find('.modal-content').css('background-color','#dad8d8');
//   });
// }

function wfTaskEdit (obj) {
  var btn         			= $(obj);
  var modal       			= btn.closest('.modal');
  var header_text 			= modal.find('.header-text');
  var control_bar 			= modal.find('.control-bar');
  var body        			= modal.find('.modal-body');
  var item_data   			= modal.find('.item-data');
  var item_id     			= item_data.attr('id');
  var app         			= item_data.attr('data-app');
  var model_type  			= item_data.attr('data-model');
  var current_phase 		= $('.task[id='+item_id+']').closest('.phase');
  var phase_id 					= current_phase.attr('id');
  var phases 						= btn.closest(document).find('.phase');
  $.get('/get_form/',{'app':'tasks','form':'TaskForm','form_id':'edit-task-form','id':item_id,'model_app':app,'model_type':model_type},function(returned){
    body.empty().html(returned);
    var form 						= modal.find('#edit-task-form');
    form.append('<input type="hidden" name="id" value="'+item_id+'">');
    form.attr('action','/task_update/');
    form.attr('method','POST');
    form.append('<div class="form-group"><label for="id_phase"></label><div class="input-group"><div class="input-group-addon"></div><select id="id_phase" name="phase" class="form-control"></select></div></div>');
    var select          = form.find('select');
    select.css('width','30%');
    $.each(phases,function(){
      var phase_id 			= $(this).attr('id');
      var phase_title 	= $(this).find('.phase-title').text();
      select.append('<option value="'+phase_id+'">'+phase_title+'</option>');
    });
    select.find('option[value='+phase_id+']').attr('selected','selected');
    modal.find('.control-bar').css('display','none');
    form.append('<button class="btn btn-success btn-update-task" onclick="wfTaskUpdate(event)" style="display:inline;margin-right:10px;">Update Task</button>')
    form.append('<button class="btn btn-grey btn-cancel-update" onclick="wfTaskUpdateCancel(event)" style="display:inline;">Cancel</button>')
    form.append('<input type="hidden" name="current_phase" value="'+phase_id+'">')
    formatForm();
    //console.log(form[0])
  });
}

function wfTaskUpdate (e) {
  e.preventDefault();
  var btn       		= $(e.target);
  var modal     		= btn.closest('.modal');
  var form      		= modal.find('#edit-task-form');
  var task_id   		= form.find('input[name=id]').val();
  var old_phase_id 	= form.find('input[name=current_phase]').val();
  var old_phase 		= $('.phase[id='+old_phase_id+']');
  var new_phase_id 	= form.find('#id_phase').find(':selected').val();
  var new_phase 		= $('.phase[id='+new_phase_id+']');
  form.ajaxSubmit(function(returned){
    modal.find('.control-bar').css('display','block');
    modal.find('.modal-body').empty().html(returned);
    if (old_phase_id != new_phase_id) {
      reloadPhaseTasks(old_phase);
      reloadPhaseTasks(new_phase);
    }
  });
}

function wfTaskUpdateCancel (e) {
	e.preventDefault();
  var btn       = $(e.target);
  var modal     = btn.closest('.modal');
  var form      = modal.find('#edit-task-form');
  var task_id   = form.find('input[name=id]').val();
  $.get('/task_details/',{'item_id':task_id},function(returned){
    modal.find('.control-bar').css('display','block');
    modal.find('.modal-body').empty().html(returned);
  });
}

function wfTaskStateChange (obj) {
  var btn 			= $(obj);
  var state 		= btn.attr('name');
  var item 			= btn.closest('.task');
  if (state == item.find('#task-status-label').text()) {
    return false;
  }
  if (item.length==0) {
    var modal   = btn.closest('.modal');
    var item    = modal.find('.item-data');
    var isModal = true;
  } else {
    isModal 		= false;
  }
  var task_id 	= item.attr('id');
  $.post('/task_state/',{'task_id':task_id,'state':state},function(returned){
    if (isModal) {
      modal.find('.task-state').empty().html(returned);
      $('.task[id='+task_id+']').find('.task-state').empty().html(returned);
    } else {
      item.find('.task-state').empty().html(returned);
    }
    updateAudits('workflow');
  });
}