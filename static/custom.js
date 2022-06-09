function fillCategory() {
    $('#cat_dis').empty();
    var record_type = $('#record_type').val();
    var repo_id = $('#repo_id').val();
    $.get('/get-cat-list/?type=' + record_type + '&repo_id=' + repo_id).then(
        res => {
            var cat_list = res['list'];
            $('#cat_dis').append(
                new Option("---------", "")
            );
            for (index in cat_list) {
                $('#cat_dis').append(
                    new Option(cat_list[index][0], cat_list[index][1])
                );
            }
        }
    );
}