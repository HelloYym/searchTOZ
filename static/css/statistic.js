var log = (function() {

    function imageRequest(url) {
        var id = '_rpLog-' + (new Date()).getTime(),
            img = new Image();
        window[id] = img;

        img.onload = img.onerror = function() {
            window[id] = null
        };

        img.src = url;
        img = null;
    }


    function _extend(prev, add) {
        var result = prev || {},
            i;

        for(i in add) {
            if(add.hasOwnProperty(i)) {
                result[i] = add[i];
            }
        }
        return result;
    }

    function send(url, options, callback) {
        var defaultOption = {
            logid: 0,
            version: 0,
            prod_id: 'rp',
            plate_url: encodeURIComponent(window.location.href),
            referrer: encodeURIComponent(document.referrer),
            time: (new Date()).getTime()
        },
        newOption = defaultOption,
        params = [],
        property,
        targetUrl = url;

        if(targetUrl.charAt(targetUrl.length-1) !== '?') {
            targetUrl += '?';
        }

        for(var i = 1, iLen = arguments.length; i < iLen; i++) {
            if( Object.prototype.toString.call( arguments[i] ) === '[object Object]' ) {
                newOption = _extend(newOption, arguments[i]);
            }
        }

        for(var property in newOption) {
            params.push(property + '=' + newOption[property] );
        }

        imageRequest(targetUrl + params.join('&'));

        if( Object.prototype.toString.call( arguments[arguments.length - 1] ) === '[object Function]' ) {
            arguments[arguments.length - 1].call();
        }

    }

    return {
        send: send
    };

})();

(function(){
	var params = {};
	var location = window.location;
	if(document){
		params.url = location.href || '';
	}
	var args = '';
	for(var i in params){
		if(args != ''){
			args += '&';
		}
		args += i + '=' + encodeURIComponent(params[i]);
	}
	var img = new Image();
	var t = new Date().getTime();
	img.onload = img.onerror = img.onabort = function() {
		img.onload = img.onerror = img.onabort = null;
		try {
			img = null;
		} catch (e) {
			//完成后销毁生成的图片对象
			img = null;
		}
	}
	if(location.port){
		img.src =  location.protocol + "//" + location.hostname + ":" + location.port  +"/static/img/cse.gif?" + args + '&r=' + t;
	}else{
		img.src =  location.protocol + "//" + location.hostname + "/static/img/cse.gif?" + args + '&r=' + t;
	}
})();