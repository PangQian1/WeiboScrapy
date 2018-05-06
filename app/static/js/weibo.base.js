var API_HOST = 'http://127.0.0.1:5000';
var FE_HOST  = 'http://localhost:63343';
var USER_INDEX_URL = FE_HOST + '/WeiboScrapy/app/static/index.html';
var USER_MAIN_URL  = FE_HOST + '/WeiboScrapy/app/static/main.html';

// 获取url参数中的某个key的值
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

// 性别处理
function getSex(sex) {
    var result = '女';
    if (sex == 'm')
        result = '男';
    return result;
}

// 是否是微博认证
function getVerify(verify) {
    var result = "未认证";
    if (verify == '2') {
        result = '微博认证(V)';
    }
    return result;
}

