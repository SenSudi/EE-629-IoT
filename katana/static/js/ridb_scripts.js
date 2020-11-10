function attrSortChange (e,ui) {
  var attrs = $(ui.item[0]).parent().find('.attr');
  var modal = attrs.closest('.modal');
  var id = modal.find('#id_item_type').val();
  updateAttrOrder(id,attrs);
}

function updateAttrOrder (type_id,attr) {
  var order = [];
  var data = {};
  $.each(attr,function(){
    var name = $(this).find('.attr-name').text();
    order.push(name);
  });
  data.order = order;
  data.id = type_id;
  $.post('/type_attr_update/',data,function(returned){
    console.log(returned);
  });
}

function initSortableAttrs () {
  $(document).find('#attrs').sortable({
    revert: true,
    items: '.attr',
    tolerance: 'pointer',
    // container: 'parent',
    stop: attrSortChange
  });
}

$(document).on('dblclick','.attr-name',function(e){
  e.preventDefault();
  var attr = $(this);
  attr.focus();
});

$(document).on('click.ridb','#btn-manage-item-attrs',function(){
  var btn = $(this);
  $.get('/ridb_manager/',{'no_val':true},function(returned){
    var modal = detailsModal(returned);
    modal.attr('data-no-val','true');
    modal.find('.modal-content').css('min-height', '240px')
  });
});

$(document).on('change','#id_item_type',function(){
  var select = $(this);
  var modal = select.closest('.modal');
  var attrs_div = modal.find('#type_attributes');
  var id = select.val();
  var data = {}
  data.id = id;
  if (modal.attr('data-no-val')) {
    data.no_val = true;
  }
  if (modal.attr('data-form-val')) {
    data.form_val = true;
  }
  if (window.where == 'Report Items DB' && id != 'none') {
    $.get('/item_type_attrs/',data,function(returned) {
      attrs_div.empty().html(returned);
      if (modal.attr('data-no-val')) {
        if (modal.find('.attr').length > 0) {
          initSortableAttrs();
        }
      }
    });
  }
});

$(document).on('keydown','.attr-name',function(e){
  var field = $(this);
  if (e.key == 'Enter' || e.key == 'Tab') {
    e.preventDefault();
    field.blur();
  }
});

$(document).on('blur','.attr-name',function(e){
  var field = $(this);
  var modal = field.closest('.modal');
  var attrs = modal.find('.attr');
  var id = modal.find('#id_item_type').val();
  var name = field.attr('data-name');
  var text = field.text();
  var aid  = field.closest('#report-item-type').children().attr('id');
  var data = {}
  data.name = name
  data.text = text
  data.id = id
  data.aid = aid
  if (name != text) {
    $.post('/item_type_update_attr/',data,function(returned){
      updateAttrOrder(id,attrs);
    });
  }
});

function inputTypeUpdate(e){
  var field = $(e);
  var modal = field.closest('.modal');
  var attrs = modal.find('.attr');
  var id = modal.find('#id_item_type').val();
  var input_type = field.parent().find(':selected').text();
  var aid  = field.closest('#report-item-type').children().attr('id');
  var data = {}
  data.input_type = input_type
  data.id = id
  data.aid = aid
  $.post('/item_type_update_attr/',data,function(returned){
    updateAttrOrder(id,attrs);
  });
};

$(document).on('click', '.btn-item-type-delete', function() {
    var btn = $(this);
    var modal = btn.closest('.modal');
    var id    = modal.find('#id_item_type').val();
    $.post('/item_type_delete/',{'id':id}, function(returned) {
        $('#content_paine').load('/report_items/');
        var modal = detailsModal(returned);
        modal.attr('data-no-val','true');
    })
});


$(document).on('blur','.attr-value',function(){
  var field = $(this);
  var modal = field.closest('.modal');
  var id    = modal.find('#item_id').val();
  var value = field.html().replace(/<br[^>]*>/gi,'\n').replace(/<div[^>]*>/gi,'\n').replace(/<\/div[^>]*>/gi,'');
  var name  = field.parent().find('.attr-name').text();
  var data  = {};
  data.name = name;
  data.value = value;
  data.id   = id;
  if (id) {
    $.post('/ri_update_attr/',data,function(returned){
      // console.log(returned);
    });
  }
});

$(document).on('click.ridb','#item_type_new_attr',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var attrs = modal.find('#attrs');
  var id = modal.find('#id_item_type').val();
  var data = {};
  data.id = id;
  if (modal.attr('data-no-val')) {
    data.no_val = true;
  }
  $.post('/item_type_add_attr/',data,function(returned){
    attrs.append(returned);
    var new_attr = attrs.find('.attr').last().find('.attr-name');
    new_attr.empty().focus();
    initSortableAttrs();
  });
});

$(document).on('click.ridb','.btn-type-attr-delete',function(e){
  e.preventDefault();
  var btn = $(this);
  var attr = btn.closest('.attr');
  var id = attr.attr('data-obj-id');
  var app = attr.attr('data-obj-app');
  var model = attr.attr('data-obj-type');
  var name = attr.attr('data-name');
  var data = {};
  data.id = id;
  data.app = app;
  data.model = model;
  data.name = name;
  var attrName = attr.find('.attr-name');
  var container = btn.parent();
  attrName.addClass('col-xs-7');
  attrName.removeClass('col-xs-12');
  container.addClass('col-xs-3');
  container.removeClass('col-xs-1');
  $.get('/type_attr_delete_check/',data,function(returned){
    container.empty().html(returned);
    container.css('padding','8px');
  });
});

$(document).on('click.ridb','.btn-type-attr-delete-confirm',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var attr = btn.closest('#report-item-type');
  var type_id = modal.find('#id_item_type').val();
  var id = attr.attr('data-obj-id');
  var app = attr.attr('data-obj-app');
  var model = attr.attr('data-obj-type');
  var name = attr.attr('data-value');
  var aid  = btn.closest('#report-item-type').children().attr('id');
  var data = {};
  data.id = id;
  data.app = app;
  data.aid = aid;
  data.model = model;
  data.name = name;
  $.post('/type_attr_delete/',data,function(returned){
    if (returned.success) {
      btn.closest('#report-item-type').remove();
      updateAttrOrder(type_id, modal.find('#report-item-type'));
    }
  });
});

$(document).on('click.ridb','.btn-type-attr-delete-cancel',function(e){
  e.preventDefault();
  var btn = $(this);
  var attr = btn.closest('.attr');
  var attrName = attr.find('.attr-name');
  var container = attr.find('.attr-misc');
  container.empty();
  attrName.addClass('col-xs-12');
  attrName.removeClass('col-xs-7');
  container.addClass('col-xs-1');
  container.removeClass('col-xs-3');
  container.html('<i class="btn fa fa-trash btn-type-attr-delete" style="color:red;font-size:16px;position:relative;"></i>');
  container.css('padding','7px');
});

function ridbItemAdd () {
  $.get('/report_item_form/',function(returned){
    var header        = "Add Report Item";
    var content       = returned;
    var strSubmitFunc = "ridbItemSubmit(this)";
    var btnText       = "Add Item";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    $('#modalWindow').find('#btn-modal-form-submit').attr('id','btn-modal-add-item');
    var modal         = $('.modal');
    var form          = modal.find('form');
    modal.attr('data-form-val',true);
    formatForm();
  });
}

function ridbItemSubmit (obj) {
  var btn        = $(obj)
  var modal      = btn.closest('.modal');
  var form       = modal.find('form');
  var data       = {};
  var attrs_val  = [], attrs_name = [], attrs_seq = [], attrs_type = [];
  var attr_count = modal.find('.form-group').length;
  var i;
  data.title     = modal.find('#id_Title')[0].value.trim();
  for (i=2; i < attr_count; i++ ){
    attrs_val.push(jQuery(modal.find('.input-group-addon').siblings()[i]).val());
    attrs_name.push(jQuery(modal.find('.input-group-addon').siblings()[i]).attr('name'));
    attrs_type.push(jQuery(modal.find('.input-group-addon').siblings()[i]).attr('data-obj-type'));
    attrs_seq.push(jQuery(modal.find('.input-group-addon').siblings()[i]).attr('data-obj-seq'));
  }
  data.values   = attrs_val;
  data.names    = attrs_name;
  data.type     = attrs_type;
  data.seq      = attrs_seq;
  if (modal.find('#id_item_type').val().length > 0){
    var options = {
      data:data,
      success:  function(){
                  $('#content_paine').load('/report_items/');
                  modal.modal('hide');
                }
    };
    form.ajaxSubmit(options);
  } else {
    form.prepend('<b style="color:red;">Please fill out required fields</b>');
  }
}

function ridbItemDetails (obj) {
  var item          = $(obj).closest('.object');
  var ri            = {}
  ri.title          = item.find('.item-title').text().trim();
  ri.description    = item.find('.item-description').text().trim();
  ri.type           = item.find('.item-type').attr('id');
  ri.id             = item.attr('id');
  $.get('/report_item_update_form/',{'id':ri.id,'selected':ri.type},function(returned){
    var header        = "Update report item <b>"+ri.title+"</b>";
    var content       = returned;
    var strSubmitFunc = "ridbItemUpdate(this)";
    var btnText       = "Update Item";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal = $('#modalWindow');
    modal.attr('data-form-val',true);
    modal.find('#item_id').val(ri.id);
    formatForm();
  });
}

function ridbItemUpdate (obj) {
  var btn = $(obj);
  var modal = btn.closest('.modal');
  var form = modal.find('form');
  var data       = {};
  var attrs_val  = [], attrs_name = [];
  var attr_count = modal.find('.form-group').length;
  var report_id  = modal.find('#type_attributes').attr('name');
  var type_id    = jQuery(modal.find('.input-group-addon').siblings()[0]).val();
  var i;
  data.title     = modal.find('#id_Title')[0].value.trim();
  data.report_id = report_id;
  data.type_id   = type_id;
  for (i=2; i < attr_count; i++ ){
    attrs_val.push(jQuery(modal.find('.input-group-addon').siblings()[i]).val());
    attrs_name.push(jQuery(modal.find('.input-group-addon').siblings()[i]).attr('name'));
  }
  data.values = attrs_val;
  data.names  = attrs_name;
  var options = {
      data:data,
      success:  function(){
                  $('#content_paine').load('/report_items/');
                  modal.modal('hide');
                }
      };
  form.ajaxSubmit(options);
}

function ridbItemTypeAdd (obj) {
  var btn = $(obj);
  var col = btn.closest('#addon-col');
  btn.remove();
  col.append('<form method="POST" action="/create_item_type/"><div class="form-group"><label for="new-item-type">Create New Item Type</label><span id="errors" style="margin-left:10px;"></span><div class="input-group"><div class="input-group-addon"></div><input type="text" name="new-item-type" class="form-control" style="width:80%;" placeholder="Item type label.." id="new-item-type"><button onclick="ridbItemTypeSubmit(event)" class="btn btn-success" id="btn-submit-item-type" style="font-size:17px;">Create</button></div></div></form>');
  formatForm();
}

function ridbItemTypeSubmit (e) {
  e.preventDefault();
  var btn               = $(e.target);
  var col               = btn.closest('#addon-col');
  var form_group        = btn.closest('.form-group');
  var input             = form_group.find('input');
  var value             = input.val();
  var form              = col.find('form');
  var modal             = btn.closest('.modal');
  var select            = modal.find('#id_item_type');
  form.ajaxSubmit(function(returned){
    if (returned['success']) {
      var labels    = returned['success'];
      var item_type = col.closest('.row').find('#id_item_type');
      item_type.empty().append('<option value="">---------</option>')
      for (label in labels){
        if (labels[label] == value) {
          item_type.append('<option value="'+label+'" selected="selected">'+labels[label]+'</option>');
        } else {
          item_type.append('<option value="'+label+'">'+labels[label]+'</option>');
        }
      }
      col.empty().append('<i class="btn fa fa-plus" style="font-size:25px;margin-top:27px;" id="btn-add-item-type"></i>');
    }
    else if (returned['errors']) {
      var errors    = col.find('#errors');
      errors.append('<b style="color:red">'+returned['errors']+'</b>')
    }
    var id = select.val();
    if (window.where == 'Report Items DB' && id != 'none') {
      var attrs_div = modal.find('#type_attributes');
      var data = {};
      data.id = id;
      if (modal.attr('data-no-val')) {
        data.no_val = true;
      }
      if (modal.attr('data-form-val')) {
        data.form_val = true;
      }
      $.get('/item_type_attrs/',data,function(returned) {
        attrs_div.empty().html(returned);
      });
    }
  });
}

function ridbItemFilterSubmit(e) {
    var btn           = $(e.target);
    var type_select   = $('#item-type-filter');
    var items_per_page= $('#items-per-page');
    var search_string   = $('#input-search-items');
    var data          = {};
    data['items_per_page']= items_per_page.find(':selected').val();
    data['items_per_page_id']= items_per_page.find(':selected').attr('id');
    data['item_type'] = type_select.find(':selected').val();
    data['item_id']   = type_select.find(':selected').attr('id');
    data['search_string'] = search_string.val();
    data['exact_match'] = $('#chk-exact-match').is(':checked');
    $.get('/report_items_filter/',data,function(returned){
        $('.items-box').empty().html(returned);
    });
}

function ridbItemPage(e) {
    var btn           = $(e.target);
    var type_select   = $('#item-type-filter');
    var page          = btn.attr('id');
    var items_per_page= $('#items-per-page');
    var search_string   = $('#input-search-items');
    var data          = {};
    data['items_per_page']= items_per_page.find(':selected').val();
    data['items_per_page_id']= items_per_page.find(':selected').attr('id');
    data['page']      = page;
    data['item_type'] = type_select.find(':selected').val();
    data['item_id']   = type_select.find(':selected').attr('id');
    data['search_string'] = search_string.val();
    data['exact_match'] = $('#chk-exact-match').is(':checked');
    $.get('/report_items_filter/',data,function(returned){
        $('.items-box').empty().html(returned);
    });
}
// $(document).on('click','#btn-add-item',function(){
//     var form = $('#add-item-form');
//     var data = form.serializeArray();
//     var trans = {}
//     $.each(data,function(idx,val){
//         var name = $(this)[0]['name'];
//         var info = $(this)[0]['value'];
//         trans[name] = info;
//     });
//     trans['csrfmiddlewaretoken'] = '{{csrf_token}}';
//     var url = '/report_items/';
//     $.post(url,trans,function(returned){
//         $('.items-box').empty().html(returned);
//         form.trigger('reset');
//     });
// });

function searchBarItems (obj) {
    var search = $(obj).val();
    var items_per_page= $('#items-per-page');
    var type_select   = $('#item-type-filter');
    var search_string   = $('#input-search-items');
    data = {};
    data['items_per_page']= items_per_page.find(':selected').val();
    data['items_per_page_id']= items_per_page.find(':selected').attr('id');
    data['item_type'] = type_select.find(':selected').val();
    data['item_id']   = type_select.find(':selected').attr('id');
    data['search_string'] = search_string.val();
    data['exact_match'] = $('#chk-exact-match').is(':checked');
    $.get('/report_items_filter/',data,function(returned){
        $('.items-box').empty().html(returned);
    });
}

$(document).on('click.ridb', '#btn-manage-static-attr', function() {
    $.get('/manage_static_attr/',function(returned){
       attributeModal(returned)
    });
});

$(document).on('click', '#btn-add-static-attr', function(e){
    var btn = $(this);
    var parent = btn.parent();
    $.get('/static_attr_form/',function(returned){
        parent.empty().html(returned);
    });
})

$(document).on('click.ridb','#new_static_attr_item',function(){
    var btn = $(this);
    var list = btn.parent().find('#attr_list_items');
    $.get('/static_attr_add_item/', function(returned) {
        list[0].insertAdjacentHTML('beforeend', returned);
    });
});

$(document).on('click.ridb','#static-attr-submit', function(){
    var btn = $(this);
    var modal = btn.closest('.modal');
    data = {};
    data.id = modal.find('.static-attr-details').attr('id');
    data.title = $('input[name$="title"]').val();
    data.values = [];
    $.each($("input[name='list-item']"), function () {
            data.values.push($(this).val());
    });
    $.post('/static_attr_save/', data, function(returned) {
        modal.find('.modal-content').html(returned)
    })
})

$(document).on('click.ridb','.static-attr-cancel', function(){
    var btn = $(this);
    var details = btn.closest('.modal').find('#attr-details')
    details.empty().html('<button id="btn-add-static-attr" class="btn btn-success waves-effect waves-light m-r-10" style="float:left">New Attributes</button>')
});

$(document).on('click.ridb', '#static-attr-row', function() {
    var attr = $(this);
    var id = attr.attr('attr-id');
    var details = attr.closest('.modal').find('#attr-details')
    $.get('/static_attr_form/',{'id':id},function(returned){
        details.empty().html(returned);
    });
})

$(document).on('click.ridb', '.static-attr-item-delete', function() {
    var btn = $(this);
    var field = btn.closest('#static-field');
    field.remove();
});

$(document).on('click.ridb', '.static-attr-delete', function() {
    var btn = $(this);
    var modal = btn.closest('.modal');
    var attr = btn.closest('#static-attr-row');
    var id = attr.attr('attr-id');
    $.post('/static_attr_delete/',{'id':id}, function(returned){
        modal.find('.modal-content').html(returned)
    })
    return false;
});

$(document).on('click.ridb', '#assign_static_attr', function() {
    var btn = $(this);
    var modal = btn.closest('.modal');
    var id    = modal.find('#id_item_type').val();
    $.get('/display_static_attrs/', function(returned){
        var modal = formItemModal(returned);
        modal.find('#type_id').val(id);
    });
})

$(document).on('click.ridb', '#static-attr-assign', function() {
    var btn = $(this);
    var modal = btn.closest('.modal');
    var attrs = $('#attrs');
    var id = $('#id_item_type').val();
    var staticAttrs = $('#static-attrs')
    var data = {};
    data.id = id;
    data.static = true;
    data.staticAttrId = staticAttrs.find(':selected').val();
    data.no_val = true;
    $.post('/item_type_add_attr/',data,function(returned){
        attrs.append(returned);
        modal.modal('hide');
        initSortableAttrs();
    });
});
