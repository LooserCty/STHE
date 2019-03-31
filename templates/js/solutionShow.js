// $(document).ready
var ringSum = 100;

$(function () {
    // $(".test").hide();
    $(".show").hide();

    var data = {
        name: "{{ datas['name'] }}"
    };

    $.ajax({
        type: 'get',
        // url: 'getProjectDateAndType',
        //url: "{{ url_for('project.getProjectDateAndType')}}",
        url: "{{ url_for('project.index')}}" + "getProjectDateAndType",
        async: true,
        data: data,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            var options = "";
            for (var i = 0; i < data['date'].length; ++i) {
                options += "<option>" + data['date'][i] + "</option>";
            }
            $(".collectDate").html(options);

            var types = "";
            for (var i = 0; i < data['type'].length; ++i) {
                types += "<option>" + data['type'][i] + "</option>";
            }
            $(".evaluationType").html(types);

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(textStatus);
        }
    });

    //绑定下拉框值改变事件
    $(".collectDate").change(function () {
        $(".test").show();
        var dataShow = {
            name: "{{ datas['name'] }}",
            date: this.value,
            type: $(".evaluationType").val()
        };
        $.ajax({
            type: 'get',
            url: 'getProjectSolutionShow',
            async: true,
            data: dataShow,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                // alert("../ok");
                $(".img-1").prop('src',
                    // "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/1.png')|safe }}"
                    data['path']
                );
                // $(".img-2").prop('src',
                //     "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/2.png')|safe }}"
                // );
                ringSum = 200;
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(textStatus);
            }
        });

    });

    //绑定下拉框值改变事件
    $(".evaluationType").change(function () {
        $(".test").show();
        var dataShow = {
            name: "{{ datas['name'] }}",
            date: $(".collectDate").val(),
            type: this.value
        };
        $.ajax({
            type: 'get',
            url: 'getProjectSolutionShow',
            async: true,
            data: dataShow,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                // alert("../ok");
                $(".img-1").prop('src',
                    // "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/1.png')|safe }}"
                    data['path']
                );
                // $(".img-2").prop('src',
                //     "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/2.png')|safe }}"
                // );
                ringSum = 200;
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(textStatus);
            }
        });

    });

    // // 进度条
    // var scroll = document.getElementById('scroll');
    // var bar = document.getElementById('bar');
    // var mask = document.getElementById('mask');
    // var ringNumber = document.getElementById('ringNumber');
    // // var ptxt = document.getElementsByTagName('p')[0];
    // var barleft = 0;
    // bar.onmousedown = function (event) {
    //     var event = event || window.event;
    //     var leftVal = event.clientX - this.offsetLeft;
    //     var that = this;
    //     // 拖动一定写到 down 里面才可以
    //     document.onmousemove = function (event) {
    //         var event = event || window.event;
    //         barleft = event.clientX - leftVal;
    //         if (barleft < 0)
    //             barleft = 0;
    //         else if (barleft > scroll.offsetWidth - bar.offsetWidth)
    //             barleft = scroll.offsetWidth - bar.offsetWidth;
    //         mask.style.width = barleft + 'px';
    //         that.style.left = barleft + "px";
    //         ringNumber.value = parseInt(barleft / (scroll.offsetWidth - bar.offsetWidth) * ringSum);

    //         //防止选择内容--当拖动鼠标过快时候，弹起鼠标，bar也会移动，修复bug
    //         window.getSelection ? window.getSelection().removeAllRanges() : document.selection.empty();
    //     }
    // };
    // document.onmouseup = function () {
    //     document.onmousemove = null; //弹起鼠标不做任何操作
    // };

    // $(".ringNumber").change(function () {
    //     var barleft = this.value / ringSum * (scroll.offsetWidth - bar.offsetWidth);
    //     mask.style.width = barleft + 'px';
    //     bar.style.left = barleft + "px";
    //     // alert(this.value);
    // });

});

window.onload = function () {
    $(".show").show();

    var dataShow = {
        name: "{{ datas['name'] }}",
        date: $(".collectDate").val(),
        type: $(".evaluationType").val()
    };
    $.ajax({
        type: 'get',
        url: 'getProjectSolutionShow',
        async: true,
        data: dataShow,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            $(".img-1").prop('src',
                // "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/1.png')|safe }}"
                data['path']
            );

            // $(".img-2").prop('src',
            //     "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/2.png')|safe }}"
            // );
            ringSum = 200;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(textStatus);
        }
    });
}