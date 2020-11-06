$(document).on('click.user','#top-nav-user-menu-profile',function(e){
	e.preventDefault();
	var link = $(this);
	var data = _getObjModelAttrs(link);
	var url = link.attr('href');
	$.get(url,data,function(returned){
		var modal = profileModal(returned);
		formatForm();
	});
});

$(document).on('click.user','#btn-modal-user-password-change',function(e){
	e.preventDefault();
	$.get('/change_pass/',function(returned){
		var modal = noteDetailsModal(returned);
		formatForm();
	});
});

$(document).on('blur.user','#form-change-pass #id_old_password',function(){
	var old = $(this);
	var form = old.closest('#form-change-pass');
	var error_field = old.closest('.form-group').find('.field-errors');
	if (old.val() != null) {
		$.post('/change_pass/',{'check_old':true,'old':old.val()},function(returned){
			if (returned.success) {
				error_field.empty().html('<i class="fa fa-check" style="color:green;"></i>');
			} else if (returned.errors) {
				populateFormErrors(form,returned.errors);
			}
		});
	}
});

$(document).on('click.user','#btn-save-new-pass',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var form = modal.find('#form-change-pass');
	form.ajaxSubmit(function(returned){
		if (returned.success) {
			window.location.replace("/login/");
		} else if (returned.errors) {
			populateFormErrors(form,returned.errors);
		}
	});
});

$(document).on('click.user','#btn-update-profile',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var form = modal.find('#profile-form');
	form.ajaxSubmit(function(returned){
		$('#form-messages').empty();
		for (var name in returned) {
        	if (/error/i.test(name)) {
            	$('#form-messages').append('<p style="color:red">'+returned[name]+'</p>');
        	} else {
            	$('#form-messages').append('<p style="color:green">'+returned[name]+'</p>');
          	}//end if-else
        }//end for
	});
});
