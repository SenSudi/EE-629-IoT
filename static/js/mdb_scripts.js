function unSelectAll() {
  $(document).find('.selected').removeClass('selected');
}

function getSelected() {
  var selected = $(document).find('.selected');
  unSelectAll();
  return selected;
}

function filterPTs () {
  var select = $(document).find('#mdb-pt-filter');
  var option = select.find(':selected');
  var pts    = $(document).find('.project_type');
  var tree   = $(document).find('#mdb-method-tree');
  var showing = $(document).find('#showing');
  var spacer = tree.find('.mdb-spacer');
  tree.find('.expandable-body').addClass('collapsed');
  tree.find('.mdb-project-type-container').removeClass('collapsed');
  tree.find('.mdb-project-type-container').removeClass('filtered');
  if (option.val() == 'all') {
    tree.find('.mdb-project-type-container').removeClass('collapsed');
    tree.find('.mdb-project-type-container').removeClass('filtered');
    showing.text('All Project Types + Unassociated Methods');
    spacer.css('display','block');
  } else {
    $.each(pts,function(){
      var pt = $(this);
      if (pt.attr('data-obj-id') != option.val()) {
        pt.closest('.mdb-project-type-container').addClass('collapsed');
        pt.closest('.mdb-project-type-container').addClass('filtered');
      }
    });
    spacer.css('display','none');
    showing.text(option.text());
  }
}

$(document).on('click.mdb','#btn-mdb-import',function(){
  $.get('/import_pt_form/',function(returned){
    var heading       = '';
    var content       = returned;
    var strSubmitFunc = '';
    var btnText       = '';
    alertModal('alertModal',heading,content,strSubmitFunc,btnText);
    var confirmModal  = $(document).find('#alertModal').find('.modal');
    // _setModalModelAttrs(confirmModal,data);
    confirmModal.addClass('modalTransparent');
    formatForm();
  });
});

$(document).on('click.mdb','#btn-submit-import-file',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('form');
  form.ajaxSubmit(function(returned){
    console.log(returned);
    if (returned.success){
      modal.modal('hide');
      mdbRefreshTree();
    }
  });
});

$(document).on('change.mdb','#mdb-pt-filter',function(){
  filterPTs();  
});

function resetFilters(){
  filterPTs();
  executeSearch();
}

$(document).on('click.mdb','.btn-mdb-reset-filters',function(){
  resetFilters();
});

$(document).on('click.mdb','.btn-mdb-show-recommended',function(){
  var recommended = $(document).find('.recommended');
  if (recommended.length > 0) {
    hideTree();
    $.each(recommended,function(){
      var method = $(this);
      exposeMethod(method);
    });
  }
});

$(document).on('click.mdb','#btn-mdb-expand-all',function(){
  var btn = $(this);
  var text = btn.text();
  var container = $(document).find('#mdb-method-tree');
  if (text == 'Expand') {
    var hidden = container.find('.collapsed');
    $.each(hidden,function(){
      var item = $(this);
      if (!item.closest('.mdb-project-type-container').hasClass('filtered')){
        item.removeClass('collapsed');
      }
    });
    btn.text('Collapse')
  } else if (text == 'Collapse') {
    container.find('.expandable-body').addClass('collapsed');
    btn.text('Expand');
  }
});


function exposePhase (result) {
  var parentPhaseContainer = result.closest('.mdb-phases-container');
  var parentProjectTypeContainer = result.closest('.mdb-project-type-container');
  result.removeClass('collapsed');
  result.closest('.expandable-container').removeClass('collapsed');
  parentPhaseContainer.removeClass('collapsed');
  if (!parentProjectTypeContainer.hasClass('filtered')) {
    parentProjectTypeContainer.removeClass('collapsed');
  }
}

function exposeMethod (result) {
  var resultContainer = result.closest('.mdb-methods-container');
  var parentPhaseContainer = result.closest('.mdb-phases-container');
  var parentProjectTypeContainer = result.closest('.mdb-project-type-container');
  result.removeClass('collapsed');
  resultContainer.removeClass('collapsed');
  parentPhaseContainer.removeClass('collapsed');
  result.closest('.expandable-container').removeClass('collapsed');
  result.closest('.expandable-container').find('.phase').removeClass('collapsed');
  if (!parentProjectTypeContainer.hasClass('filtered')) {
    parentProjectTypeContainer.removeClass('collapsed');
  }
}

function hideTree () {
  var allPTs = $(document).find('.mdb-project-type-container');
  var allPhases = $(document).find('.phase');
  var phaseContainers = $(document).find('.mdb-phases-container');
  var allMethods = $(document).find('.method');
  var methodContainers = $(document).find('.mdb-methods-container');
  allPTs.addClass('collapsed');
  allPhases.addClass('collapsed');
  phaseContainers.addClass('collapsed');
  allMethods.addClass('collapsed');
  methodContainers.addClass('collapsed');
}

function exposeSearchResults () {
  var results = $(document).find('.searchResult');
  hideTree();
  $.each(results,function(){
    var result = $(this);
    if (result.hasClass('method')) {
      exposeMethod(result);
    } else if (result.hasClass('phase')) {
      exposePhase(result);
    } else if (result.hasClass('project_type')) {
      if (!result.closest('.mdb-project-type-container').hasClass('filtered')) {
        result.closest('.mdb-project-type-container').removeClass('collapsed');
      }
    }
  });
}

function executeSearch () {
  var input       = $('#input-search');
  var value       = input.val();
  var tree        = $(document).find('#mdb-method-tree');
  var objects     = tree.find('.object');
  var resultText  = '';
  var output      = $('#search-output');
  var resultCount = 0;
  output.empty();
  output.parent().find('b').remove();
  output.parent().find('hr').remove();
  if (value != '') {
    var options   = {
      ignoreCase: $('#chk-ignore-case').is(':checked'),
      revealResults: $('#chk-reveal-results').is(':checked')
    };
    if (options.ignoreCase) {
      var re      = new RegExp(value,'i');
    }
    $.each(objects,function(){
      var object  = $(this);
      if (re.test(object.text())) {
        if (!object.closest('.mdb-project-type-container').hasClass('filtered')){
          if (options.revealResults) {
            object.addClass('searchResult');
          }
          output.append('<li>'+object.text()+'</li>');
          resultCount += 1;
        }
      } else {
        object.removeClass('searchResult');
      }
    });
    if (options.revealResults) {
      exposeSearchResults();
    }
    output.parent().prepend('<hr class="modal-divider" style="margin:2px 0 2px 0;">')
    output.parent().prepend('<b>'+resultCount+' Results</b>');
  } else {
    tree.find('.searchResult').removeClass('searchResult');
    filterPTs();
  }
}

$(document).on('keyup.mdb','#input-search',function(e){
  executeSearch();
});

function mdbRefreshTree (){
  $.get('/method_data_tree/',function(returned){
    $(document).find('#mdb-method-tree').empty().html(returned);
    filterPTs();
  });
}

// PTYPE SCRIPTS
$(document).on('click.mdb','#btn-mdb-add-ptype',function(){
  var btn = $(this);
  $.get('/db_ptype_add_form/',function(returned){
    var modal = formModal(returned);
    formatForm();
  });
});

$(document).on('click.mdb','#btn-modal-ptype-add-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-db-add-ptype');
  form.ajaxSubmit(function(returned){
    if (returned.errors) {
      populateFormErrors(form,returned.errors);
    } else if (returned.success) {
      mdbRefreshTree();
      modal.modal('hide');
    }
  });
});

$(document).on('click.mdb','.project_type .click',function(e){
  e.preventDefault();
  var click   = $(this);
  var object  = click.closest('.object'); 
  var data = _getObjModelAttrs(object);
  $.get(data.details,data,function(returned){
    var modal = detailsModal(returned);
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.mdb','#db-modal-ptype-edit',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  $.get('/db_ptype_edit_form/',data,function(returned){
    modal.find('.modal-content').empty().html(returned);
    formatForm();
  });
});

$(document).on('click.mdb','#btn-ptype-update',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-db-update-ptype');
  var data = _getModalModelAttrs(modal);
  var options = {
    data:data,
    success: function(returned) {
      if (returned.errors) {
        var errors = returned.errors;
        populateFormErrors(form,errors);
      } else if (returned.success) {
        mdbRefreshTree();
        $.get(data.details,data,function(details){
          modal.find('.modal-content').empty().html(details);
        });
      }
    }
  }
  form.ajaxSubmit(options);
});

// END PTYPE
//#############################################################################
// PHASE SCRIPTS //
//#################
$(document).on('click.mdb','#btn-mdb-add-phase',function(){
  var btn = $(this);
  var selected = getSelected();
  var data = {};
  data.id = []
  var i=0;
  selected.each(function(){
    data.id[i]=parseInt($(this).attr('data-obj-id'));
    i++;
  });
  $.get('/db_phase_add_form/',data,function(returned){
    var modal = formModal(returned);
  });
});

$(document).on('click.mdb','#btn-modal-phase-add-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-db-add-phase');
  form.ajaxSubmit(function(returned){
    if (returned.errors) {
      //console.log(returned.errors);
      populateFormErrors(form,returned.errors);
    } else if (returned.success) {
      mdbRefreshTree();
      modal.modal('hide');
    }
  });
});

$(document).on('click.mdb','#btn-modal-phase-add-cancel, #btn-phase-update-cancel, #btn-ptype-update-cancel, .btn-modal-cancel',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  modal.modal('hide');
});

$(document).on('click.mdb','.mdb-p-title .click, .phase-title',function(e){
  e.preventDefault();
  var click   = $(this);
  var object  = click.closest('.object');
  var data    = _getObjModelAttrs(object);
  $.get(data.details,data,function(returned){
    var modal = detailsModal(returned);
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.mdb','#modal-phase-prev-ancestor,#modal-phase-next-descendant',function(){
  var btn   = $(this);
  var modal = btn.closest('.modal');
  var data  = _getObjModelAttrs(btn);
  if (data.relative) {
    data.id = data.relative
    $.get('/db_phase_details/',data,function(returned){
      modal.find('.modal-content').empty().html(returned);
    });
  } else {
    return false;
  }
});

$(document).on('click.mdb','#btn-modal-phase-recommend-approve',function(){
  var btn   = $(this);
  var modal = btn.closest('.modal');
  var data  = _getObjModelAttrs(btn);
  $.post('/db_phase_approve/',data,function(returned){
    if (returned.success) {
      mdbRefreshTree();
      $.get('/db_phase_details/',data,function(details){
        modal.find('.modal-content').empty().html(details);
      });
    }
  })
});

$(document).on('click.mdb','#btn-modal-phase-recommend-decline',function(){
  var btn   = $(this);
  var modal = btn.closest('.modal');
  var data  = _getObjModelAttrs(btn);
  var ancestor = modal.find('#modal-phase-prev-ancestor').attr('data-obj-relative-id');
  $.post('/db_phase_decline/',data,function(returned){
    if (returned.success) {
      mdbRefreshTree();
      $.get('/db_phase_details/',{'id':ancestor},function(details){
        modal.find('.modal-content').empty().html(details);
      });
      $('#methodologies').find('.notify').remove();
    }
  })
});

$(document).on('click.mdb','.db-modal-phase-method, .db-modal-content-link',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getObjModelAttrs(btn);
  data.url = btn.attr('data-url');
  $.get(data.url,data,function(returned){
    modal.find('.modal-content').empty().html(returned);
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.mdb','#db-modal-phase-edit',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  $.get('/db_phase_edit_form/',data,function(returned){
    modal.find('.modal-content').empty().html(returned);
    formatForm();
  });
});

$(document).on('click.mdb','#btn-phase-update',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-db-phase-update');
  var data = _getModalModelAttrs(modal);
  var options = {
    data:data,
    success: function(returned) {
      if (returned.errors) {
        var errors = returned.errors;
        populateFormErrors(form,errors);
      } else if (returned.success) {
        mdbRefreshTree();
        $.get(data.details,data,function(details){
          modal.find('.modal-content').empty().html(details);
        });
      }
    }
  }
  form.ajaxSubmit(options);
});

// END PHASE

// METHOD SCRIPTS
$(document).on('click.mdb','#btn-mdb-add-method',function(){
  var btn = $(this);
  var selected = $(document).find('.selected');
  var data = {};
  data.id = []
  var i=0;
  selected.each(function(){
    data.id[i]=parseInt($(this).attr('data-obj-id'));
    i++;
  });
  $.get('/db_method_add_form/',data,function(returned){
    var modal = formModal(returned);
  });
});

$(document).on('click.mdb','#btn-modal-method-add-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-db-add-method');
  form.ajaxSubmit(function(returned){
    if (returned.errors) {
      console.log(returned.errors);
      populateFormErrors(form,returned.errors);
    } else if (returned.success) {
      mdbRefreshTree();
      modal.modal('hide');
    }
  });
});

$(document).on('click.mdb','.mdb-m-title .click, .method-title',function(e){
  e.preventDefault();
  var click   = $(this);
  var object  = click.closest('.object');
  var data    = _getObjModelAttrs(object);
  $.get(data.details,data,function(returned){
    var modal = detailsModal(returned);
    _setModalModelAttrs(modal,data);
  });
});

$(document).on('click.mdb','#db-modal-method-edit',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  $.get('/db_method_edit_form/',data,function(returned){
    modal.find('.modal-content').empty().html(returned);
    formatForm();
  });
})

$(document).on('click.mdb','#btn-method-update',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-db-method-update');
  var data = _getModalModelAttrs(modal);
  var options = {
    data:data,
    success: function(returned) {
      if (returned.errors) {
        var errors = returned.errors 
        populateFormErrors(form,errors);
      } else if (returned.success) {
        mdbRefreshTree();
        $.get(data.details,data,function(details){
          modal.find('.modal-content').empty().html(details);
        });
      }
    }
  }
  form.ajaxSubmit(options);
});

$(document).on('click.mdb','#btn-modal-method-recommend-approve',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  $.post('/db_method_approve/',data,function(returned){
    if (returned.success) {
      modalRefresh(btn);
      mdbRefreshTree();
    }
  });
});

$(document).on('click.mdb','#btn-modal-method-recommend-decline',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  $.post('/db_method_decline/',data,function(returned){
    if (returned.declined) {
      mdbRefreshTree();
      modal.modal('hide');
    }
  });
});

function methodDeployConfirm (data) {
  $.get('/open_projects_checklist/',function(returned){
    var heading       = '';
    var content       = returned;
    var strSubmitFunc = 'closeAlertModal(this)';
    var btnText       = 'close';
    alertModal('alertModal',heading,content,strSubmitFunc,btnText);
    var confirmModal  = $(document).find('#alertModal').find('.modal');
    _setModalModelAttrs(confirmModal,data);
    confirmModal.find('.modal-footer').append('<button class="btn btn-warning btn-method-deploy-submit">deploy</button>'); 
    confirmModal.addClass('modalTransparent');
  });
}

$(document).on('click.mdb','.btn-method-deploy',function(){
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  methodDeployConfirm(data);
});

$(document).on('click.mdb','.btn-method-deploy-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var data = _getModalModelAttrs(modal);
  data.projects = modal.find('input:checked').map(function(){return parseInt($(this).val())}).get();
  data.projects = data.projects.filter(function(n){ return(!isNaN(parseInt(n))) });
  $.post('/db_method_deploy/',data,function(returned){
    if (returned.success) {
      modal.modal('hide');
      modalRefresh($(document).find('#detailsModal').find('.modal-ctrl-refresh'));
    }
  });
});

function Phase_reorder_update(){
    $(document).find('.mdb-phases-container').sortable({
        revert: true,
        items: '.phase',
        tolerance: 'pointer',
        container: 'parent',
        stop: ptypephaseSortChange
    });
}

function ptypephaseSortChange(e,ui) {
    var phases =$(ui.item[0]).closest('.mdb-phases-container').find('.phase');
    $.each(phases,function(index) {
        var id = $(this).attr('data-obj-id');
        $.post('/phase_update/',{'id':id,'seq':index},function(returned){
            if (returned.error){
                console.log(returned.error);
            }
        });
    });
}

function ptype_step() {
    $(document).find('#ptype-sortable').sortable({
        revert: true,
        items: '.ptype-method',
        tolerance: 'pointer',
        container: 'parent',
        draggable: 'true',
        stop: ptypeSortChange
    });
}

function ptypeSortChange (e,ui) {
  var ptype = $(ui.item[0]).closest('#ptype-sortable').find('.ptype-method');
  $.each(ptype,function(index) {
    var id = $(this).attr('data-obj-id');
    $.post('/ptype_reorder_update/',{'id':id,'seq':index},function(returned) {
        if (returned.error) {
            console.log(returned.error);
        }
    });
  });
}

function method_step() {
    $(document).find('.mdb-methods-container').sortable({
        revert: true,
        items: '.method-id',
        tolerance: 'pointer',
        draggable: 'true',
        stop: methodSortChange
    });
}

function methodSortChange (e,ui) {

  var method = $(ui.item);
  data = {};
  data.id = method.attr('data-obj-id');
  data.projectTypeId = method.attr('project-type-id');
  data.phaseId = method.attr('phase-id');
  data.sequence = method.index() + 1; // index starts from 0 where as the application should store it from 1
  debugger;
  $.post('/method_reorder_update/',data,function(returned){
        if (returned.error) {
            console.log(returned.error);
        }
    });
}

$(document).on('change.tm','#method-add-phase-select',function(e){
    e.preventDefault();
    var select = $(this);
    var modal = select.closest('.modal');
    var selected = $(document).find('.selected');
    var data = {};
    data.id = [select.find('#id_phase').val()];
    var form = modal.find('#form-db-add-method');
    form.attr("action", "/db_method_add_form/");
    var options = {
        data: data,
        success: function(returned){
            $(document).find('.modal-content').html(returned);
            formatForm();
        }
    };
    form.ajaxSubmit(options);
});

$(document).on('change.tm','#method-edit-phase-select',function(e){
    e.preventDefault();
    var select = $(this);
    var modal = select.closest('.modal');
    var selected = $(document).find('.selected');
    var data = _getModalModelAttrs(modal);
    data.phase_id = select.find('#id_phase').val();
    var form = modal.find('#form-db-method-update');
    form.attr("action", "/db_method_edit_form/");
    var options = {
        data: data,
        success: function(returned){
            $(document).find('.modal-content').html(returned);
            formatForm();
        }
    };
    form.ajaxSubmit(options);
});
//END ITEM

$(document).on('click.mdb','#btn-mdb-manage-phase',function(e){
    e.preventDefault();
    $.get('/db_manage_phases/',function(returned){
        var header        = "Manage Phases";
        var content       = returned;
        var strSubmitFunc = "";
        var btnText       = "";
        var footer        = false;
        doModal('dynamicModal', header, content, strSubmitFunc, btnText, footer);
        $(document).find('.modal-content').css('overflow','hidden');
        $(document).find('.modal-dialog').css('width','40vw');
    });
});

$(document).on('click.mdb','#btn-mdb-manage-method',function(e){
    e.preventDefault();
    $.get('/db_manage_methods/',function(returned){
        var header        = "Manage Methods";
        var content       = returned;
        var strSubmitFunc = "";
        var btnText       = "";
        var footer        = false;
        doModal('dynamicModal', header, content, strSubmitFunc, btnText, footer);
        $(document).find('.modal-content').css('overflow','hidden');
        $(document).find('.modal-dialog').css('width','40vw');
    });
});

$(document).on('click.mdb','.phase-delete',function(e){
    e.preventDefault();
    var btn = $(this);
    var item = btn.closest(".item");
    var id = item.attr("id");
    $.post('/phase_delete/', {'id':id}, function(returned){
        if (returned.success) {
            item.remove();
        }
    });
});

$(document).on('click.mdb','.method-delete',function(e){
    e.preventDefault();
    var btn = $(this);
    var item = btn.closest(".item");
    var id = item.attr("id");
    $.post('/method_delete/', {'id':id}, function(returned){
        if (returned.success) {
            item.remove();
        }
    });
});

$(document).on('click.mdb','.method-remove',function(e){
    e.preventDefault();
    var btn = $(this);
    var item = btn.closest(".object");
    var id = item.attr("data-obj-id");
    var pt = item.closest(".ptype-method");
    var ptypeId = pt.attr("data-obj-id");
    $.post('/method_remove/', {'id':id, 'ptype_id': ptypeId}, function(returned){
        if (returned.success) {
            item.remove();
        }
    });
});

$(document).on('click.mdb','.phase-remove',function(e){
    e.preventDefault();
    var btn = $(this);
    var item = btn.closest(".object");
    var id = item.attr("data-obj-id");
    var pt = item.closest(".ptype-method");
    var ptypeId = pt.attr("data-obj-id");
    $.post('/phase_remove/', {'id':id, 'ptype_id': ptypeId}, function(returned){
        if (returned.success) {
            item.remove();
        }
    });
});

$(document).on('click.mdb','.project-type-remove',function(e){
    e.preventDefault();
    var btn = $(this);
    var item = btn.closest(".object");
    var id = item.attr("data-obj-id");
    $.post('/project_type_remove/', {'id':id}, function(returned){
        if (returned.success) {
            item.remove();
        }
    });
});
