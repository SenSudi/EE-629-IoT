function refreshTrackedIssues () {
  $.get('/display_tracked_issues/',function(returned){
    $(document).find('#it-issues').empty().html(returned);
  });
}

$(document).on('click.it','#btn-it-issue-add',function(){
  var modal = getForm($(this));
});

$(document).on('click.it','#btn-it-status-manage',function(){
  var btn = $(this);
  var url = btn.attr('data-url');
  $.get(url,function(returned){
    var modal = formModal(returned);
    modal.attr('data-details',url);
    modal.find('.modal-dialog').css('width','50vw');
  });
});

function recolorTable (table) {
  var c = true;
  var e = 'even';
  var o = 'odd';
  $.each(table.find('.object'),function(){
    var obj = $(this);
    obj.removeClass('odd');
    obj.removeClass('even');
    if (c) {
      obj.addClass(e);
      c = false;
    } else {
      obj.addClass(o);
      c = true;
    }
  });
}

function clearErrors (error_field) {
  error_field.empty();
  error_field.removeClass('popped');
  error_field.removeClass('modal-error-field');
}

function populateErrors (error_field,text) {
  error_field.empty().text(text);
  error_field.addClass('popped');
  error_field.addClass('modal-error-field');
}

$(document).on('click.it','.it-new-status-obj',function(){
  var obj         = $(this);
  var modal       = obj.closest('.modal');
  var error_field = modal.find('.modal-errors');
  var table       = modal.find('#it-modal-statuses');
  $.get(obj.attr('data-url'),function(returned){
    clearErrors(error_field);
    if (returned.errors) {
      populateErrors(error_field,returned.errors);
    }
    table.prepend(returned);
    recolorTable(table);
  });
});

function editableFieldSubmitOrCancel (field,key) {
  var modal       = field.closest('.modal');
  var error_field = modal.find('.modal-errors');
  var object      = field.closest('.object');
  var field_init  = field.text().trim();
  clearErrors(error_field);
  if (key == 'Escape') {
    field.blur();
    return false;
  } else {
    var data          = _getObjModelAttrs(object);
    data.content      = field.text().trim();
    data.content_type = field.attr('data-content');
    $.post(data.edit,data,function(returned){
      field.blur();
      if (returned.errors.sequence) {
        populateErrors(error_field,returned.errors.sequence);
        field.empty().text(field.attr('data-init'));
      }
    });
  }
}

// $(document).on('focus.it','.obj-editable-field',function(e){
//   var target = document.getElementById($(this).attr('id'));
//   console.log(target);
//   target.setSelectionRange(0, target.value.length);
// });


$(document).on('keypress.it','.obj-editable-field',function(e){
  var field = $(this);
  if (e.key == 'Enter' || e.key== 'Tab' || e.key == 'Escape') {
    e.preventDefault();
    editableFieldSubmitOrCancel(field,e.key);
  }
});

function statusSequenceChange(btn,direction) {
  var status  = btn.closest('.status');
  var data    = _getObjModelAttrs(status);
  var modal   = btn.closest('.modal');
  data.seq    = direction;
  var value   = parseInt(status.find('.it-status-object-sequence').text())
  var sequences = $('.it-status-object-sequence').map(function(){ return parseInt($(this).text()) }).get();
  sequences = sequences.filter(function(n){ return(!isNaN(parseInt(n))) });
  var max = Math.max.apply(Math,sequences);
  var min = Math.min.apply(Math,sequences);
  if (direction == 'down' && value == max) {
    var numOccurances = getOccuracnce(sequences,value);
    if (numOccurances == 1) {
      return false;
    }
  }
  if (direction == 'up' && value <= 1) {
    return false;
  }
  $.post(data.edit,data,function(returned){
    if (returned.success) {
      modalRefresh(btn);
    }
  });
}

$(document).on('click.it','.it-modal-status-seq-down',function(){
  var btn     = $(this);
  statusSequenceChange(btn,'down');
});

$(document).on('click.it','.it-modal-status-seq-up',function(){
  var btn     = $(this);
  statusSequenceChange(btn,'up');
});

// $(document).on('blur.it','.obj-editable-field',function(e){
//   console.log(e);
// });

// $(document).on('click.it','.btn-it-status-add',function(e){
//   e.preventDefault();
//   console.log($(this).attr('data-url'));
//   var modal = addFormItem($(this));
// });

$(document).on('click.it','#btn-modal-issue-add-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-it-issue-add');
  form.ajaxSubmit(function(returned){
    if (returned.errors) {
      populateFormErrors(form,returned.errors);
    } else if (returned.success) {
      refreshTrackedIssues();
      updateAudits('issue_tracker');
      modal.modal('hide');
    }
  }); 
});

$(document).on('click.it','.it-issue-title',function(){
  var btn     = $(this);
  var issue   = btn.closest('.object');
  var data    = _getObjModelAttrs(issue);
  $.get(data.details,data,function(returned){
    var modal = detailsModal(returned);
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.it','.it-modal-note-cancel, .it-modal-form-cancel',function(e){
  e.preventDefault();
  var btn = $(this);
  var container = btn.closest('.modal-form-container');
  container.empty();
});

$(document).on('click.it','#btn-it-modal-note-submit',function(e){
  e.preventDefault();
  var btn       = $(this);
  var modal     = btn.closest('.modal');
  var container = btn.closest('.modal-form-container');
  var data      = _getModalModelAttrs(modal);
  var form      = container.find('#form-issue-note-form');
  var options   = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else if (returned.success) {
                  container.empty();
                  refreshTrackedIssues();
                  modalRefresh(container);
                }
              }
  };
  form.ajaxSubmit(options);         
});

$(document).on('click.it','#btn-modal-files-submit',function(e){
  e.preventDefault();
  var btn       = $(this);
  var modal     = btn.closest('.modal');
  var container = btn.closest('.modal-form-container');
  var data      = _getModalModelAttrs(modal);
  var form      = container.find('#form-both-files');
  var options   = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else if (returned.success) {
                  container.empty();
                  refreshTrackedIssues();
                  modalRefresh(container);
                }
              }
  };
  form.ajaxSubmit(options);
});

$(document).on('click.it','.it-modal-issue-notes',function(){
  var tab       = $(this);
  var modal     = tab.closest('.modal');
  var data      = _getModalModelAttrs(modal);
  var notes_url = '/get_notes_list/';
  $.get(notes_url,data,function(returned){
    if (returned.errors) {
      console.log(returned.errors);
    } else {
      modal.find('.notes-list').empty().html(returned);
    }
  });
});

$(document).on('click.it','.it-modal-issue-files',function(){
  var tab       = $(this);
  var modal     = tab.closest('.modal');
  var data      = _getModalModelAttrs(modal);
  var notes_url = '/get_files_list/';
  $.get(notes_url,data,function(returned){
    if (returned.errors) {
      console.log(returned.errors);
    } else {
      modal.find('.files-list').empty().html(returned);
    }
  });
});

$(document).on('click.it','#btn-note-submit',function(e){
  e.preventDefault();
  window.setTimeout(refreshTrackedIssues(),2000);
});

// $(document).on('click.it','#btn-modal-issue-update-submit',function(e){
//   e.preventDefault();
//   refreshTrackedIssues();
// });

function getStatusSelect (selected) {
  $.get('/status_select_field/',{'id':selected},function(returned){
    return returned;
  });
}

function itIssueTrack (e) {
  e.preventDefault();
  var modal  = $(e.target).closest('.modal')
	var form   = modal.find('form');
	form.ajaxSubmit(function(returned){
    $('#issues').empty().html(returned);
    modal.modal('hide');
    updateAudits('issue_tracker');
  });
}


function itIssueEdit (obj) {
  var item_id       = $(obj).closest('.item').attr('id');
  var data          = {'item_id':item_id};
  var url           = '/issue_details/';
  var header        = "Update Issue";
  var content       = $('#update-sample').html();
  var strSubmitFunc = "itIssueUpdate(event)";
  var btnText       = "Update Issue";
  var info          = {};
  doModal('dynamicModal', header, content, strSubmitFunc, btnText);
  var modal = $('#modalWindow');
  modal.find('#btn-modal-form-submit').attr('id','btn-update-issue');
  $.get(url,data,function(returned){
    modal.find('#modal-form-div').empty().html(returned);
    var form = modal.find('form');
    form.attr('action','/issue_update/');
    form.attr('method','POST');
    form.append('<input type="hidden" name="id" value="'+item_id+'">');
    formatForm();
  });
}

function itIssueUpdate(e){
  e.preventDefault()
  var modal = $(e.target).closest('.modal')
  var form = modal.find('form');
  form.ajaxSubmit(function(returned){
    if (returned == 'Form is not valid!') {
      modal.find('.modal-body').append(returned);
    } else {
      $('#issues').empty().html(returned);
      modal.modal('hide');
      updateAudits('issue_tracker');
    }
  }); 
}


function itNoteModal (obj) {
  var item_id         = $(obj).closest('.item').attr('id');
  var data            = {};
  data['model_id']    = item_id;
  data['model_type']  = 'Issue';
  data['app']         = 'issuetracker';
  $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'note-form'},function(returned) {
    var header        = "Issue Notes";
    var content       = returned;
    var strSubmitFunc = "";
    var btnText       = "";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#modalWindow');
    modal.find('.modal').data('issue_id',item_id);
    modal.find('#modal-form-div').append('<button onclick="itNoteAdd(event)" class="btn btn-success btn-add-note">Add Note</button><hr>');
    modal.find('form').attr('action','/add_note/');
    $('#modalWindow').find('form').attr('method','POST');
    $('#note-form').append('<input type="hidden" name="id" value="'+item_id+'">');
    $('#note-form').append('<input type="hidden" name="model_type" value="Issue">');
    $('#note-form').append('<input type="hidden" name="app" value="issuetracker">');
    $('#note-form').append('<input type="hidden" name="where" value="issue_tracker">');
    formatForm();
    var url = '/get_notes_list/?header=true';
    $.get(url,data,function(returned){
      modal.find('.modal-body').append(returned);
    });
  });
}

function itNoteAdd (e) {
  e.preventDefault();
  var modal       = $(e.target).closest('.modal')
  var form        = modal.find('#note-form');
  var item_id     = form.find('input[name=id]').val();
  var item        = $('.item[id='+item_id+']');
  var note_count  = parseInt(item.find('.note-count').text());
  form.ajaxSubmit(function(returned){
    if (returned == 'Form is not valid!') {
      modal.find('.modal-body').append(returned);
    } else {
      modal.find('.modal-notes-div').remove();
      modal.find('.modal-body').append(returned);
      item.find('.note-count').text(note_count+1);
    }
    updateAudits('issue_tracker');
  }); 
}

function itNoteEdit (obj) {
  var note            = $(obj).closest('.note');
  var note_id         = note.attr('id');
  var modal           = note.closest('.modal');
  $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'edit-note-form','id':note_id,'model_app':'notes','model_type':'Note'},function(returned){
    var header        = '<b>'+note.find('.note-title').text()+'</b>';
    modal.find('.modal-header').find('h4').text(header);
    modal.find('#modal-form-div').empty().append(returned);
    modal.find('#modal-form-div').append('<button onclick="itNoteUpdate(event)" class="btn btn-success btn-update-note">Update Note</button><hr>');
    var form          = modal.find('#edit-note-form');
    form.attr('action','/update_note/');
    form.attr('method','POST');
    form.append('<input type="hidden" name="id"         value="'+note_id+'">');
    form.append('<input type="hidden" name="model_type" value="Issue">');
    form.append('<input type="hidden" name="app"        value="issuetracker">');
    form.append('<input type="hidden" name="header"     value="true">');
    form.append('<input type="hidden" name="where"      value="issue_tracker">');
    formatForm();
  });
}
// $(document).on('click','.btn-update-note',function(){});

function itNoteUpdate (e) {
  e.preventDefault();
  var btn   = $(e.target);
  var modal = btn.closest('.modal');
  var form  = modal.find('#edit-note-form');
  form.ajaxSubmit(function(returned){
    modal.find('.modal-notes-div').remove();
    modal.find('.modal-body').append(returned)
    $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'note-form'},function(returned) {
      modal.find('#modal-form-div').empty().append(returned);
      modal.find('#modal-form-div').append('<button onclick="itNoteAdd(event)" class="btn btn-success btn-add-note">Add Note</button><hr>');
      formatForm();
    });
  });
}

  // $(document).on('click','.note',function(){
  //   var note_id         = $(this).attr('id');
  //   var data            = {'csrfmiddlewaretoken':'{{csrf_token}}','note_id':note_id}
  //   var url             = '/note_info/';
  //   $.post(url,data,function(returned){
  //     //console.log(returned)
  //     var header = '<b>'+returned['title']+'</b>';
  //     var content = returned['body'];
  //     var strSubmitFunc = "submitForm()";
  //     var btnText = "";
  //     doModal('notesModal', header, content, strSubmitFunc, btnText);
  //     var modal = $('#notesModal').find('#modalWindow');
  //     modal.find('.modal-footer').append('<div class="row"><div class="col-md-3">Author: '+returned['creator']+'</div><div class="col-md-3"></div><div class="col-md-3"></div><div class="col-md-3">'+returned['created']+'</div></div>')
  //     modal.modal('show');
  //     modal.css('margin-top','150px');
  //     modal.find('.modal-content').css('background-color','#efe867');
  //     modal.find('.modal-header').css('border-bottom','1px solid black');
  //     modal.find('.modal-footer').css('border-top','1px solid black');
  //   });
  // });

function itProjectFilter (obj) {
  var option  = $(obj).find(':selected');
  var text    = option.text()
  var proj_id = option.val();
  var url     = '/display_tracked_issues/';
  $.get(url,{'p_id':proj_id},function(returned){
    $('#issues').empty().html(returned);
    if (proj_id != 'all'){
      $('#showing').empty().text(text);
    } else {
      $('#showing').empty().text('All Projects');
    }
  });
}

function itHSB (obj) {
  var val = $(obj).find('b').attr('id');
  var url = '/display_tracked_issues';
  $.get(url,{'val':val},function(returned){
    $('#issues').empty().html(returned);
  });
}