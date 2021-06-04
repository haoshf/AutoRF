$("#project").change(function () {
    searchResource();
    $("#project_list").click();
});
$("#project").ready(function () {
    searchResource();
    $("#project_list").click();
});
function searchResource() {
    var project = $("#project").val();
    rowIds = [];
    $("input[name='Resource']:checked").each(function (i) {
        rowIds.push($(this).val());
    });
    // console.log(rowIds);
    $.ajax({
        url: '/resource_select.html',
        type: 'GET',
        data: {'project': project, 'rowIds': rowIds},
        success: function (arg) {
            $('#select').html(arg);
        }
    })
}