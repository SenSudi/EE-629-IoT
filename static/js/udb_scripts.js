$(document).on('click.udb','#btn-udb-user-add',function(){
	var btn = $(this);
	var data = _getObjModelAttrs(btn);
	$.get(data.url,function(returned){
		var modal = formModal(returned);
		formatForm();
	});
});

// function userUserAdd (obj) {
// 	$.get('/get_form/',{'app':'users','form':'UserForm','form_id':'add-user-form'},function(returned){
// 		var header        = "Add User";
//     	var content       = returned;
//     	var strSubmitFunc = "userUserSubmit(event)";
//     	var btnText       = "Submit";
//     	doModal('dynamicModal', header, content, strSubmitFunc, btnText);
//     	var modal         = $('#modalWindow');
//     	var form 		  = modal.find('#add-user-form');
//     	form.attr('action','/user_add/');
//     	form.attr('method','POST');
//     	formatForm();
// 	});
// }
function reloadUsers () {
	$.get('/display_users/',function(returned){
		$(document).find('#udb-users').empty().html(returned);
	});
}

$(document).on('click.udb','#btn-modal-user-add-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var form = modal.find('#form-udb-user-add');
	var data = {}
	data.where = $(document).find('#page-data').attr('where');
  	var options = {
    	data:data,
    	success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  reloadUsers();
                  modal.modal('hide');
                }
              }
  	};
  	form.ajaxSubmit(options);
});

// function userUserSubmit (e) {
// 	e.preventDefault();
// 	var btn 	= $(e.target);
// 	var modal 	= btn.closest('.modal');
// 	var form 	= modal.find('#add-user-form');
// 	form.ajaxSubmit(function(returned){
// 		$('#items').empty().html(returned);
// 		modal.modal('hide');
// 	});
// }

// function userUserDetails (obj) {
// 	var user 				= $(obj);
// 	var uid 				= user.attr('data-item-id');
// 	var username 			= user.find('.user_name').text();
// 	$.get('/user_details/',{'uid':uid},function(returned){
// 		var header 			= username + '\'s Details';
// 		var content 		= returned;
// 		var strSubmitFunc 	= '';
// 		var btnText 		= '';
// 		doModal('dynamicModal',header,content,strSubmitFunc,btnText);
// 		var modal 			= $('#modalWindow');
// 		modal.find('.modal-content').attr('data-username',username);
// 		modal.find('.modal-content').attr('data-uid',uid)
// 		modal.find('.modal-header').append('<i onclick="userUserEdit(this)" class="btn fa fa-edit pull-right" id="btn-user-edit" data-uid="'+uid+'"></i>')
// 		modal.find('.modal-header').css('padding-bottom','0');
// 	});
// }

$(document).on('click.udb','#btn-udb-user-edit',function(){
	var btn = $(this);
	var user = btn.closest('.user');
	var data = _getObjModelAttrs(user);
	$.get(data.url,data,function(returned){
		var modal = formModal(returned);
		_setModalModelAttrs(modal,data);
	});
});

// function userUserEdit (obj) {
// 	var btn = $(obj);
// 	var uid = btn.attr('data-uid');
// 	var modal = btn.closest('.modal');
// 	var header = modal.find('.modal-header');
// 	var body = modal.find('.modal-body');
// 	var footer = modal.find('.modal-footer');
// 	$.get('/user_update/',{'uid':uid},function (returned) {
// 		btn.remove()
// 		var text = header.find('h4').text() 
// 		header.find('h4').text('Edit '+text);
// 		body.empty().html(returned);
// 		footer.empty().append('<button onclick="userUserUpdate(event)" class="btn btn-success pull-right" id="btn-update-user">Update</button>')
// 		footer.append('<button onclick="userUserUpdateCancel(event)" class="btn pull-right" id="btn-update-cancel" style="margin-right:5px;">Cancel</button>')
// 		formatForm();
// 	});
// }


$(document).on('click.udb','#qwerty-pwr',function(){
	var btn = $(this);
	var modal = btn.closest('.modal');
	var edit_modal = $(document).find('#form-udb-user-update');
	edit_modal.focus();
	modal.modal('hide');
	// console.log(edit_modal);
	edit_modal.focus();
});

function _resetDetails (obj,uid) {
	modal = $(obj)
	var username = modal.find('.modal-content').attr('data-username');
	$.get('/user_details/',{'uid':uid},function(returned){
		modal.find('.modal-body').empty().html(returned);
		modal.find('.modal-footer').empty();
		modal.find('.modal-header').find('h4').text(username+'\'s Details');
		var edit = '<i onclick="userUserEdit(this)"';
				edit += ' class="btn fa fa-edit pull-right"';
				edit += ' id="btn-user-edit"';
				edit += 'data-uid="'+uid+'"></i>'
		modal.find('.modal-header').append(edit);
	});
	if ($('#alertModal').length > 0) {
		$('#alertModal').find('#modalWindow').modal('hide');
	}
}

$(document).on('click.udb','#btn-udb-user-update-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var form = modal.find('#form-udb-user-update');
	var data = _getModalModelAttrs(modal);
	data.where = $(document).find('#page-data').attr('where');
  	var options = {
    	data:data,
    	success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form,returned.errors);
                } else {
                  reloadUsers();
                  modal.modal('hide');
                }
              }
  	};
  	form.ajaxSubmit(options);
});

// function userUserUpdate (e) {
// 	e.preventDefault();
// 	var btn = $(e.target);
// 	var modal = btn.closest('.modal');
// 	var form = modal.find('#user-edit-form');
// 	var uid = modal.find('.modal-content').attr('data-uid');
// 	form.ajaxSubmit(function(returned){
// 		$('#items').empty().html(returned);
// 		_resetDetails('#'+modal.attr('id'),uid);
// 	});
// }

// function userUserUpdateCancel (e) {
// 	e.preventDefault();
// 	var btn = $(e.target);
// 	var modal = btn.closest('.modal');
// 	var uid = modal.find('.modal-content').attr('data-uid');
// 	// SEND MODAL selector
// 	cancelForm("_resetDetails('#dynamicModal',"+uid+")");
// }

function confirmDelete (content) {
    var modal = $('#alertModal');
    var html = '<div id="modalWindow" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="confirm-modal" aria-hidden="true" data-backdrop="static">';
    html += '<div class="modal-dialog">';
    html += '<div class="modal-content">';
    html += content;
    html += '</div>';// content
    html += '</div>';// dialog
    html += '</div>';// modalWindow    
    modal.html(html);
    modal.find('.modal').modal();
    modal.find('.modal').modal('show');
    var dialog = modal.find('.modal-dialog');
    modal.css('position','relative');
    modal.css('z-index','9990');
    dialog.css('width','30vw');
    dialog.css('margin-top','20vh');
    formatForm();
    return modal.find('.modal');
  }

$(document).on('click.udb','#btn-udb-user-delete',function(){
	var btn = $(this);
	var user = btn.closest('.user');
	var data = _getObjModelAttrs(user);
	$.get('/user_delete/',data,function(returned){
		var modal = confirmDelete(returned);
	});
});

$(document).on('click.udb','#btn-udb-user-delete-confirm',function(e){
	e.preventDefault();
	var btn 	= $(this);
	var modal 	= btn.closest('.modal');
	var form 	= modal.find('form');
	form.ajaxSubmit(function(returned){
		if (returned.errors) {
			populateFormErrors(form,returned.errors);
		} else if (returned.success) {
			reloadUsers();
			modal.modal('hide');
		}
	});
});

$(document).on('click.mrfb','.mrfb',function(){
	var btn = $(this);
	var data = _getObjModelAttrs(btn);
	$.get(data.url,data,function(returned){
		btn.closest('.modal-content').empty().html(returned);
		formatForm();
	});
});

$(document).on('click.udb','.udb-nav-tab',function(e){
	e.preventDefault();
	var tab = $(this);
	var pane = tab.closest('.udb-user-card-info').find('.tab-content');
	var data = _getObjModelAttrs(tab);
	$.get(data.url,data,function(returned){
		pane.empty().html(returned);
	});
});


$(document).on('click.user','#btn-reset',function(e) {
	e.preventDefault();
	var id = $(e.target).closest('.modal').attr('data-obj-id');
	$.get('/user_pw_reset/',{'uid':id},function(returned) {
		var modal = noteDetailsModal(returned);
		formatForm();
	});

    $(document).on('click.user','#btn-save',function(e){
        e.preventDefault();
        var modal = $(e.target).closest('.modal');
        var form = modal.find('#form-change-pass-reset');
        form.ajaxSubmit ({
            data:{'uid':id},
            success:function(returned) {
 		        if (returned.success) {
                    $(".modal-dialog").closest('.modal').modal('hide');
 		        } else if (returned.errors) {
 			        populateFormErrors(form,returned.errors);
 		        }
 		    }
        });
    });
});
