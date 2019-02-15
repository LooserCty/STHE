// $(document).ready
$(function () {
    $(".test").hide();

    var data = {
        name: "{{ datas['name'] }}"
    };

    $.ajax({
        type: 'get',
        // url: 'getProjectDate',
        //url: "{{ url_for('project.getProjectDate')}}",
        url: "{{ url_for('project.index')}}" + "getProjectDate",
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
        }
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
                    "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/1.png')|safe }}"
                )
                $(".img-2").prop('src',
                    "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/2.png')|safe }}"
                )
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(textStatus);
            }
        });

    });


});

window.onload = function () {
    var dataShow = {
        name: "{{ datas['name'] }}",
        date: $(".collectDate").val(),
        type: $(".evaluationType").val()
    }
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
                "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/1.png')|safe }}"
            )
            $(".img-2").prop('src',
                "{{ url_for('static',filename='data/'+g.user['username']+'/'+datas['name']+'/solution/image/2.png')|safe }}"
            )
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(textStatus);
        }
    });
}