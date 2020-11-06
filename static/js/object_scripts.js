function refreshObjectsContainer () {
	var objects_container 	= $(document).find('#content_paine').find('.objects-container');
	console.log(objects_container);
	var url 				= objects_container.attr('data-url');
	var data 				= {}; 
	data.where 				= $(document).find('#page-data').attr('where');
	console.log(url);
	$.get(url,data,function(returned){
		objects_container.empty().html(returned);
	});
}


function refreshObjectsContainerfile () {
	var objects_container 	= $(document).find('#content_paine').find('.report-files');
	var url                 = objects_container.attr('data-url');
	var data                = {};
	data.where 				= $(document).find('#page-data').attr('where');
 	$.get(url,data,function(returned){
		objects_container.empty().html(returned);
	});
}

function getForm (btn) {
	var url 		= btn.attr('data-url');
	$.get(url, function(returned) {
		var modal 	= formModal(returned);
		return modal;
	});
}

function highlightObject (object) {
	if (object.hasClass('selected')) {
		object.removeClass('selected');
	} else {
		object.addClass('selected');
	}
}

$(document).on('click.object','.btn-object-export',function(){
	var btn = $(this);
	var modal = btn.closest('.modal');
	var data = _getModalModelAttrs(modal);
	$.post(data.export,data,function(returned){
        $('#content_paine').load('/methodologies/');
        modal.modal('hide');
	});
});

$(document).on('click.object','.selectable',function(e){
	e.preventDefault();
	if ($(this).hasClass('object')) {
		var object = $(this);
	} else {
		var object = $(this).closest('.object');
	}
	var object_type = object.attr('data-obj-type');
	var selected = $(document).find('.selected');
	var flag = false;
	if (e.shiftKey) {
		var container = object.closest('.multi-select-container');
		if (container.length > 0) {
			var first = container.find('.selected').first();
			if (first.length == 0) {
				return false;
			} else {
				var arry = [];
				var allObjects = container.find('.object[data-obj-type="'+object_type+'"]');
				$.each(allObjects,function(){
					arry.push($(this));
				});
				var i = 0;
				var len = arry.length;
				for (;i<len;i++) {
					var currentID = arry[i].attr('data-obj-id');
					if ( currentID == first.attr('data-obj-id')) {
						var indexOfFirst = i;
					} else if (currentID == object.attr('data-obj-id')) {
						var indexOfCurrent = i;
					}
				}
				var j = indexOfFirst;
				var end = indexOfCurrent + 1;
				for (;j < end;j++) {
					arry[j].addClass('selected');
				}
				document.getSelection().removeAllRanges();
			}
		}
	} else {
		if (selected.length > 0) {
			$.each(selected,function(){
				if ($(this).attr('data-obj-id') == object.attr('data-obj-id')) {
					flag = true;
				}
			});
			if (flag) {
				selected.removeClass('selected');
			} else {
				selected.removeClass('selected');
				object.addClass('selected');
			}
		} else {
			object.addClass('selected');
		}
	}
});

$(document).on('click.object','.multi-selectable',function(e){
	e.preventDefault();
	if ($(this).hasClass('object')) {
		var object = $(this);
	} else {
		var object = $(this).closest('.object');
	}
	var object_type = object.attr('data-obj-type');

	var container = object.closest('.multi-select-container');
	var selected = $(container).find('.selected');
	selected.addClass('selected');
	object.toggleClass('selected');
});

$(document).on('click.object','.details',function(){
	var btn = $(this);
	var object = btn.closest('.object');
	var data = _getObjModelAttrs(object);
	$.get(data.details,data,function(returned){
		var modal = detailsModal(returned);
		_setModalModelAttrs(modal,data);
	});
});

$(document).on('click.it','.btn-obj-delete',function(e){
  e.preventDefault();
  var btn     = $(this);
  var object  = btn.closest('.object');
  var modal   = btn.closest('.modal');
  var data    = _getObjModelAttrs(object);
  $.post(data.delete,data,function(returned){
    if (returned.success) {
	    if (modal.length > 0) {
	    	object.remove()
	    } else {
	    	refreshObjectsContainer ();
	    }
    }
  });
});

$(document).on('click.it','.btn-obj-delete-file',function(e){
  e.preventDefault();
  var btn     = $(this);
  var object  = btn.closest('.object');
  var modal   = btn.closest('.modal');
  var data    = _getObjModelAttrs(object);
  $.post('/delete_report_file/',data,function(returned){
    if (returned.success) {
	    if (modal.length > 0) {
	    	modalRefresh(btn);
	    } else {
	    	refreshObjectsContainerfile ();
	    }
    }
  });
});

$(document).on('click.object','.btn-object-add',function(){
	var btn 	= $(this);
	var modal 	= getForm(btn);
});

$(document).on('click.object','.btn-object-add-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var form = modal.find('form');
	form.ajaxSubmit(function(returned){
		modal.modal('hide');
	});
});

$(document).on('click.object','.objects-refresh',function(){
    refreshObjectsContainer();
});

$(document).ajaxSuccess(function(event,xhr,settings){
	if (typeof(xhr.responseJSON) != 'undefined') {
		var success = xhr.responseJSON.success;
		var errors = xhr.responseJSON.errors;
		if (success) {
			if (success == 'object form success') {
				refreshObjectsContainer();
			}
		} else if (errors) {
			var form = $(event.currentTarget.forms[0]);
			populateFormErrors(form,errors);
		}
	}
});

$(document).on('click.delete','.btn-generic-delete',function(e){
	e.preventDefault();
	var btn = $(this);
	var object = btn.closest('.object');
	var id = object.attr('data-obj-id');
	var app = object.attr('data-obj-app');
	var model = object.attr('data-obj-model');
	data = {}
	data.title = object.attr('data-obj-title');
	data.model = model;
	$.get('/generic_delete_form/',data,function(returned){
		var modal = formModal(returned);
		modal.attr('data-obj-id',id);
		modal.attr('data-obj-app',app);
		modal.attr('data-obj-model',model);
	});
});

$(document).on('click.delete','#btn-generic-delete-submit',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	var id = modal.attr('data-obj-id');
	var app = modal.attr('data-obj-app');
	var model = modal.attr('data-obj-model');
	data = {}
	data['id'] = id;
	data['app'] = app;
	data['model'] = model;
	$.post('/generic_delete/',data,function(returned){
		if (returned.success && model == 'Report_Item') {
			$(document).find('[data-obj-id="'+id+'"]').remove();
			modal.modal('hide');
			$(document).find('body').removeClass('modal-open');
			$(document).find('.modal-backdrop').remove();
			$('#content_paine').load('/report_items/');
		}
		else if (returned.success) {
			$(document).find('[data-obj-id="'+id+'"]').remove();
			modal.modal('hide');
			$(document).find('body').removeClass('modal-open');
			$(document).find('.modal-backdrop').remove();
		}
	});
});

$(document).on('click.modals','#btn-modal-close',function(e){
	e.preventDefault();
	var btn = $(this);
	var modal = btn.closest('.modal');
	modal.modal('hide');
});