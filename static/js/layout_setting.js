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

function px() {
    $('#tab tr').each(function (n) {
        $('#tab tr')[n].children[0].innerText = 1 + n++;
    });
}
function add(obj) {
    var brothers = obj.parentElement.cloneNode(true);
    obj.parentNode.after(brothers);
}

function del(obj) {
    obj.parentElement.remove()
}

function tb(obj) {
    if ($('#tab').css('display') == 'none'){
        wbgs();
    };
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

function keywords(keyword_list,keyword_list_new) {
    // let yao = keyword_list;
    $(".input-select").attr("placeholder", "键入索引 快速输入关键字");
    $(".input-select").keyup(function () {
        $(".input-select+div").empty();
        //判断该组件是否已获得焦点
        if ($(this).is(":focus")) {
            keyword_list.forEach((e) => {
                if (e.keyword.indexOf($(this).val()) != -1){
                $(".input-select+div").append("<a id=" + e.keyword + ">" + e.keyword + "</a>");
            }
        })
        }
        $(".input-select+div").append("<a>" + $(this).val() + "</a>");
    });
    $(".input-select").focus(function () {
        $(".input-select+div").empty();
        $(this).after("<div></div>");
        keyword_list.forEach((e) => {
            $(".input-select+div").append("<a>" + e.keyword + "</a>");
    })
    });
    $(".input-select").blur(function () {
        if (!$(".input-select+div").is(":hover"))
            $(".input-select+div").remove();
            key(keyword_list_new);
            // var vue = $.inArray($(this).val(),keyword_list_new);
            // if (vue!=-1){
            //     $(this).css("color","blue").css("font-weight","bold");
            // }
    });
    $("#tbody").on("click", ".input-select+div a", function () {
        $(this).parent().prev().val($(this).text());
        // $(this).parent().prev().css("color","blue").css("font-weight","bold");
        $(".input-select+div").remove();
    });
}


$("#resource,#suite").change(function () {
    searchKeywords()
});
$("#resource,#suite").ready(function () {
    searchKeywords();
});
function selectAmount() {
    var data = [];
    $('#tab tr').each(function (i) {
        // 遍历 tr
        $(this).children('td').each(function (j) {  // 遍历 tr 的各个 td
            var item = $(this).children('input').val();
            var arg = /\$\{\w+\}/g;
            var rep = /\[.+\]/g;
            if(j > 2 && item && item != "${EMPTY}") {
                var v = arg.exec(item.replace(rep,''));
                if ($.inArray(data,v)==-1){
                    data.push(v);
                }
            };
        });
    });
    var args = data.join("|");
    $('#id_Arguments').val(args)
}
$(window).on('load', function () {  
    $('.selectpicker').selectpicker({  
        'selectedText': ''
    });
});  

function searchKeywords() {
    var resource = $("#resource").val();
    var suite = $("#suite").val();
    $.ajax({
        url: '/keywords_select',
        type: 'GET',
        data: {'resource': resource, 'suite': suite},
        success: function (arg) {
            var data = JSON.parse(arg);
            if (data.status) {
                var keyword_list_new = [];
                $.each(data.keyword_list,function(i,item){
                    keyword_list_new.push(item.keyword);
                });
                keywords(data.keyword_list,keyword_list_new);
                key(keyword_list_new);
                argumnets(data.keyword_list);
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

function key(keyword_list){

    $('#tab tr').each(function (i) {
        $(this).children('td').each(function (j) {
            var value = $(this).children('input').val();
            var vlaue = $.inArray(value, keyword_list);
            if(vlaue != -1) {
                $(this).children('input').css("color","blue").css("font-weight","bold");
            }
        });
});

}

function argumnets(keyword_list) {
    $('#tab tr>td>input').mouseover(function(){
        // console.log($(this).val());
        keyword_list.forEach((e) => {
            // console.log(e.keyword);
            if (e.keyword==$(this).val()){
                console.log(e.arguments,e.documentation);
                $("#flo1").text('输入参数：'+e.arguments);
                $("#flo2").text('帮助信息：'+e.documentation);
                // var mod = "<p>" + e.arguments + "</p>";
                // alert(mod);
                // var top  = event.pageY-5;
                // var left = event.pageX-5;
                var top = $(this).offset().top + 36
                var left = $(this).offset().left
                $("#flo").css({
                    'top' : top + 'px',
                    'left': left+ 'px',
                    'display': 'block'
                   });
                setTimeout(function(){$("#flo").hide()}, 3000);
            }
        })
    })
}

function wbgs(obj) {
    console.log($('#text').text());
    if ($('#text').css('display') == 'none'){
        $('#tab').hide();
        var data = '';
        $('#tab tr').each(function (i) {
            // 遍历 tr
            var v = '';
            $(this).children('td').each(function (j) {  // 遍历 tr 的各个 td
                var value = $(this).children('input').val();
                if (value != undefined && value != '') {
                    v = v + '    '+value
                }
                $(this).children('input').val('');
            });
            if (v){
                data = data +v+ '\n'
            }
        });
        $('#text').val(data);
        $('#text').show();
    } else {
        $('#text').hide();
        var tr = $('#text').val().split('\n');
        // console.log(tr);
        tr.forEach(function (n,i) {
            var td = n.split('    ');
            // console.log($('#tab tr').length);
            if ($('#tab tr').length<i){
                console.log(i);
                var brothers = $('#tab tr')[0].cloneNode(true);
                brothers.children[0].innerText = 1 + $('#tab tr').length;
               $('#tab tr')[0].after(brothers);
                px();
            }
            if ($('#tab tr')[i]){
                td.forEach(function (v,j) {
                    if ($('#tab tr')[i].children.length<td.length){
                        console.log($('#tab tr')[i].children[1].children[0]);
                        add($('#tab tr')[i].children[1].children[0]);
                    };
                    if (v){
                        $('#tab tr')[i].children[j].children[0].value = v;
                    }
                });
            }
        });
        $('#tab').show();
    }
}

$(function() {
    //初始化菜单
    $.contextMenu({
        selector: '.tr',
        callback: function(key, options) {
            console.log("点击了：" + key);
        },
        items: {
            "Insert Rows": {name: "插入", icon: "add",callback:function(){
                var i = $('#tab tr').length;
                var j = i - 1;
                var brothers = $('#tab tr')[j].cloneNode(true);
                brothers.children[0].innerText = 1 + i++;
                $(this).before(brothers);
                px();
            }},
            "Delete Rows": {name: "删除", icon: "delete",callback:function(){
                $(this).remove();
                px();
            }},
            "sep1": "---------",
            "Move Up": {name: "上移", icon: "cut",callback:function(){
                var prev = $(this).prev();
                if ($(this).index() > 0) {
                    $(this).insertBefore(prev); //插入到当前<tr>前一个元素前
                    }
                px();
            }},
            "Move Down": {name: "下移", icon: "copy",callback:function(){
                var next = $(this).next();
                if (next) {
                    $(this).insertAfter(next); //插入到当前<tr>前一个元素前
                    }
                px();
            }},
            "sep2": "---------",
            "Comment": {name: "注释", icon: "",callback:function(){
                var td = $(this).children()[1];
                var brothers = td.cloneNode(true);
                brothers.children[0].value = "Comment";
                td.before(brothers);
            }},
            "Uncomment": {name: "反注释", icon: "",callback:function(){
                var td = $(this).children()[1]
                var value = td.children[0].value;
                if (value=="Comment") {
                    td.remove();
                }
            }},
        }
    });
});