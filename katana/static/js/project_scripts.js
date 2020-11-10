// $('#id_client').keydown(function(){
// 	if ($(this).val() != ''){
// 		$(this).parent().addClass('ui-widget');
// 		data = {'val' : $(this).val(), 'csrfmiddlewaretoken': '{{csrf_token}}'}
// 		url = /find_model/
// 		$.post(url,data,function(returned){
// 			var clientsList = returned['clients']
// 			$('#id_client').autocomplete({source: clientsList});
// 		});
// 	}
// });


		// ADD FUNCTIONALITY TO POPULATE CURRENT VIPS INTO VIP SELECT



function projectProjectNavDisplay () {
	if ($('#project_nav_header').length == 0) {
      $.get('/get_project_nav/',function(returned){
        $('#projects-dropdown').after(returned);
        $('#projects-dropdown').removeClass('active');
        $('#projects-dropdown').find('.nav-second-level').attr('aria-expanded','false');
        $('#projects-dropdown').find('.nav-second-level').removeClass('in');
        $('#projects-dropdown').find('.nav-second-level').css('height:0px;');
      });
    }
}

function projectClickProjectLink (text) {
	projectProjectNavDisplay();
    $('#project_title').text(text);
    $('#project_title_link').attr('href','/overview');
    $('#project_title_link').addClass('cpll');
    $('.side-nav-link').removeClass('active');
    $(document).find('#side-menu').find('#overview').addClass('active');
}

function projectNewProjectSubmit (e) {
	e.preventDefault();
	var form 	= $('#proj-form');
	var content = $('#content_paine');
	var title 	= form.find('#id_title').val();
	$('#wrapper').prepend('<div class="preloader" id="preloader"><div class="cssload-speeding-wheel" id="cssload-speeding-wheel"></div></div>');
    var options = {
        error: function(){
            $('#preloader').remove();
		    $('#cssload-speeding-wheel').remove();
        },
        success: function(returned){
        $('.field-errors').empty();
		    if (returned.errors) {
			    var errors = returned.errors
			    for (var field in errors) {
				    var selector = '#'+field+'_errors';
				    $(selector).append(' - '+'<b>'+errors[field]+'</b>');
				    $(selector).css({'color':'red',
								     'margin-left':'10px',
								     'font-wieght':'bolder'});
				    $('#preloader').remove();
				    $('#cssload-speeding-wheel').remove();
			    }
		    } else if (returned.success) {
			    $.get(returned.success,function(returned){
				    content.empty().html(returned);
				    projectClickProjectLink(title);
				    var section = $(document).find('#page-data').attr('data-section');
				    $('#section').text(section);
				    $('#preloader').remove();
				    $('#cssload-speeding-wheel').remove();
			    });
		    }
        }
    }
    form.ajaxSubmit(options);
}

function projectClientSelect (e) {
	var client 		= $(e.target);
	var selected 	= client.find(':selected');
	var field 		= $('#gprcf');
	if (selected.val() != '') {
		var data 		= {'model_id':selected.val()}; 
		$.get('/p_gpcfi/',data,function(returned){
			field.empty().append(returned);
		});
		if ($('#id_role').length == 0 ) {
			$.get('/p_gprf/',function(returned){
				$('#gprf').empty().prepend(returned)
			});
		}
		if ($('#assign-message').length == 0) {
			$.get('/p_gprfm/',function(returned){
				$('#gprfcol').append(returned)
			});
		}	
		formatForm();
	}
}

function projectPersonChange (e) {
	var person = $(e.target);
	var selected = person.find(':selected').val();
	if (selected == 'add') {
			person.children().removeAttr('selected');
			projectPersonAdd();
	}
}

function projectPersonAdd () {
	var client 					= $('#id_client').find(':selected');
	var name 						= client.text();
	var c_id 						= client.val(); 
	$.get('/get_form/',{'app':'contacts','form':'ContactOnlyForm','form_id':'person-add-form'},function(returned){
		var header        = 'Add Contact to '+name;
	  var content       = returned;
	  var strSubmitFunc = "projectPersonSubmit(event)";
	  var btnText       = "Submit";
	  doModal('dynamicModal', header, content, strSubmitFunc, btnText);
	  var modal         = $('#modalWindow');
	  modal.find('#btn-modal-form-submit').attr('id','btn-person-submit');
	  var form = modal.find('#person-add-form');
	  form.append('<input type="hidden" value="'+c_id+'" name="c_id" id="c_id">');
	  form.attr('method','POST');
	  form.attr('action','/acfnpf/');
	  formatForm();
	});
}

function projectPersonSubmit (e) {
	e.preventDefault();
	var btn 	= $(e.target);
	var modal = btn.closest('.modal');
	var form 	= modal.find('#person-add-form');
	var first = form.find('#id_first_name').val();
	var last = form.find('#id_last_name').val();
	form.ajaxSubmit(function(returned){
			if (returned['errors']) {
				// ADD ERROR REPORTING HERE
			}	else {		
				modal.modal('hide');
				$('#gprcf').empty().append(returned);
				var opts = $('#gprcf').find('#id_person').find('option');
				opts.attr('selected','');
				$.each(opts,function(){
					if($(this).text().search(first + ' ' + last)){
						$(this).attr('selected','selected');
					}
				});
				formatForm();
			}
	});
}

function projectRoleChange (e) {
	var role = $(e.target);
	var selected = role.find(':selected').val();
	if (selected == 'add') {
			role.children().removeAttr('selected');
			projectRoleAdd();
	}
}

function projectRoleAdd () { 
	$.get('/get_form/',{'app':'utils','form':'RoleForm','form_id':'role-add-form'},function(returned){
		var header        = 'Add New Role';
	  var content       = returned;
	  var strSubmitFunc = "projectRoleSubmit(event)";
	  var btnText       = "Submit";
	  doModal('dynamicModal', header, content, strSubmitFunc, btnText);
	  var modal         = $('#modalWindow');
	  modal.find('#btn-modal-form-submit').attr('id','btn-role-submit');
	  var form = modal.find('#role-add-form');
	  form.attr('method','POST');
	  form.attr('action','/u_aprfap/');
	  formatForm();
	});
}

function projectRoleSubmit (e) {
	e.preventDefault();
	var btn 				= $(e.target);
	var modal 			= btn.closest('.modal');
	var form 				= modal.find('#role-add-form');
	var val_list		= []
	var values 			= $('#id_role').find('option');
	$.each(values,function(){val_list.push($(this).val())});
	form.ajaxSubmit(function(returned){
		$('#gprf').empty().prepend(returned);
		var new_roles = $('#id_role').find('option');
		$.each(new_roles,function(){
			if (val_list.includes($(this).val())==false) {
				$(this).attr('selected','selected');
			}
		});
		modal.modal('hide');
	});
}

function projectAssignRole (e) {
	e.preventDefault();
	var btn 		= $(e.target);
	var form 		= btn.closest('form');
	var message = form.find('#assign-message');
	var person 	= form.find('#id_person');
	var role 		= form.find('#id_role');
	var csrf 		= form.find('name[csrfmiddlewaretoken]').val();
	var output 	= '';
	var r_id = role.find(':selected').val();
	var p_id = person.find(':selected').val();

	if (person.find(':selected').val() == '') {
		output += 'Error: No person selected';
		if (role.find(':selected').val() == '') {
			if (output == '') {
				output += 'Error: No role selected';
			} else {
				output += ' / ';
				output += 'no role selected';
			}
		}
		message.text(output);
		message.css('color','red');
	} else if (role.find(':selected').val() == '') {
		if (output == '') {
			output += 'Error: No role selected';
		} else {
			output += ' / ';
			output += 'no role selected';
		}
		message.text(output);
		message.css('color','red');
	} else if (p_id == 'add' || r_id == 'add' || p_id == '' || r_id == '') {
		output = 'Error: Must select valid person and role';
		message.text(output);
		message.css('color','red');
	} else {
		person.children().removeAttr('selected');
		role.children().removeAttr('selected');
		message.text('Please select a person and role - (optional)');
		var data = {'r_id':r_id,'p_id':p_id,'csrfmiddlewaretoken':csrf};

		$.post('/p_spvip/',data,function(returned){
			var model 	= returned.model
			var value 	= model.value
			var display = model.display
			var option 	= '<option value="';
			option 			+= value;
			option 			+= '" selected="selected">';
			option 			+= display;
			option 			+= '</option>';
			$('#id_vips').prepend(option);
		});
	}
}