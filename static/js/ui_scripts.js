// Attach the event keypress to exclude the F5 refresh
// $(document).bind('keypress', function(e) {
// 	if (e.keyCode == 116){
// 	  // validNavigation = true;
// 	  return false
// 	}
// });

// $(document).on('contextmenu', function(e) {
// 	e.preventDefault();
// });

$(document).on('focus.ui','input[type=date]',function(){
	$(this).datepicker({dateFormat: 'yy-mm-dd'});
});

function reloadSideNav () {
	var sideNavContainer = $(document).find('.sidebar-nav');
	$.get('/display_sidenav/',function(returned){
		sideNavContainer.empty().html(returned);
		$(document).find('#side-menu').metisMenu();
	});
}

$(document).on('hidden.bs.modal', function (e) {
	var modalParent = $(e.target).parent();
	modalParent.empty();
	var backdrops = $(document).find('.modal-backdrop');
	if (backdrops.length > 1) {
		backdrops.last().remove();
	}
	var modal = $(document).find('.modal');
	if (modal.length > 0) {
		modal.focus();
		$(document).find('body').addClass('modal-open');
	}
	if (modal.length == 0) {
		$(document).find('body').removeClass('modal-open');
		$(document).find('.modal-backdrop').remove();
	}
    var transparent_modal = $(document).find('.modalTransparent');
    transparent_modal.removeClass('modalTransparent');
});


$(document).ajaxSuccess(function(event,xhr,settings){
	if (typeof(xhr.responseJSON) != 'undefined') {
		var sidenav = xhr.responseJSON.sidenav;
		if (sidenav) {
			reloadSideNav();
		}
	}
});

$(document).on('click.ui','.btn-expand-collapse',function(e){
	e.preventDefault();
	var minus 	= 'fa-minus'
	var plus 	= 'fa-plus'
	var btn 	= $(this);
	var parent 	= btn.closest('.expandable-container');
	var body	= parent.find('.expandable-body').first();
	if (btn.hasClass(plus)) {
		btn.removeClass(plus);
		btn.addClass(minus);
		body.removeClass('collapsed');
		if (!body.children().hasClass('.expandable-body')) {
			body.children().removeClass('collapsed');
		}
		body.find('.object').removeClass('collapsed');
	} else if (btn.hasClass(minus)) {
		btn.removeClass(minus);
		btn.addClass(plus);
		body.addClass('collapsed');
		if (!body.children().hasClass('.expandable-body')) {
			body.children().addClass('collapsed');
		}
	}
});

// $(document).on('dblclick.tasks',function(e){
// 	e.preventDefault();
// 	e.stopPropagation();
// 	console.log(e);
// });

// $(document).on('dblclick.wf',function(e){
// 	e.preventDefault();
// 	e.stopPropagation();
// 	console.log(e);
// });

// $(document).on('click.tasks',function(e){
// 	e.preventDefault();
// 	console.log(e);
// });