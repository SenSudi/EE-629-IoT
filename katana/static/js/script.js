$(function() {
	$('.side-tab').click(function() {
		$('.side-tab').removeClass('side-tab-active');
		$('#project-space').html('The text you are adding');
		$(this).addClass('side-tab-active')
	});
});