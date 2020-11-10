function getPageData () {
  var page_data       = $('#page-data');
  project_title       = page_data.attr('data-proj-title');
  project_id          = page_data.attr('data-proj-id');
}

function ovvwNoteModal(obj){
  getPageData();
  $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'note-form'},function(returned) {
    var header        = "Add Note to "+project_title;
    var content       = returned;
    var strSubmitFunc = "ovvwNoteSubmit(event)";
    var btnText       = "Add Note";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#modalWindow');
    modal.find('#btn-modal-form-submit').attr('id','btn-submit-note');
    var form           = modal.find('#note-form');
    form.attr('action','/add_note/');
    form.attr('method','POST');
    form.append('<input type="hidden" name="id" value="'+project_id+'">');
    form.append('<input type="hidden" name="model_type" value="Project">');
    form.append('<input type="hidden" name="app" value="project">');
    form.append('<input type="hidden" name="header" value="true">');
    form.append('<input type="hidden" name="where" value="overview">');
    formatForm();
  });
}

function ovvwNoteSubmit (e){
  e.preventDefault();
  var btn = $(e.target);
  var modal = btn.closest('.modal');
  var form = modal.find('form');
  form.ajaxSubmit(function(returned){
    $('#notes').empty().html(returned);
    var count = parseInt($('.project-note-count').text())
    $('.project-note-count').text(count+1);
    var notecount = parseInt($('.note-count').text())
    $('.note-count').text(notecount+1);
    modal.modal('hide');
    updateAudits('overview');
  });
}

function ovvwNoteDetails (obj){
    noteTitleDetailsModal (obj);
}

function ovvwNoteEdit (obj){
  getPageData();
  var note            = $(obj).closest('.note');
  var note_id         = note.attr('data-obj-id');
  $.get('/get_form/',{'app':'notes','form':'NoteForm','form_id':'edit-note-form','id':note_id,'model_app':'notes','model_type':'Note'},function(returned){
    var header        = '<b>'+note.find('.note-title').text()+'</b>';
    var content       = returned;
    var strSubmitFunc = "ovvwNoteUpdate(event)";
    var btnText       = "Update Note";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#dynamicModal').find('#modalWindow');
    modal.find('#btn-modal-form-submit').attr('id','btn-edit-note');
    var form          = modal.find('#edit-note-form');
    form.attr('action','/update_note/');
    form.attr('method','POST');
    form.append('<input type="hidden" name="id"         value="'+note_id+'">');
    form.append('<input type="hidden" name="model_id"   value="'+project_id+'">');
    form.append('<input type="hidden" name="model_type" value="Project">');
    form.append('<input type="hidden" name="app"        value="project">');
    form.append('<input type="hidden" name="header"     value="true">');
    form.append('<input type="hidden" name="where"      value="overview">');
    formatForm();
  });
}

function ovvwNoteUpdate (e){
  e.preventDefault();
  var btn = $(e.target);
  var modal = btn.closest('.modal');
  var form = modal.find('#edit-note-form');
  form.ajaxSubmit(function(returned){
    $('#notes').empty().html(returned);
    updateAudits('overview');
    modal.modal('hide');
  });
}

function ovvwMilestoneAdd (obj) {
  var btn = $(obj);
  var parent = btn.closest('.milestones');
  $.get('/get_form/',{'app':'project','form':'MilestoneForm','form_id':'new-milestone-form','arg':true},function(returned){
    var header        = 'New Milestone';
    var content       = returned;
    var strSubmitFunc = "ovvwMilestoneSubmit(event)";
    var btnText       = "Submit";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#dynamicModal').find('#modalWindow');
    modal.find('#btn-modal-form-submit').attr('id','btn-submit-milestone');
    var form          = modal.find('#new-milestone-form');
    form.attr('action','/milestone_add/');
    form.attr('method','POST');
    form.attr('onchange','ovvwMilestoneFormChange(event)');
    // $.get('/get_milestone_tasks/',function(info){
    //   var choices = info.choices;
    //   var tasks = $('#id_tasks');
    //   var group = '';
    //   tasks.empty();
    //   for (choice in choices) {
    //     if (choices[choice].label) {
    //       var id = choices[choice].data_id
    //       var label = choices[choice].label
    //       tasks.append('<optgroup data-id="'+id+'" label="'+label+'">')
    //       group = $('optgroup[data-id='+id+']');
    //     } else {
    //       group.append(choices[choice])
    //     }
    //   }
    // });
    formatForm();
  }); 
}

function ovvwMilestoneFormChange (e) {
  // var input = $(e.target);
  // var form = input.closest('form');
  // var tasks = form.find('#id_tasks');
  // tasks.find('option').prop('selected',false);
  // if (input.attr('id') == 'id_phases') {
  //   var selected = input.find(':selected');
  //   $.each(selected,function(){
  //     var id = selected.val();
  //     var group = tasks.find('optgroup[data-id='+id+']');
  //     $.each(group,function(){
  //       $(this).find('option').prop('selected',true);
  //       console.log($(this).find('option'))
  //     });
  //   });
  // }
}

function ovvwMilestoneSubmit (e) {
  e.preventDefault();
  var btn = $(e.target);
  var modal = btn.closest('.modal');
  var form = modal.find('#new-milestone-form');
  form.ajaxSubmit(function(returned){
    $('.milestones').empty().html(returned);
    modal.modal('hide');
  });
}

function ovvwMilestoneBody (obj) {
  var btn = $(obj);
  var ms = btn.closest('.milestone');
  var body = ms.find('.body');
  if (btn.hasClass('fa-plus')) {
    body.css('display','block');
    btn.removeClass('fa-plus');
    btn.addClass('fa-minus');
  } else if (btn.hasClass('fa-minus')) {
    body.css('display','none');
    btn.removeClass('fa-minus');
    btn.addClass('fa-plus');
  }
}

function ovvwMilestoneDelete (obj) {
  var btn      = $(obj);
  var parent   = btn.closest('.milestone');
  var ms_id    = parent.attr('id');
  var location = parent.closest('.milestones').attr('id');
  $.ajax({
    type: 'POST',
    url: '/milestone_delete/',
    data: {'milestone_id' : ms_id, 'location': location},
    success: function(returned) {
      $('.milestones').empty().html(returned);
    }
  });
}

function ovvwMilestoneStateChange (obj) {
  var btn      = $(obj);
  var state    = btn.attr('name');
  var parent   = btn.closest('.milestone');
  var ms_id    = parent.attr('id');
  if (state == parent.find('#milestone-status-label').text()) {
    return false;
  }
  $.post('/milestone_state/',{'ms_id':ms_id,'state':state},function(returned){
    parent.find('.milestone-state').empty().html(returned);
  });
}
