function test(obj) {

    var div1 = document.getElementById("div1");
    if (div1.style.display == "block") {
        div1.style.display = "none";
        obj.innerHTML = 'Settings<<';
    } else {
        div1.style.display = "block";
        obj.innerHTML = 'Settings>>';
    }
}

function zj(obj) {
    var i = $('#tab tr').length;
    var j = i - 1;
    var brothers = $('#tab tr')[j].cloneNode(true);
    brothers.children[0].innerText = 1 + i++;
    $('#tab tr')[j].after(brothers);
}

function add(obj) {
    var brothers = obj.parentElement.cloneNode(true);
    obj.parentNode.after(brothers);
}

function del(obj) {
    obj.parentElement.remove()
}

function tb(obj) {
    var data = {};
    $('#tab tr').each(function (i) {
        // 遍历 tr
        $(this).children('td').each(function (j) {  // 遍历 tr 的各个 td
            var rowcell = String(i + 1) + '-' + String(j);
            var value = $(this).children('input').val();
            if (value != undefined && value != '') {
                data[rowcell] = $(this).children('input').val();
            }
        });
    });
    $('#valdict').val(JSON.stringify(data));
}

function keywords(keyword_list) {
    let yao = keyword_list;
    $(".input-select").attr("placeholder", "键入索引 快速输入关键字");
    $(".input-select").keyup(function () {
        $(".input-select+div").empty();
        //判断该组件是否已获得焦点
        if ($(this).is(":focus")) {
            yao.forEach((e) => {
                if (e.keyword.indexOf($(this).val()) != -1){
                $(".input-select+div").append("<a id=" + e.keyword + ">" + e.keyword + "</a>");
            }
        })
        }
        $(".input-select+div").append("<a>" + $(this).val() + "</a>");
    });
    $(".input-select").focus(function () {
        $(this).after("<div></div>");
        yao.forEach((e) => {
            $(".input-select+div").append("<a>" + e.keyword + "</a>");
    })
    });
    $(".input-select").blur(function () {
        if (!$(".input-select+div").is(":hover"))
            $(".input-select+div").remove();
    });
    $("#tbody").on("click", ".input-select+div a", function () {
        $(this).parent().prev().val($(this).text());
        $(".input-select+div").remove();
    });
}

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
    console.log(rowIds);
    $.ajax({
        url: '/resource_select.html',
        type: 'GET',
        data: {'project': project, 'rowIds': rowIds},
        success: function (arg) {
            $('#select').html(arg);
        }
    })
}
$("#resource,#suite").change(function () {
    searchKeywords()
});
$("#resource,#suite").ready(function () {
    searchKeywords()
});

function searchKeywords() {
    var resource = $("#resource").val();
    var suite = $("#suite").val();
    $.ajax({
        url: '/keywords_select.html',
        type: 'GET',
        data: {'resource': resource, 'suite': suite},
        success: function (arg) {
            var data = JSON.parse(arg);
            if (data.status) {
                keywords(data.keyword_list);
            }
        }
    })

}
function binplDel() {
    $('#delBtn').on('click', function () {
        $('#delModal').modal('show');
        rowIds = [];
        $("input[name='Resource']:checked").each(function (i) {
            rowIds.push($(this).val());
        });
        console.log(rowIds);
    });
}
