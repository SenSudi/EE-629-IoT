$(function(){
	socket = new WebSocket("ws://" + window.location.host + "/");
	socket.onmessage = function(e) {
	    console.log(e);
	    if (/logged/.test(e.data) && !/{{user.username}}/.test(e.data)){
			$('.mailbox').append('<li class="text-center" style="border:1px solid #dad8d8"><b>'+e.data+'</b></li>');
			if ($('#mailbox-notify').closest('a').attr('aria-expanded') == false) {
				console.log('here')
				$('#mailbox-notify').addClass('notify');
			}
		}
			if ($('.mailbox').children().length > 6) {
			    $('.mailbox').children().first().remove();
			}
	}

	socket.onopen = function() {
	    socket.send("{{user.username}} logged in!");
	}

	//Call onopen directly if socket is already open
	if (socket.readyState == WebSocket.OPEN) socket.onopen();

	$(window).on('beforeunload', function(){
	    //socket.send("{{user.username}} has logged out");
	    socket.close();
	});
});