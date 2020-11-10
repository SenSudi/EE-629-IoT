function homeMilestoneProjectMinMax (obj) {
	var title = $(obj);
	var project = title.closest('.project');
	var ms 		= project.find('#home-milestones');
	if (ms.css('display') == 'none') {
		ms.css('display','block');
	} else {
		ms.css('display','none');
	}
}

function msProjectFilter(e) {
    var option  = $(e.target).find(':selected');
    var text    = option.text()
    var proj_id = option.val();
    var url     = '/home_milestones/';
    $.get(url,{'p_id':proj_id},function(returned){
        var activate = $('#btn-activate-filters');
        msFilterSubmit(activate);
        $('.milestones').empty().html(returned);
        if (proj_id != 'all'){
            $('#showing').empty().text(text);
        } else {
            $('#showing').empty().text('All Projects');
        }
    });
}

function msStatusFilter(e) {
    var option  = $(e.target).find(':selected');
    var text    = option.text()
    var status  = option.val();
    var url     = '/home_milestones/';
    $.get(url,{'status':status},function(returned){
        msFilterSubmit();
        $('.milestones').empty().html(returned);
        if (status != 'all'){
            $('#showing').empty().text(text);
        } else {
            $('#showing').empty().text('All Status');
        }
    });
}

function msFilterReset(e) {
    _selectDefault()
    $.get('/ms_filter_clear/',function(returned) {
        $('.milestones').html(returned);
    });
}

function _selectDefault() {
    document.getElementById('project-filter').value = 'all';
    document.getElementById('status-filter').value = 'all';
    document.getElementById('fltr-date-start').value = '';
    document.getElementById('fltr-date-end').value = '';
}

function msFilterSubmit(e) {
    var pid        = _getPid();
    var status     = $('#status-filter').find(':selected').val();
    var from       = _getStart();
    var to         = _getEnd();
    var data       = {};
    data['pid']    = pid;
    data['status'] = status;
    data['from']  = from;
    data['to']    = to;
    $.get('/ms_filter_submit/',data,function(returned) {
        $('.milestones').html(returned);
    });
}

function msSort(e, field) {
    var isAscending = _isAscendingOrder(e);
    var id = $(e).attr('id');
    var data = {};
    data['isAscending'] = isAscending;
    data['field'] = field;
    $.get('/ms_sort/',data,function(returned) {
        $('.milestones').empty().html(returned);
        _changeSortIcon(document.getElementById(id), isAscending);
    });
}

function _isAscendingOrder(e) {
    var sort = $(e).find('.fa');
    if (sort.hasClass('fa-sort') || sort.hasClass('fa-sort-down')) {
        return false;
    } else if (sort.hasClass('fa-sort-up')) {
        return true;
    }
}

function _changeSortIcon(e, sortAscending) {
    var sort = $(e).find('.fa');
    if (sortAscending) {
        sort.removeClass();
        sort.addClass('fa fa-sort-down');
    } else {
        sort.removeClass();
        sort.addClass('fa fa-sort-up');
    }
}