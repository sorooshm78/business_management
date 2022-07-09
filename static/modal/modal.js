function delBtnOnClick(url) {
    $('#url').val(url);
    var modal = $('#delModal');
    modal.style.display = "block";
}

function doDelete() {
    var url = $('#url').val();
    $.get(url);
    location.reload();
}