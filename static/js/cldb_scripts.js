function cldbClientAdd (obj) {
  $.get('/get_form/',{'app':'clients','form':'ClientForm','form_id':'add-client-form'},function(returned) {
  	var header        = "Add Client";
    var content       = returned;
    var strSubmitFunc = "cldbClientSubmit(event)";
    var btnText       = "Submit";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#modalWindow');
    var form 					= modal.find('#add-client-form');
    form.attr('action','/add_client/');
    form.attr('method','POST');
    formatForm();
  });
}

function cldbClientSubmit (e) {
  e.preventDefault();
  var btn = $(e.target);
  var modal = btn.closest('.modal');
  var form = modal.find('#add-client-form');
  form.ajaxSubmit(function(returned){
    $('#items').empty().html(returned);
    modal.modal('hide');
  });
}

function cldbClientDetails (obj) {
    var item = $(obj).closest('.item')
    console.log(item)
    console.log(item.attr('id'));
    $.get('/client_details/',{'item-id':item.attr('id')},function(returned){
        var header        = "Details for "+item.find('.item-name').text();
        var content       = returned;
        var strSubmitFunc = "";
        var btnText       = "";
        doModal('dynamicModal', header, content, strSubmitFunc, btnText);
        var modal = $('#modalWindow');
        modal.attr('data-form-val',true);
        modal.find('#item_id').val(ri.id);
        formatForm();
    });
}

function cldbDetailsProjectTitle (obj) {
  var project = $(obj).closest('.project');
  var p_id = project.attr('data-project-id');
  var modal = project.closest('.modal');
  $.get('/projects/'+p_id,function(returned){
    modal.modal('hide');
    $('#content_paine').empty().html(returned);
    $('#section').text($(document).find('#page-data').attr('data-section'));
    projectClickProjectLink($(obj).text());
  });
}

function cldbClientDelete (obj) {
  var item =  $(obj).closest('.item')
  var data = _getClientModelAttrs(item);
  data.content = "<h4><b>Associated Projects: "+data.project_count+"</b></h4><h4><b> Associated Contacts: "+data.contact_count+"</b></h4>"
  $.get('/generic_delete_form/',data,function(returned){
		var modal = formModal(returned);
		modal.attr('data-obj-id',data.id);
		modal.attr('data-obj-app',data.app);
		modal.attr('data-obj-model',data.model);
	});
}

function cldbClientEdit (obj) {
  var item        = $(obj).closest('.item')
  $.get('/client_update_form/',{'id':item.attr('id')},function(returned){
    var header        = "Update Client Info";
    var content       = returned;
    var strSubmitFunc = "cldbClientUpdate(this)";
    var btnText       = "Update";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    formatForm();
  });
}

function cldbClientUpdate (obj) {
    var form        = $('#client-edit-form');
    var content     = $('#content_paine');
    var id          = jQuery($('.form-group')[1]).attr('id');
    var data        = {};
    data.id         = id;
    form.ajaxSubmit({data:data});
    $.get('/display_clients/',function(returned){
        $('#items').empty().html(returned);
        $('#client-edit-form').closest('#modalWindow').modal('hide');
    });
}

function _getClientModelAttrs (object) {
    var obj_attrs           = {}
    obj_attrs.title         = object.attr('data-obj-title');
    obj_attrs.project_count = object.attr('data-obj-project-count');
    obj_attrs.contact_count = object.attr('data-obj-contact-count');
    obj_attrs.model         = object.attr('data-obj-model');
    obj_attrs.id            = object.attr('data-obj-id');
    obj_attrs.app           = object.attr('data-obj-app');
    return obj_attrs
  }
