function getUrlParam(name) {
		var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
		var r = window.location.search.substr(1).match(reg);
		if(r != null) {
			return decodeURI(r[2]);
		}
		return null;
}

function digest(trunks) {
    for (let trunk of trunks) {
        trunk.en_trunk = trunk.en_trunk.trim();
        trunk.cn_trunk = trunk.cn_trunk.trim();
        trunk.x_trunk = '';
        if (trunk.en_trunk.length > 0 && trunk.cn_trunk.length > 0) {
            trunk.en_trunk_digest = textDigest(trunk.en_trunk, 50);
            trunk.cn_trunk_digest = textDigest(trunk.cn_trunk, 40);
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
        trunk.x_trunk_digest = textDigest(trunk.x_trunk, 90);
    }
}

function mergeOptions(options) {
    for (let option of options) {
        if (option.en_option.length > 0 && option.cn_option.length === 0) {
            option.x_option = option.en_option;
        } else if (option.en_option.length === 0 && option.cn_option.length > 0) {
            option.x_option = option.cn_option;
        } else {
            option.x_option = '';
        }
    }
    return options;
}

function textDigest(text, n) {
    if (text.length <= n) {
        return text;
    } else {
        return text.substring(0, n - 1) + '…';
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

const rjust = (string, len, ch) => {
    if (string.length < len) {
        let n = len - string.length;
        let buf = [];
        for (let i = 0; i < n; i++) {
            buf.push(ch);
        }
        buf.push(string);
        return buf.join('');
    }
    return string;
};

const ckeditorConfig = {
    toolbar: ['imageUpload'],
};


class CkeditorUploadAdapter {
    constructor (loader) {
        this.loader = loader;
    }
    upload() {
        const body = new FormData();
        body.append('upload', this.loader.file);
        return fetch('/upload/', {
            body: body,
            method: 'POST'
        }).then((response) => {
            return response.json();
        }).then((result) => {
            if (result.uploaded) {
                return {
                    default: result.url,
                };
            } else {
                alert('请求失败，请检查日志');
            }
        }).catch((error) => {
            alert('请求失败，请检查日志。' + error);
        });
    }
    static abort() {
        console.log('Abort upload.');
    }
}

const newTrunk = () => {
    return {
        entity_id: '',
        code: '',
        en_trunk: '',
        cn_trunk: '',
        explanation: '',
        source: '',
        level: 0,
        comment: '',
        parent_id: '',
        options: [
            newOption(),
            newOption(),
            newOption(),
            newOption(),
        ],
    };
};

const newOption = () => {
    return {
        entity_id: '',
        // trunk_id: '',
        // code: '',
        en_option: '',
        cn_option: '',
        is_true: false,
        comment: '',
    };
};