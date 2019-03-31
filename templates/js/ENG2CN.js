$(function () {
    o = document.getElementsByClassName('dataTables_length');
    if (o[0]) {
        o[0].children[0].innerHTML = o[0].children[0].innerHTML.replace('Show', '显示');
        o[0].children[0].innerHTML = o[0].children[0].innerHTML.replace('entries', '项');
    }


    o = document.getElementsByClassName('dataTables_filter');
    if (o[0]) {
        o[0].children[0].innerHTML = o[0].children[0].innerHTML.replace('Search', '搜索');
    }


    o = document.getElementsByClassName('dataTables_empty');
    if (o[0]) {
        o[0].innerHTML = '表格中没有数据';
    }


    o = document.getElementsByClassName('dataTables_info');
    if (o[0]) {
        o[0].innerHTML = o[0].innerHTML.replace('Showing', '显示');
        o[0].innerHTML = o[0].innerHTML.replace('entries', '项');
        o[0].innerHTML = o[0].innerHTML.replace('to', '到');
        o[0].innerHTML = o[0].innerHTML.replace('of', '共');
    }

    o = document.getElementById('dataTable_previous');
    if (o) {
        o.innerHTML = o.innerHTML.replace('Previous', '上一页');
    }

    o = document.getElementById('dataTable_next');
    if (o) {
        o.innerHTML = o.innerHTML.replace('Next', '下一页');
    }

});