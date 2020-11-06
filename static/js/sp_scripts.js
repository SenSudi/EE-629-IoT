function scratchpad () {
  var container = $('#scratchModal');
  $.get('/scratchpad/',function(returned){
    
    container.empty().html(returned);
    
    var modal = container.find('.modal');
    var dialog = modal.find('.modal-dialog');

    modal.modal();
    modal.modal('show');
    dialog.css('width','50vw');
    dialog.css('margin-top','10vh');

    var body = modal.find('.modal-body');
    body.find('br').first().remove();
  });
}

$(document).on('click.sp','#btn-nav-scratchpad',function(){
  scratchpad();
});
  
$(document).on('input.sp','#scratch-pad-body',function(){
  var scratch = $(this)
  var modal = scratch.closest('.modal');
  var footer = modal.find('.modal-footer');
  var modified = scratch.html().replace(/<br[^>]*>/gi,'\n');
  //console.log(modified);
  var data = {'scratch': modified};
  var url = '/scratchpad_update/';
  $.post(url, data, function(returned){
    if (returned.success) {
      footer.empty().html(returned.success);
      footer.css('color','#666');
    } else if (returned.errors) {
      footer.empty().html(returned.errors);
      footer.css('color','red');
    }
  });
});

$(document).on('click.sp','.btn-scratch-text-up',function(){
  var body = $('#scratch-pad-body');
  var size = body.css('font-size');
  size.replace(/px/,'');
  var num = parseInt(size);
  body.css('font-size',num+1);
});

$(document).on('click.sp','.btn-scratch-text-down',function(){
  var body = $('#scratch-pad-body');
  var size = body.css('font-size');
  size.replace(/px/,'');
  var num = parseInt(size);
  body.css('font-size',num-1);
});