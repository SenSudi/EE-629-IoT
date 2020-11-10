//##################################################################################
// NOTES //
//#########
//
// Add note button
//    - Populates the dynamicModal with the NoteForm
//    - Requires the parent object to have class .object
//    - Requires the parent object to have data-title and data-obj-type
//    - Requires the parent object to have data-obj-app, data-obj-model, data-obj-id
function narrative (command) {
  var nar = $(document).find('#narrative-input'); 
 switch (command){
  case 'show':
   // Show narrative input;
   nar.css('display','block');
   window.narrativeActive = true;
   nar.find('textarea').focus();
   break;
  case 'hide':
   // Hide narrative input;
   nar.css('display','none');
   window.narrativeActive = false;
   break;
  default:
   break;
 }
}

$(document).on('keyup',function(e){
  if (e.shiftKey && e.altKey && e.key == 'N' && window.project) {
    narrative('show');
  }
});

$(document).on('click.notes','#btn-narrative-input',function(){
  var btn = $(this);
  if (window.narrativeActive) {
    narrative('hide');
  } else {
    narrative('show');
  }
});

function submitNarrative (altText) {
  var container = $('#narrative-input').find('textarea');
  var text = container.val();
  if (altText) {
    text = altText;
  }
  $.post('/narrative/',{'body':text},function(returned){
    if (returned.success){
      //on return success clear contents
      container.val('');
      //hide input
      narrative('hide'); 
    }
  });
}

$(document).on('click.notes','#btn-narrative-submit',function(e){
  e.preventDefault();
  //send to server to create and add to project
  submitNarrative();
});

$(document).on('keyup','#narrative-input textarea',function(e){
  if (e.altKey && e.key == 'Enter') {
    submitNarrative();
  }
});

// $(document).on('click.notes', '.narrative .date',function(){
//   var btn = $(this);
//   var nar = btn.closest('.narrative');
//   var pk = nar.attr('data-pk');
//   var field = "#n-"+pk+"date"
//   btn.datepicker({dateFormat: 'yy-mm-dd',altField: field});
//   btn.datepicker("option","altField","field")
//   // dp.removeClass('ui-datepicker-inline');
//   // dp.css('float','right');
//   // dp.css('z-index','10000');
// });

// $(document).on('click.notes','.narrative td a',function(e){
//   e.preventDefault();
//   console.log($(this));
//   $(this).closest('.date').datepicker("destroy");
// });

$(document).on('click.notes','.btn-note-add',function(){
  var btn             = $(this);
  var object          = btn.closest('.object');
  var obj             = _getObjModelAttrs(object);
  $.get('/note_add_form/',function(returned){
    var header        = 'Add Note to '+obj.type+' <b>'+obj.title+'</b>';
    var content       = returned;
    var strSubmitFunc = '';
    var btnText       = '';
    var footer        = false;
    doModal('dynamicModal',header,content,strSubmitFunc,btnText,footer);
    formatForm();
    var modal = $('#dynamicModal').find('.modal');
    _setModalModelAttrs(modal,obj);
  });
});

$(document).on('click.notes','#btn-note-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-note-add');
  var data = _getModalModelAttrs(modal);
  data.where = $(document).find('#page-data').attr('where');
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  modal.modal('hide');
                }
              }
  };
  form.ajaxSubmit(options);
});

$(document).on('click.notes', '.btn-note-edit',function(){
  var btn = $(this);
  var object = btn.closest('.object');
  var obj = _getObjModelAttrs(object);
  $.get('/note_edit_form/',obj,function(returned){
    var header        = 'Update Note <b>'+obj.title+'</b>';
    var content       = returned;
    var strSubmitFunc = '';
    var btnText       = '';
    var footer        = false;
    doModal('dynamicModal',header,content,strSubmitFunc,btnText,footer);
    formatForm();
    var modal = $('#dynamicModal').find('.modal');
    _setModalModelAttrs(modal,obj);
  });
});

$(document).on('click','#btn-note-update',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-note-edit');
  var data = _getModalModelAttrs(modal);
  data.where = $(document).find('#page-data').attr('where');
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  modal.modal('hide');
                }
              }
  };
  form.ajaxSubmit(options);
});
//##################################################################################
// NOTE DETAILS //
//################
$(document).on('click.notes','.note-title',function(){
  var title   = $(this);
  var note    = title.closest('.note');
  var obj     = _getObjModelAttrs(note);
  $.get('/note_info/',obj,function(returned) {
    var modal = noteDetailsModal(returned);
    _setModalModelAttrs(modal,obj);
  });
});
//##################################################################################
// NOTE RELATIVES //
//##################
$(document).on('click','#modal-note-prev-ancestor',function(){
  var btn       = $(this);
  var modal     = btn.closest('.modal');
  var id        = btn.attr('data-obj-ancestor');
  if (id) {
    $.get('/note_info/',{'id':id},function(returned){
      modal.find('.modal-content').empty().html(returned);
    });
  } else {
    return false;
  }
});

$(document).on('click','#modal-note-next-child',function(){
  var btn       = $(this);
  var modal     = btn.closest('.modal');
  var id        = btn.attr('data-obj-child');
  if (id) {
    $.get('/note_info/',{'id':id},function(returned){
      modal.find('.modal-content').empty().html(returned);
    });
  } else {
    return false;
  }
});
//##################################################################################
// function noteTitleDetailsModal (obj) {
// 	var note            = $(obj).closest('.note');
//   var note_id         = note.attr('data-obj-id');
//   var title           = note.attr('data-obj-title');
//   var data            = {'note_id':note_id}
//   var url             = '/note_info/';
//   $.get(url,data,function(returned){
//     var header        = '<b>'+title+'</b>';
//     var content       = returned;
//     var strSubmitFunc = "";
//     var btnText       = "";
//     doModal('noteDetailsModal', header, content, strSubmitFunc, btnText);
//     var modal         = $('#noteDetailsModal').find('.modal');
//     modal.css('z-index','1100');
//     modal.css('margin-top','150px');
//     modal.find('.modal-content').css('box-shadow','1px 1px 1px 1px black');
//     modal.find('.modal-footer').append('<div class="row"><div class="col-md-3">Author: '+returned['creator']+'</div><div class="col-md-3"></div><div class="col-md-3"></div><div class="col-md-3">'+returned['created']+'</div></div>')
//     modal.find('.modal-content').css('background-color','white');
//     modal.find('.modal-header').css('border-bottom','none');
//     modal.find('.modal-footer').css('border-top','none');
//     modal.find('.modal-content').css('min-width','30%');
//     modal.modal('show');
//   });
// }

function noteEdit (obj) {
	var section = $(document).find('#page-data').attr('data-section');
	switch (section) {
		case 'Workflow':
			wfNoteEdit(obj);
			break;
		case 'Project Overview':
			ovvwNoteEdit(obj);
			break;
    case 'Issue Tracker':
      itNoteEdit(obj);
      break;
	}
}
