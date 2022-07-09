function delBtnOnClick() {
    var modal = $('#delModal');
    modal.style.display = "block";
}

function doDelete(url) {
    $.get(url);
    location.reload();
}