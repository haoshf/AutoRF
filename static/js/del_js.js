
function bindDel() {
    $('#tb').on('click', '.del-row', function () {
        $('#delModal').modal('show');
        rowIds = [];
        var rowId = $(this).parent().parent().attr('nid');
        rowIds.push(rowId);
    });
}

function binplDel() {
    $('#delBtn').on('click',function () {
        rowIds = [];
        $("input[name='check_box_list']:checked").each(function (i) {
            rowIds.push($(this).val());
        });
        console.log('sssssssssssssssssssss',rowIds);
        if (rowIds.length == 0){
            alert('请先勾选要删除的数据！')
        } else{
            $('#delModal').modal('show')
        }
        });
}

function bindDelCancel() {
    $('#delCancel').click(function () {
        $('#delModal').modal('hide');
        })
}

function clickDome(obj){
    if($(obj).prop("checked")){
        $("#tb").find("input[type='checkbox']").prop("checked",true);
    }else{
        $("#tb").find("input[type='checkbox']").prop("checked",false);
    }
}

window.onload=function () {
    $("#project_list").click();
};