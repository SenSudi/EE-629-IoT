function codbContactAdd (obj) {
  $.get('/get_form/',{'app':'contacts','form':'ContactForm','form_id':'add-contact-form'},function(returned) {
  	var header        = "Add Contact";
    var content       = returned;
    var strSubmitFunc = "codbContactSubmit(event)";
    var btnText       = "Submit";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#modalWindow');
    var form 					= modal.find('#add-contact-form');
    form.attr('action','/add_contact/');
    form.attr('method','POST');
    formatForm();
  });
}

function codbContactSubmit (e) {
	e.preventDefault();
	var btn = $(e.target);
	var modal = btn.closest('.modal');
	var form = modal.find('#add-contact-form');
	form.ajaxSubmit(function(returned){
		$('#items').empty().html(returned);
		modal.modal('hide');
	});
}

function codbContactDetails (obj) {
  var contact = $(obj);
  var cid = contact.attr('data-item-id');
  $.get('/contact_db_details/',{'contact-id':cid},function(returned){
    var header        = "Details for "+contact.find('.first_name').text()+" "+contact.find('.last_name').text();
    var content       = returned;
    var strSubmitFunc = "";
    var btnText       = "";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal         = $('#modalWindow');
  });
}