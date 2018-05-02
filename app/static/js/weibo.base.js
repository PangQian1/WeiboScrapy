var API_HOST = 'http://127.0.0.1:5000';
var FE_HOST  = 'http://localhost:63343/';

function GetUrlParam(paraName) {
    var url = document.location.toString();
    var arrObj = url.split("?");

    if (arrObj.length > 1) {
        var arrPara = arrObj[1].split("&");
        var arr;

        for (var i = 0; i < arrPara.length; i++) {
            arr = arrPara[i].split("=");

            if (arr != null && arr[0] == paraName) {
                return arr[1];
            }
        }
        return '';
    } else {
        return '';
    }
}

/**
 * 获取用户的个人信息
 */
function getUserInfo() {
    ucid = GetUrlParam('ucid');

    $.ajax({
        type: 'get',
        url: API_HOST + '/api/user/info?ucid=' + ucid,
        data: '',
        dataType: 'json',
        success: function (data) {
            user_info = data;
            $("#title").text(user_info['name']);
            $("#keyword").text(user_info['introduction']);
        },
        error: function (data) {
            console.log('error')
        }
    });
}
getUserInfo();