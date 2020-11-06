function refreshReports(){
	var container = $(document).find('#report-wizards-container');
	$.get('/display_reports/',function(returned){
		container.empty().html(returned);
	});
}

function formatWizard(modal) {
	var dialog = modal.find('.modal-dialog');
	modal.css('position','relative');
	modal.css('z-index','5000');
	dialog.css('width','70vw');
	dialog.css('margin-top','10vh');
}

$(document).on('click.rw','.rw-report-title',function(){
	var object = $(this).closest('.object');
	var data = _getObjModelAttrs(object);
	var modal = $(document).find('#formModal');
	$.get(data.details,data,function(returned){
		modal.empty().html(returned);
		var last_step_edited = modal.find('.wizard-steps').attr('id');
		var wiz = $(document).find('.wizard');
		$('.wizard').wizard({
			onFinish: function() {
        	    wizardFinish(wiz);
	    	}
		});
        $('.wizard').wizard('goTo',last_step_edited-1);
		modal.find('.modal').modal();
		modal.find('.modal').modal('show');
        modal.find('input[name="check"]').shiftSelectable();
		formatWizard(modal);
		formatForm();
		_setModalModelAttrs(modal.find('.modal'),data);
	});
});

$(document).on('click.rw','.btn-rw-wizard-add',function(){
	var btn = $(this);
	var url = btn.attr('data-url');
	$.get(url,function(returned){
		var modal = $(document).find('#formModal');
		modal.html(returned);
		modal.find('.modal').modal();
		modal.find('.modal').modal('show');
        modal.find('input[name="check"]').shiftSelectable();
		formatWizard(modal);
		modal.attr('data-details','/report_add_form/');
		formatForm();
		refreshReports();
	});
});

$(document).on('click.rw', '.wizard-close', function() {
    $('#content_paine').load('/report_wizard/');
});

$(document).on('change.rw','.rw-mb .form-control',function(){
    var input 		= $(this);
    var modal 		= input.closest('.modal');
    var object  	= input.closest('.object');
    var data 		= _getModalModelAttrs(modal);
    data.object 	= object.attr('data-obj-type');
    data.obj_app	= object.attr('data-obj-app');
    data.obj_model 	= object.attr('data-obj-model');
    data.obj_id 	= object.attr('data-obj-id');
    data.value = [];
    if (input.hasClass('select')) {
        var option  = object.find(':selected');
        var text    = option.text();
        if (text != '---Choose one---') {
            data.value.push(input.val());
        } else {
            data.value = ''
        }

    } else if (input.hasClass('multiSelect')) {
        $.each($("input[name='check']:checked"), function () {
            data.value.push($(this).val());
        });
    } else {
        data.value = input.val();
    }
    data.field = input.attr('name');
    $.post(data.edit,data);
});

$(document).on('click.rw', '.wizard-next',function(){
    _update_step_modified($(this));
});

function _update_step_modified(e) {
    var input 		= e;
    var modal 		= input.closest('.modal');
    var wizard  	= input.closest('.object');
    var object      = wizard.find('.wizard-steps').find('.current');
    var data 		= _getModalModelAttrs(modal);
    if(input.text() == 'Next'){
        var prev_step	= object.attr('step-sequence'); //The previously viewed step-sequence is present in prev_step.To get the latest step viewed of a particular report wizard step-sequence is incremented.
        data.sequence  = parseInt(prev_step)+1;
    } else{
        data.sequence = object.attr('step-sequence');
    }
    $.post('/report_wizard_update_step_modified/',data);
}

$(document).on('click.rw', '.wizard-back',function(){
    var wizard = $('.wizard').wizard();
    var current = wizard.find('ul').find('.current');
    var current_disable = current.addClass('disabled');
    var remove = current.removeClass('done');
    var current_seq_list = current.closest('li')
    var previous = current_seq_list.prev()
    var add = previous.addClass('current')
    previous.removeClass('done')
    _update_step_modified($(this));
});

$(document).on('click.rw','.btn-rw-report-start',function(){
	var data = {};
    data.title = $("#id_title").val();
    data.wizard = $("#id_wizard").val();
	$.get('/report_add/',data,function(returned){
        var modal = $(document).find('#formModal');
		modal.html(returned);
        modal.find('.modal').modal();
        formatWizard(modal);
		var modalBody =  $(modal).find('.modal');
		var data = _getModalModelAttrs(modalBody);
        data.details = '/report_wizard_content';
		$.get(data.details, data, function (returned) {
            modalBody.find('.modal-body').empty().html(returned);
            formatForm();
        });

	});
});

$(document).on('click.rw','.btn-var-item-add',function(e){
	e.preventDefault();
	var btn = $(this);
	var wizard_var = btn.closest('.object');
	var data = _getObjModelAttrs(wizard_var);
	$.get('/wizard_var_item_add/',data,function(returned){
		var modal = $(document).find('#dynamicModal');
		modal.html(returned);
		modal.find('.modal').modal();
		modal.find('.modal').modal('show');
		modal.css('position','relative');
		modal.css('z-index','9000');
		formatForm();
	});
});

$(document).on('click.rw','.btn-var-item-add-submit',function(){
	var btn = $(this);
	var modal = btn.closest('.modal');
	var wizard = $(document).find('#formModal').find('.modal');
	var data = _getModalModelAttrs(modal);
	var itemId = modal.attr('data-extra');
	var form = modal.find('form');
	var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
					populateFormErrors(form,returned.errors);
                } else if (returned.success) {
                    modal.modal('hide');
                    var itemType = returned.success.item_type;
                    var select = wizard.find('.select');
                    if (select[0].id.toLowerCase().includes(itemType.toLowerCase())) {
                        select.append('<option value="'+returned.success.id+'" selected>'+returned.success.title+'</option>');
                        select.trigger('change.rw')
					}
                    var multiSelect = wizard.find('.multiSelect');
                    if (multiSelect[0].id.toLowerCase().includes(itemType.toLowerCase())) {
                        multiSelect[0].insertAdjacentHTML( 'beforeend','<input name="check" class="chkbox" type="checkbox" style="margin-right:10px" value="'+returned.success.id+'" checked>'+ returned.success.title + '<br/>');
						multiSelect.trigger('change.rw')
                    }
                }
              }
  	};
  	form.ajaxSubmit(options);
});

// SEE: https://gist.github.com/AndrewRayCode/3784055
$.fn.shiftSelectable = function() {
    var lastChecked,
        $boxes = this;

    $boxes.click(function(evt) {
        if(!lastChecked) {
            lastChecked = this;
            return;
        }
        if(evt.shiftKey) {
            var start = $boxes.index(this),
                end = $boxes.index(lastChecked);
            $boxes.slice(Math.min(start, end), Math.max(start, end) + 1).each(function(){
                this.checked = lastChecked.checked;
                $(this).trigger('change');
            });
        }

        lastChecked = this;
    });
};

function ridbVariableAdd() {
    $.get('/report_variable_add/',function(returned){
        var header        = "Add Report Variable";
        var content       = returned;
        var strSubmitFunc = "reportVarSubmit(this)";
        var btnText       = "Add Variable";
        doModal('dynamicModal', header, content, strSubmitFunc, btnText);
        formatForm();
    });
}

function reportVarSubmit(obj){
    var form 	= $('#report-var-form');
	var content = $('#content_paine');
	form.ajaxSubmit(function(returned){
	$('.field-errors').empty();
		if (returned.errors) {
			var errors = returned.errors
			for (var field in errors) {
				var selector = '#'+field+'_errors';
				$(selector).append(' - '+'<b>'+errors[field]+'</b>');
				$(selector).css({'color':'red',
								 'margin-left':'10px',
								 'font-wieght':'bolder'
				});
			}
		} else if (returned.success) {
			$.get(returned.success,function(returned){
				content.empty().html(returned);
				$(document).find('#form-add-var').closest('#modalWindow').modal('hide');

	        });
        }

    });
}

$(document).on('click.delete','.btn-generic-delete-variable',function(obj){
    var obj = $(this).closest('.object');
    var id = obj.attr('id');
    $.ajax({
        type: 'POST',
        url: 'delete_report_variable/',
        data: {'id' : id},
        success: function(data) {
            if (data == 'success') {
                obj.remove();
                $('#content_paine').load('/report_variable/');
            }
        }
    });
});

function ReportVarEdit(obj){
    var var_obj = $(obj).closest('.object');
    var id = var_obj.attr('id');
    var url = '/report_variable_edit/';
    $.get(url,{'id':id},function(returned){
        var header        = "Update Report Variable";
        var content       = returned;
        var strSubmitFunc = "report_var_update(this)";
        var btnText       = "Update Variable";
        doModal('dynamicModal', header, content, strSubmitFunc, btnText);
        formatForm();
    });
}

function report_var_update(obj){
    var form = $('#report-var-edit-form');
	var content = $('#content_paine');
    var id = $(document).find(".btn-modal-add-var").attr('id');
    var data = {};
    data.id = id;
    data.display = $("#id_display").val();
    data.limit = $("#id_limit").val();
    data.template = $("#id_template").val();
    data.input_type = $("#id_input_type").val();
	$.post('/report_variable_edit/',data,function(returned){
	    $('.field-errors').empty();
		if (returned.errors) {
			var errors = returned.errors
			for (var field in errors) {
				var selector = '#'+field+'_errors';
				$(selector).append(' - '+'<b>'+errors[field]+'</b>');
				$(selector).css({'color':'red',
								 'margin-left':'10px',
								 'font-wieght':'bolder'
				});
			}
		} else if (returned.success) {
		    $.get(returned.success,function(returned){
				content.empty().html(returned);
				$(document).find('#report-var-edit-form').closest('#modalWindow').modal('hide');

	        });
        }
    });
}

function rvInputtypetFilter(obj){
    var option  = $(obj.target).find(':selected');
    var text    = option.text();
    var input_type  = option.val();
    var nvar_per_page = $('#no-of-variables').val();
    var search_string = $('#input-search-variable').val();
    var data = {};
    data.input_type = input_type;
    data.nvar_per_page = nvar_per_page;
    data.search_string = search_string;
    data.exact_match = $('#chk-exact-match').is(':checked')
    var url = '/report_variable_filter/';
    $.get(url,data,function(returned){
        $('#page-reload').empty().html(returned);
    });
}

function rvpagination(e){
    var btn = $(e.target);
    var page = btn.attr('id');
    var input_type = $('#input-type-filter').val();
    var search_string = $('#input-search-variable').val();
    var nvar_per_page = $('#no-of-variables').val();
    var data = {};
    data.page = page;
    data.input_type = input_type;
    data.nvar_per_page = nvar_per_page;
    data.search_string = search_string;
    data.exact_match = $('#chk-exact-match').is(':checked')
    $.get('/report_variable_filter/',data,function(returned){
        $('#page-reload').html(returned);
    });
}

function variable_per_page(obj) {
  var nvar_per_page = $(obj).val();
  var input_type = $('#input-type-filter').val()
  var search_string = $('#input-search-variable').val();
  var data = {};
  data.input_type = input_type;
  data.nvar_per_page = nvar_per_page;
  data.search_string = search_string;
  data.exact_match = $('#chk-exact-match').is(':checked');
  var url = '/report_variable_filter/'
  if (nvar_per_page){
    $.get(url,data,function(returned){
        $('#page-reload').empty().html(returned);
    });
  }
}

function searchBarVariable (obj) {
    var search_string = $(obj).val();
    var nvar_per_page = $('#no-of-variables').val();
    var input_type = $('#input-type-filter').val();
    var data = {};
    data.input_type = input_type;
    data.nvar_per_page = nvar_per_page;
    data.search_string = search_string;
    data.exact_match = $('#chk-exact-match').is(':checked');
    if(nvar_per_page && input_type) {
        var url = '/report_variable_filter/'
        $.get(url,data,function(returned) {
            $('#page-reload').empty().html(returned);
        });
    }
}
