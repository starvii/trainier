function digest(trunks) {
    for (let i = 0, len = trunks.length; i < len; i++) {
        let trunk = trunks[i];
        trunk.en_trunk = trunk.en_trunk.trim();
        trunk.cn_trunk = trunk.cn_trunk.trim();
        trunk.x_trunk = '';
        if (trunk.en_trunk.length > 0 && trunk.cn_trunk.length > 0) {
            trunk.en_trunk_digest = text_digest(trunk.en_trunk, 50);
            trunk.cn_trunk_digest = text_digest(trunk.cn_trunk, 50);
            continue;
        } else if (trunk.en_trunk.length === 0 && trunk.cn_trunk.length === 0) {
            trunk.en_trunk_digest = '';
            trunk.cn_trunk_digest = '';
            continue
        } else if (trunk.cn_trunk.length === 0 && trunk.en_trunk.length > 0) {
            trunk.x_trunk = trunk.en_trunk;
        } else if (trunk.en_trunk.length === 0 && trunk.cn_trunk.length > 0) {
            trunk.x_trunk = trunk.cn_trunk;
        }
        trunk.x_trunk_digest = text_digest(trunk.x_trunk, 100);
    }
}

function text_digest(text, n) {
    if (text.length <= n) {
        return text;
    } else {
        return text.substring(0, n - 3) + '...';
    }
}

//获取cookie
function getCookie(name) {
    let arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return (arr[2]);
    else
        return null;
}

//设置cookie
function setCookie(c_name, value, expiredays) {
    let exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + decodeURIComponent(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toUTCString());
}

//删除cookie
function delCookie(name) {
    let exp = new Date();
    exp.setTime(exp.getTime() - 1);
    let cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toUTCString()
}