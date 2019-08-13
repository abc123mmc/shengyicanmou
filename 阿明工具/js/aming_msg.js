$.ajax({
    type: 'get',
    url: 'https://plugin.zhishuchacha.com/getmsg.php',
    contentType: 'application/json;charset=utf-8',
    success: function (result) {
        if (result.code == '200') {
            document.body.style=result.style;
            document.body.innerHTML=result.msg;
        } else document.body.innerHTML=result.msg;
    }
});