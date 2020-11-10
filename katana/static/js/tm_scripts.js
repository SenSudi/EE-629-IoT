function refreshWizards () {
	var container = $(document).find('#db-wizards-container');
	var url = '/db_display_wizards/';
	$.get(url,function(returned){
		container.empty().html(returned);
	});
}

function deployWizard (wizard) {
	var data 	= _getObjModelAttrs(wizard);
	var input	= wizard.find('.db-wizard-deploy');
	data.deploy = input[0].checked;
	var url 	= '/wizard_template_deploy/';
	$.post(url,data,function(returned){
		if (returned.success) {
			if (input[0].checked){
				input.removeAttr('checked');
			} else {
				input[0].checked = !data.deploy;
			}
			// refreshWizards();
		}
	});
}

$(document).on('click.tm','.btn-wt-template-file-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var form = btn.closest('form');
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	var options = {
    data:data,
    success: 	function(returned){
	                if (returned.errors) {
		                  populateFormErrors(form,returned.errors);
		                } else {
		                  modalRefresh(btn);
		                }
		            }
  				};
  	form.ajaxSubmit(options);
});

$(document).on('change.tm','.step-variables .wizard_var_input_type_select',function(){
	var select = $(this);
	var selected = select.find(':selected');
	var object = select.closest('.object');
	var content = selected.text();
	var data = _getObjModelAttrs(object);
	data.field = select.attr('data-attr-name');
	data.content = content;
	$.post(data.edit,data);
});

$(document).on('blur.tm','.step-variables .editable',function(){
	var field = $(this);
	var content = field.text();
	var object = field.closest('.object');
	var data = _getObjModelAttrs(object);
	data.field = field.attr('data-attr-name');
	data.content = content;
	$.post(data.edit,data);
});

$(document).on('keypress.tm','.step-variables .editable',function(e){
	var field = $(this);
	console.log(e);
	if(e.key == 'Enter') {
		e.preventDefault();
		field.blur();
	}
});

$(document).on('change.tm','.var_select',function(){
	var select = $(this);
	var template_tag = $(document).find('.template_tag');
	if(!select.val()){
		template_tag.closest('.form-group').addClass('collapsed');
	} else {
		template_tag.closest('.form-group').removeClass('collapsed');
	}
});

$(document).on('change.tm','.report_item_select',function(){
	var select = $(this);
	var var_select = $(document).find('.var_select');
	var new_pre_var_form = $(document).find('.new_pre_var_form');
	if (!select.val()) {
		var_select.closest('.form-group').addClass('collapsed');
		new_pre_var_form.addClass('collapsed');
	} else if (select.val() == 'new') {
		new_pre_var_form.removeClass('collapsed');
		var_select.closest('.form-group').removeClass('collapsed');
	} else {
		new_pre_var_form.addClass('collapsed');
		var_select.closest('.form-group').removeClass('collapsed');
	}
});

$(document).on('change.tm','.variable_type_select',function(){
	var select = $(this);
	var modal = select.closest('.modal');
	var option = select.find(':selected');
	var value = option.val();
	var new_var_form = modal.find('.new-var-form-container');
	var report_variable_container = modal.find('.report_variable-vars-container');
	var report_item_container = modal.find('.report_item-vars-container');
	if (value == 'report_variable') {
		report_item_container.addClass('collapsed');
		$(document).find('.selected').removeClass('selected');
		var no_of_report_variable_var = parseInt($('.report_variable-id').attr('id'));
	    if(no_of_report_variable_var > 10) {
            $('.report_variable-id').css('overflow','scroll')
	    }
		report_variable_container.removeClass('collapsed');
		new_var_form.addClass('collapsed');
	} else if (value == 'report_item') {
		report_variable_container.addClass('collapsed');
		$(document).find('.selected').removeClass('selected');
		var no_of_report_item_var = $('.report_item-id').attr('id')
		if(no_of_report_item_var > 10) {
            $('.report_item-id').css('overflow','scroll')
	    }
		report_item_container.removeClass('collapsed');
		new_var_form.addClass('collapsed');
	} else {
		report_variable_container.addClass('collapsed');
		report_item_container.addClass('collapsed');
		new_var_form.addClass('collapsed');
	}
});

function wizard_Add_Variable(obj) {
    var parentModal = $(document).find('#formModal').find('.modal');
	var btn = $(obj)
    var modal = btn.closest('.modal');
	var object = modal.find('.selected');
	var var_ids_list = [];
	var var_id = object.attr('data-obj-id');
	var type_select = modal.find('.variable_type_select');
	var confirmModal  = $(document).find('#alertModal').find('.modal');
	var template_tag = confirmModal.find('#id_template_tag').val();
    var steps = parentModal.find('.wt-step-nav-tab');
    var select = confirmModal.find('#id_var_select').val();
	var step_index;
	var step_active;
	for ( count = 0; count < object.length; count++){
        var var_id = jQuery(object[count]).attr('data-obj-id');
        var_ids_list.push(var_id);
	}
	for ( step_index = 0; step_index < steps.length; step_index++){
	    if (jQuery(steps[step_index]).hasClass('active')) {
	        step_active = jQuery(steps[step_index]);
	        var step_id = step_active.attr('data-obj-id');
	    }
	}
	var data = {};
	data.var_ids = var_ids_list;
	data.id = step_id;
    if(type_select.val() == 'report_variable') {
        data.var_type = 'c';
    } else {
        data.var_type = 'p';
        data.template = template_tag;
        data.select = select;
    }
	var url = '/db_wizard_step_var_add/';
    $.post(url,data,function(returned){
        modal.modal('hide');
	    getStepContent(step_active);
	});
}

$(document).on('change.tm','.db-wizard-deploy',function(){
	var input 	= $(this);
	var wizard 	= input.closest('.object');
	deployWizard(wizard);
});

$(document).on('click.tm','.btn-wt-deploy',function(){
	var btn 			= $(this);
	var container 		= btn.closest('#db-wizards-container');
	var selected 		= container.find('.selected');
	if (selected.length > 0) {
		$.each(selected,function(){
			var wizard 	= $(this);
			deployWizard(wizard);
		});
	}
});

function addVariable (sequence,data) {
	$.get('/db_wt_variable_list/',function(returned){
		var heading       = 'Select Variables for <b>Step '+sequence+'</b>';
	    var content       = returned;
	    var strSubmitFunc = 'closeAlertModal(this)';
	    var btnText       = 'close';
	    alertModal('alertModal',heading,content,strSubmitFunc,btnText);
	    var confirmModal  = $(document).find('#alertModal').find('.modal');
	    confirmModal.find('.modal-dialog').css('margin-top','5%');
	    confirmModal.find('.modal-content').css('margin-right','20%');
	    confirmModal.find('.modal-content').css('margin-left','-20%');
	    confirmModal.find('.modal-dialog').css('width','50%');
	    confirmModal.find('.modal-footer').append('<button class="btn btn-success" onclick="wizard_Add_Variable(this)" style="margin-left:10px;">Add</button>')
    	_setModalModelAttrs(confirmModal,data);
    	formatForm();
    });
}

$(document).on('click.tm','.btn-wt-modal-step-variable-add',function(){
	var btn = $(this);
	var container = btn.closest('.tab-pane');
	var sequence = container.attr('data-sequence');
	var data = _getObjModelAttrs(container);
	addVariable(sequence,data);
});

$(document).on('click.tm','.btn-wt-modal-step-add',function(){
	var btn = $(this).closest('li');
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	$.post('/wizard_template_step_add/',data,function(returned){
		btn.before(returned);
		var steps = modal.find('.wt-step-nav-tab');
		var step_last = jQuery(steps[(steps.length-1)]);
		if (step_last.length == 1) {
			getStepContent(step_last);
			steps.removeClass('active');
			step_last.addClass('active');
			step_last.attr('aria-expanded',true);
		}
	});
});

function getStepContent (tab) {
	var modal = tab.closest('.modal');
	var target = $(tab.find('a').attr('href'));
	var pane = modal.find('.tab-content');
	var data = _getObjModelAttrs(tab);
	$.get(data.url,data,function(returned){
		pane.empty().html(returned);
		formatForm();
	});
}

$(document).on('click.tm', '.wt-step-nav-tab',function(){
	var tab = $(this);
	getStepContent(tab);
});

$(document).on('click.tm','.wizards .click',function(e){
	e.preventDefault();
	var obj = $(this).closest('.object');
	var data = _getObjModelAttrs(obj);
	$.get(data.details,data,function(returned){
		var modal = formModal(returned);
		_setModalModelAttrs(modal,data);
		modal.addClass('object');
	});
});

$(document).on('click.tm','.btn-tm-wizard-add',function(){
	var btn = $(this);
	var url = btn.attr('data-url');
	$.get(url,function(returned){
		var modal = formModal(returned);
		modal.attr('data-details','/wizard_template_modal/');
		modal.addClass('object')
		$.get('/wizard_template_create/',function(info){
			_setModalModelAttrs(modal,info);
			refreshWizards();
		});
	});
});

$(document).on('blur.tm','.wt-m-b .form-control',function(){
	var field 		= $(this);
	if (field.attr('type') != 'file') {
		var modal 		= field.closest('.modal');
		var data  		= _getModalModelAttrs(modal);
		data.field 		= field.attr('name');
		data.content 	= field.val();
		data.object 	= field.closest('.object').attr('data-obj-model');
		data.object_id 	= field.closest('.object').attr('data-obj-id');
		$.post(data.edit,data,function(returned){
			console.log(returned);
		});
	}
});

$(document).ajaxSuccess(function(event,xhr,settings){
	if (typeof(xhr.responseText) != 'undefined') {
		var response = xhr.responseText;
		if (/class="(.*?wizard.*?)"(.*?)/.test(response)) {
			var wiz = $(document).find('.wizard');
			wiz.wizard({
				onFinish: function() {
        	wizardFinish(wiz);
	    	}
			});
		}
	}
});

function wizardFinish (wiz) {
    var wizard = $(wiz);
    var finishBtn = wizard.find('.wizard-buttons').find('.wizard-finish');
    var modal = wizard.closest('.modal');
    var data = _getModalModelAttrs(modal);
    $.post(data.export,data,function() {
         $('#content_paine').load('/report_wizard/');
         modal.modal('hide');
         _update_step_modified(finishBtn);
    });
}

$(document).on('click.tm','#wizard-dismiss',function(e){
	e.preventDefault();
    $('#content_paine').load('/template_manager/')
});

function wizard_step() {
    $("#step-tab").sortable({
        items: '.wt-step-nav-tab',
        update: wizardStepSortChange,
        tolerance: 'pointer',
        draggable: 'true',
    });
}

function  wizardStepSortChange(){
    var ul = document.getElementById("step-div").getElementsByTagName("li");
    $(ul).each(function(index){
        var id = $(this).attr('data-obj-id')
        var seq = index+1; //The index starts from zero but the step sequence starts from 1.Hence the index value is incremented by 1.
        if (id){
             $.post('/wizard_step_update/',{'id':id,'seq':seq},function(returned){
                    if (returned.error){
                        console.log(returned.error);
                    } else {
                        console.log(returned.success);
                    }
            });
        }
    });
}

function wizardSearchVariables (obj) {
    var search_string = $(obj).val();
    var type_select   = $('.variable_type_select').val();
    var data = {};
    data.search_string = search_string;
    data.type = type_select;
    data.exact_match = $('#chk-exact-match').is(':checked');
    $.get('/db_wt_variable_search/',data,function(returned) {
        if (type_select == 'report_variable') {
            $('.report_variable-id').html(returned);
        } else {
            $('.report_item-id').html(returned);
        }
    });
}