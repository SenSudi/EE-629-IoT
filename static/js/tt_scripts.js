function noteZeroTimes(){
  $.each($('.entry'),function(){
    var entry = $(this);
    var time = parseFloat(entry.find('.entry-time').text());
    if (time == 0) {
      entry.find('.item-header').css('background-color','#ce6868');
    }
  });
}


function ttEntryAdd () {
  var url             ='/entry_add_form/';
  $.get(url,function(returned){
    var header         = "Add Time Entry";
    var content        = returned
    var strSubmitFunc  = "ttEntrySubmit(event)";
    var btnText        = "Add Entry";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    var modal = $('#modalWindow');
    var form = modal.find('form');
    modal.find('#btn-modal-form-submit').attr('id','btn-submit-entry');
    form.attr('action','/add_time_entry/')
    form.find('#id_project').attr('onchange','ttEntryAddProjectChange(this)');
    formatForm();
  });

}

function ttEntryAddProjectChange(obj){
  var select = $(obj);
  var choice = select.find(':selected');
  var p_id = choice.val();
  var url = '/get_tasks_for_project/';
  $.get(url,{'p_id':p_id},function(returned){
    if (returned == 'invalid project') {
      alert(returned);
    } else {
      select.closest('form').append('<div class="form-group"><label for="id_task"></label><span></span><div class="input-group"><div class="input-group-addon"></div><select id="id_task" name="task"></select></div></div>');
      $('#id_task').empty().html(returned);
      formatForm();
      $('#id_task').closest('.form-group').css('display','block');
    }
  });
}

function tableCompute() {
  $.get('/get_week/',function(info){
    $('#week-div').empty().html(info);
    _setWeekTotal();
    _setPeriodTotal();
  });
}

function ttEntrySubmit (e) {
  e.preventDefault();
	var form = $(e.target).closest('.modal').find('form');
	form.ajaxSubmit(function(returned){
      $('#entries').empty().html(returned);
      tableCompute();
      $('#modalWindow').modal('hide');
      noteZeroTimes();
      updateAudits('timetracker');
    });
}

function ttEntryEdit (obj) {
  var btn             = $(obj);
  var item            = btn.closest('.item');
  var timetracker_id         = item.attr('id');
  var url             ='/time_entry_edit_form/';
  $.get(url,{'id':timetracker_id,'submit_id':'btn-update-entry','action':'/time_entry_edit/'},function(returned){
    var header        = "Update Time Entry";
    var content       = returned;
    var strSubmitFunc = "";
    var btnText       = "";
    doModal('dynamicModal', header, content, strSubmitFunc, btnText);
    $('#modalWindow').find('#update_id').val(timetracker_id);
    formatForm();
  });
}

$(document).on('click.tt','#btn-update-entry',function(e){
  e.preventDefault();
  ttEntryUpdate(e);
});

function ttEntryUpdate(e){
  e.preventDefault();
  var modal = $(e.target).closest('.modal')
  var form  = modal.find('form');
  form.ajaxSubmit(function(returned){
    $('#entries').empty().html(returned);
    tableCompute();
    modal.modal('hide');
    noteZeroTimes();
    updateAudits('timetracker');
  });
}

function ttDelete (obj) {
  var item            = $(obj).closest('.item');
  var timetracker_id         = item.attr('id');
  $.ajax({
    type: 'POST',
    url: '/delete_time_entry/',
    data: {'del_time_entry_id' : timetracker_id},
    success: function(data) {
      if (data == 'success') {
        item.remove();
        tableCompute();
      }
    }
  });
}



function ttProjectFilter (e) {
  var option  = $(e.target).find(':selected');
  var text    = option.text()
  var proj_id = option.val();
  var url     = '/display_time_entries/';
  $.get(url,{'p_id':proj_id},function(returned){
    var activate = $('#btn-activate-filters');
    ttFilterSubmit(activate);
    $('#entries').empty().html(returned);
    if (proj_id != 'all'){
      $('#showing').empty().text(text);
    } else {
      $('#showing').empty().text('All Projects');
    }
    noteZeroTimes();
  });
}
  
function ttFilterDateCurrent (obj) {
  var btn = $(obj);
  var val = btn.find(':selected').val();
  $.get('/tt_get_current/',{'val':val},function(returned){
    var start = returned.dates.start
    var end   = returned.dates.end
    $('#fltr-date-start').val(start)
    $('#fltr-date-end').val(end)
    var activate = $('#btn-activate-filters');
    //console.log(activate);
    //console.log(activate[0]);
    ttFilterSubmit(activate);
  });
}

function _getPid () {
  return $('#project-filter').find(':selected').val();
}

function _getUid () {
  return $('#user-filter').find(':selected').val();
}

function _getStart () {
  return $('#fltr-date-start').val();
}

function _getEnd () {
  return $('#fltr-date-end').val();
}

function _setShowing () {
  var proj    = $('#project-filter').find(':selected').text();
  var user    = $('#user-filter').find(':selected').text();
  var from    = _getStart();
  var to      = _getEnd();
  var message = $('#message');
  var pm = message.find('#proj-msg');
  var um = message.find('#user-msg');
  var fm = message.find('#from-msg');
  var tm = message.find('#to-msg');
  if (/-- All/.test(proj)) {
    pm.text('All Projects');
  } else {
    pm.text(proj);
  }
  um.text(user);
  fm.text(from);
  tm.text(to);
}

function _setWeekTotal () {
  var total = 0.00; 
  $.each($('.day'),function(){
    var time = parseFloat($(this).text());
    total += time;
  });
  $('#week-total').text(total.toFixed(2));
}

function _setPeriodTotal () {
  var total = 0.00;
  $.each($('.entry'),function(){
    var entry = $(this);
    if (entry.css('display') != 'none') {
      var time = parseFloat(entry.find('.entry-time').text().trim());
      total += time
    }
  });
  $('#period-total').text(total.toFixed(2));
}

function ttFilterSubmit (obj) {
  //console.log(obj)
  var btn       = $(obj);
  var pid       = _getPid();
  var uid       = _getUid();
  var from      = _getStart();
  var to        = _getEnd();
  var data      = {};
  data['pid']   = pid;
  data['uid']   = uid;
  data['from']  = from;
  data['to']    = to;
  $.get('/tt_filter_submit/',data,function(returned) {
    $('#entries').empty().html(returned);
    searchBar($('#input-search')[0]);
    _setShowing();
    $.get('/get_week/',function(info){
      $('#week-div').empty().html(info);
      _setWeekTotal();
      _setPeriodTotal();
    });
  });
}

function ttDayCopyHours (obj) {
  var btn = $(obj);
  var id  = btn.attr('data-copy');
  var item = $('#'+id);
  copyText(btn);
}

function ttDayCopyNotes (obj) {
  var btn = $(obj);
  var notes = btn.find('.tt-day-notes');
  notes.text(formatBrToNewline(notes.text()));
  copyText(notes);
}

function ttSearchUpdate () {
  _setPeriodTotal();
}

function ttDayShowNotes (obj) {
  var btn = $(obj);
  var notes = btn.parent().find('.tt-day-notes').val();
  var date = btn.closest('.day').find('.tt-day-two-date').text();
  var header        = "Daily Notes for "+date;
  var content       = notes;
  var strSubmitFunc = "closeAlertModal(this);";
  var btnText       = "Close";
  doModal('noteDetailsModal', header, content, strSubmitFunc, btnText);
}
  // $(document).on('click','#btn-filter-date',function(){
  //     var btn = $(this);
  //     //btn.closest('form').preventDefault();
  //     data = {};
  //     var from = $('#from-date').val();
  //     var url ='/display_time_entries/';
  //     if ($('#from-date').val().length == 10) {
  //       data['from'] = $('#from-date').val();
  //     }
  //     if ($('#to-date').val().length == 10) {
  //       data['to'] = $('#to-date').val();
  //     }
  //     data['p_id'] = $('#project-filter').find(':selected').val();
  //     $.get(url,data,function(returned){
  //       if (returned != 'Invalid Date or Range!') {
  //         $('#entries').empty().html(returned);
  //         btn.text('Clear Filter');
  //         btn.attr('id','btn-clear-filter');
  //         btn.removeClass('btn-success');
  //         btn.addClass('btn-info');
  //       }
  //     });
  // });

// $(document).on('click','#btn-clear-filter',function(){
//   var btn = $(this);
//   var url = /display_time_entries/;
//   data = {'p_id':$('#project-filter').find(':selected').val()};
//   $.get(url,data,function(){
//     $('#entries').empty().html(returned);
//     btn.text('Filter');
//     btn.attr('id','btn-filter-date');
//     btn.removeClass('btn-info');
//     btn.addClass('btn-success');
//   });
// });

$(document).on('click','.btn-time-entry-add',function(){
  var btn             = $(this);
  var object          = btn.closest('.object');
  var obj             = _getObjModelAttrs(object);
  $.get('/time_entry_add_form/',{'submit_id':'btn-time-entry-submit','action':'/time_entry_add/'},function(returned){
    var header        = 'Add Time Entry for '+obj.type+' <b>'+obj.title+'</b>';
    var content       = returned;
    var strSubmitFunc = '';
    var btnText       = '';
    var footer        = false;
    doModal('dynamicModal',header,content,strSubmitFunc,btnText,footer);
    formatForm();
    var modal = $('#dynamicModal').find('.modal');
    _setModalModelAttrs(modal,obj);
  });
});

$(document).on('click','#btn-time-entry-submit',function(e){
  e.preventDefault();
  var btn = $(this);
  var modal = btn.closest('.modal');
  var form = modal.find('#form-time-entry-add');
  var data = _getModalModelAttrs(modal);
  data.where = $(document).find('#page-data').attr('where');
  var options = {
    data:data,
    success:  function(returned){
                if (returned.errors) {
                  populateFormErrors(form.attr('id'),returned.errors);
                } else {
                  modal.modal('hide');
                }
              }
  };
  form.ajaxSubmit(options);
});
