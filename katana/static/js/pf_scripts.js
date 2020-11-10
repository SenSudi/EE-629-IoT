function pfFileAdd (e) {
  e.preventDefault();
  var project_title = $('#project_title').text();
  $.get('/get_form/',{'app':'files','form':'FileUploadForm','form_id':'file-upload-form'},function(returned){
	var header        = "Associate New File(s) With "+project_title;
  var content       = returned;
  var strSubmitFunc = "pfFileSubmit(event)";
  var btnText       = "Submit File";
  doModal('dynamicModal', header, content, strSubmitFunc, btnText);
  $('#modalWindow').find('#btn-modal-form-submit').attr('id','btn-submit-file');
  $('#modalWindow').find('#file-upload-form').attr('action','/project_files/');
  $('#modalWindow').find('#file-upload-form').attr('method','POST');
  formatForm();
  });
}

function pfFileSubmit (e) {
  e.preventDefault();
  var btn = $(e.target);
  var modal = btn.closest('.modal');
	var form = modal.find('#file-upload-form');
	form.ajaxSubmit(function(returned){
    $('#files').empty().html(returned);
    $('#modalWindow').modal('hide');
  });
}

function pfFileDelete (e) {
  e.preventDefault();
  var btn = $(e.target);
  var file = btn.closest('.file');
  var fid = file.attr('data-item-id');
  $.get('/file_delete/',{'fid':fid},function(returned){
    if (returned.error) {
      var header        = "Error";
      var content       = returned.error;
      var strSubmitFunc = "closeAlertModal(this)";
      var btnText       = "OK";
      alertModal('alertModal', header, content, strSubmitFunc, btnText);
    } else if (returned.success) {
      var header        = "Attention!";
      var content       = returned.success;
      var strSubmitFunc = "pfFileDeleteConfirm(event)";
      var btnText       = "Delete";
      alertModal('alertModal', header, content, strSubmitFunc, btnText);
      var modal = $('#alertModal').find('.modal');
      var cancel_btn = '<button onclick="closeAlertModal(this)" class="btn pull-right">Cancel</button>';
      modal.find('.modal-footer').append(cancel_btn);
      modal.find('#btn-modal-form-submit').attr('id','btn-file-delete-confirm');
      modal.find('#btn-file-delete-confirm').attr('data-fid',fid)
    }
  });
}

function pfFileDeleteConfirm (e) {
  e.preventDefault();
  var btn = $(e.target);
  var modal = btn.closest('.modal');
  var fid = modal.find('#btn-file-delete-confirm').attr('data-fid');
  $.post('/file_delete/',{'fid':fid},function(returned){
    if (returned.error) {
      var header        = "Error";
      var content       = returned.error;
    } else if (returned.success) {
      var header        = "Success";
      var content       = returned.success;
    }
      modal.modal('hide');
      var strSubmitFunc = "closeAlertModal(this)";
      var btnText       = "OK";
      alertModal('alertModal', header, content, strSubmitFunc, btnText);
    if (returned.success) {
      $.get('/display_files/',function (files) {
        $('#files').empty().html(files);
      });
    }
  });
}

function pfHSB (e) {
  var val = $(this).find('b').attr('id');
  var url = '/display_files';
  $.get(url,{'val':val},function(returned){
    $('#files').empty().html(returned);
  });
}