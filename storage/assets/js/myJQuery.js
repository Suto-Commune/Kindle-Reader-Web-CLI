var $, $s;
$ = $s = function (selector, context) {
    return new $s.fn.init(selector, context);
};
$s.fn = $s.prototype;
$s.fn.init = function (selector, context) {
    var nodeList = [];
    if (typeof (selector) == 'string') {
        nodeList = (context || document).querySelectorAll(selector);
    } else if (selector instanceof Node) {
        nodeList[0] = selector;
    } else if (selector instanceof NodeList || selector instanceof Array) {
        nodeList = selector;
    }
    this.length = nodeList.length;
    for (var i = 0; i < this.length; i += 1) {
        this[i] = nodeList[i];
    }
    return this;
};
$s.fn.init.prototype = $s.fn;
$s.fn.each = function (cb_fun, need_ret) {
    var res = [];
    for (var i = 0; i < this.length; i++) {
        res[i] = cb_fun.call(this[i]);
    }
    if (need_ret) {
        if (res.length === 1) {
            res = res[0];
        }
        return res;
    }
    return this;
};
$s.fn.eq = function () {
    var nodeList = [];
    for (var i = 0; i < arguments.length; i++) {
        nodeList[i] = this[arguments[i]];
    }
    return $s(nodeList);
};
$s.fn.first = function () {
    return this.eq(0);
};
$s.fn.last = function () {
    return this.eq(this.length - 1);
};
$s.fn.find = function (str) {
    var nodeList = [];
    var res = this.each(function () {
        return this.querySelectorAll(str);
    }, 1);
    if (res instanceof Array) {
        for (var i = 0; i < res.length; i++) {
            for (var j = 0; j < res[i].length; j++) {
                nodeList.push(res[i][j]);
            }
        }
    } else {
        nodeList = res;
    }
    return $s(nodeList);
};
$s.fn.parent = function () {
    return $s(this.each(function () {
        return this.parentNode;
    }, 1));
};
$s.fn.hide = function () {
    return this.each(function () {
        this.style.display = "none";
    });
};
$s.fn.show = function () {
    return this.each(function () {
        this.style.display = "";
    });
};
$s.fn.text = function (str) {
    if (str !== undefined) {
        return this.each(function () {
            this.innerText = str;
        });
    } else {
        return this.each(function () {
            return this.innerText;
        }, 1);
    }
};
$s.fn.html = function (str) {
    if (str !== undefined) {
        return this.each(function () {
            this.innerHTML = str;
        });
    } else {
        return this.each(function () {
            return this.innerHTML;
        }, 1);
    }
};
$s.fn.outHtml = function (str) {
    if (str !== undefined) {
        return this.each(function () {
            this.outerHTML = str;
        });
    } else {
        return this.each(function () {
            return this.outerHTML;
        }, 1);
    }
};
$s.fn.val = function (str) {
    if (str !== undefined) {
        return this.each(function () {
            this.value = str;
        });
    } else {
        return this.each(function () {
            return this.value;
        }, 1);
    }
};
$s.fn.css = function (key, value, important) {
    if (value !== undefined) {
        return this.each(function () {
            this.style.setProperty(key, value, important);
        });
    } else {
        return this.each(function () {
            return this.style.getPropertyValue(key);
        }, 1);
    }
};
$s.fn.attr = function (key, value) {
    if (value !== undefined) {
        return this.each(function () {
            this.setAttribute(key, value);
        });
    } else {
        return this.each(function () {
            return this.getAttribute(key);
        }, 1);
    }
};
$s.fn.removeAttr = function (key) {
    return this.each(function () {
        this.removeAttribute(key);
    });
};
$s.fn.remove = function () {
    return this.each(function () {
        this.remove();
    });
};
$s.fn.append = function (str) {
    return this.each(function () {
        this.insertAdjacentHTML('beforeend', str);
    });
};
$s.fn.prepend = function (str) {
    return this.each(function () {
        this.insertAdjacentHTML('afterbegin', str);
    });
};
$s.fn.hasClass = function (str) {
    return this.each(function () {
        return this.classList.contains(str);
    }, 1);
};
$s.fn.addClass = function (str) {
    return this.each(function () {
        return this.classList.add(str);
    });
};
$s.fn.removeClass = function (str) {
    return this.each(function () {
        return this.classList.remove(str);
    });
};
$s.fn.click = function (f) {//click改为监听事件，
    if (typeof (f) == "function") {//重载，若含有参数就注册事件，无参数就触发事件
        this.each(function () {
            this.addEventListener("click", f);
        });
    } else {
        this.each(function () {
            var event = document.createEvent('HTMLEvents');
            event.initEvent("click", true, true);
            this.dispatchEvent(event);
        });
    }
};
$s.fn.tag = function (tag) {
    this[0] = document.createElement(tag);
    return this;
};
$s.fn.dom = function (str) {
    var dom = document.createElement('p');
    dom.innerHTML = str;
    this[0] = dom.childNodes[0];
    return this;
};


$s.ajax = {
    get: function (url, fn, async) {
        // XMLHttpRequest对象用于在后台与服务器交换数据
        if (async === undefined) async = true;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, async);
        xhr.onreadystatechange = function () {
            // readyState == 4说明请求已完成
            if (xhr.readyState === 4 && xhr.status === 200 || xhr.status === 304) {
                // 从服务器获得数据
                fn.call(this, xhr.responseText);
            }
        };
        xhr.send();
    },
    // datat应为'a=a1&b=b1'这种字符串格式，在jq里如果data为对象会自动将对象转成这种字符串格式
    post: function (url, data, fn, async) {
        if (async === undefined) async = true;
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, async);
        // 添加http头，发送信息至服务器时内容编码类型
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && (xhr.status === 200 || xhr.status === 304)) {
                fn.call(this, xhr.responseText);
            }
        };
        xhr.send(data);
    }
};

$s.getUrlPra = function (paraName, location) {
    var url;
    if (location === undefined) url = document.location.toString();
    else url = location;
    var arrObj = url.split("?");
    if (arrObj.length > 1) {
        var arrPara = arrObj[1].split("&");
        var arr;
        for (var i = 0; i < arrPara.length; i++) {
            arr = arrPara[i].split("=");
            if (arr !== null && arr[0] === paraName) {
                return arr[1];
            }
        }
        return "";
    } else {
        return "";
    }
};//取得url的参数


$.url = {
    add: function (name, value) {
        var currentUrl = window.location.href.split('#')[0];
        if($s.getUrlPra(name,currentUrl)!==''){
            this.update(name,value);
            return;
        }
        if (/\?/g.test(currentUrl)) {
            if (/name=[-\w]{4,25}/g.test(currentUrl)) {
                currentUrl = currentUrl.replace(/name=[-\w]{4,25}/g, name + "=" + value);
            } else {
                currentUrl += "&" + name + "=" + value;
            }
        } else {
            currentUrl += "?" + name + "=" + value;
        }
        history.pushState(null, null, currentUrl);  //将网址设置
    },
    update: function (paramName, replaceWith) {
        var oUrl = window.location.href.toString();
        var re = eval('/(' + paramName + '=)([^&]*)/gi');
        var nUrl = oUrl.replace(re, paramName + '=' + replaceWith);
        this.location = nUrl;
        history.pushState(null, null, nUrl);  //将网址设置
    }
};

$s.cookie = {
    set: function (key, val, time, path) {//设置cookie方法
        if (path === undefined) path = "/";
        var date = new Date(); //获取当前时间
        date.setTime(date.getTime() + time * 24 * 3600 * 1000); //格式化为cookie识别的时间
        document.cookie = key + "=" + val + ";expires=" + date.toGMTString() + ";path=" + path;  //设置cookie
    },
    get: function (key) {//获取cookie方法
        /*获取cookie参数*/
        var getCookie = document.cookie.replace(/[ ]/g, "");  //获取cookie，并且将获得的cookie格式化，去掉空格字符
        var arrCookie = getCookie.split(";"); //将获得的cookie以"分号"为标识 将cookie保存到arrCookie的数组中
        var tips='';  //声明变量tips
        for (var i = 0; i < arrCookie.length; i++) {   //使用for循环查找cookie中的tips变量
            var arr = arrCookie[i].split("=");   //将单条cookie用"等号"为标识，将单条cookie保存为arr数组
            if (key === arr[0]) {  //匹配变量名称，其中arr[0]是指的cookie名称，如果该条变量为tips则执行判断语句中的赋值操作
                tips = arr[1];   //将cookie的值赋给变量tips
                break;   //终止for循环遍历
            }
        }
        return tips;
    }
};