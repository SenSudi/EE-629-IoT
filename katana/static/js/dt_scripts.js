$(document).on('click.dt','#btn-dt-add-table',function(){
  var btn = $(this);
  $.get('/table_add_form/',function(returned){
    var modal = formModal(returned);
    formatForm();
  });
});

$(document).on('click.dt','#btn-dt-table-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('form');
  var container = $(document).find('#data-tables');
  form.ajaxSubmit(function(returned){
    if (returned.success) {
        container.append(returned.element);
        modal.modal('hide');
    } else if (returned.errors) {
      populateFormErrors(form.attr('id'),returned.errors);
    } else {
        return false;
    }
  });
});

$(document).on('click.dt','#btn-add-data-type',function(){
  var btn = $(this);
  var col = btn.closest('#addon-col');
  btn.remove();
  $.get('/data_type_add_form/',function(returned){
    col.empty().html(returned);
    formatForm();
  });
});

$(document).on('click.dt','#btn-dt-label-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var col = btn.closest('#addon-col');
  var modal = btn.closest('.modal');
  var form = modal.find('#dt-create-form');
  var select = modal.find('#id_data_type');
  var attrs = modal.find('#type-attributes');
  form.ajaxSubmit(function(returned){
    if (returned.success) {
      col.empty().html('<i id="btn-add-data-type" class="btn fa fa-plus" style="font-size:25px;margin-top:27px;"></i>');
      select.append(returned.option);
      attrs.empty().html(returned.attrs);
    } else if (returned.errors) {
      populateFormErrors(form.attr('id'),returned.errors);
    }
  });
});

$(document).on('click.dt','#btn-form-cancel',function(e){
  e.preventDefault();
  var btn = $(this);
  var col = btn.closest('#addon-col');
  col.empty().html('<i id="btn-add-data-type" class="btn fa fa-plus" style="font-size:25px;margin-top:27px;"></i>');
});

$(document).on('change.dt','#id_data_type',function(){
  var select = $(this);
  var modal = select.closest('.modal');
  var attrs_div = modal.find('#type-attributes');
  var id = select.val();
  var data = {};
  data['id'] = id;
  if (id != 'none') {
    $.get('/data_type_attrs/',data,function(returned) {
      attrs_div.empty().html(returned);
    });
  }
});

$(document).on('keydown.dt','.dt-attr-name',function(e){
  var field = $(this);
  if (e.key == 'Enter' || e.key == 'Tab') {
    e.preventDefault();
    field.blur();
  }
});

$(document).on('blur.dt','.dt-attr-name',function(e){
  var field = $(this);
  var modal = field.closest('.modal');
  var id = modal.find('#id_data_type').val(); 
  var name = field.attr('data-name');
  var text = field.text();
  var data = {}
  data.name = name
  data.text = text
  data.id = id
  if (name != text) {
    $.post('/data_type_update_attr/',data,function(returned){
      if (returned.success) {
        field.attr('data-name',text);
      }
    });
  }
});

$(document).on('click.dt','#btn-manage-dts',function(){
  var btn = $(this);
  $.get('/dt_manager/',function(returned){
    var modal = detailsModal(returned);
    formatForm();
  });
});

$(document).on('click.dt','#data-type-new-attr',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var attrs = modal.find('#attrs');
  var id = modal.find('#id_data_type').val();
  var data = {};
  data.id = id;
  $.post('/data_type_add_attr/',data,function(returned){
    attrs.append(returned);
    attrs.find('[data-name="new attribute"]').empty().focus();
  });
});