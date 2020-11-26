function randomString(len) {
    len = len || 32;
    var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
    var maxPos = $chars.length;
    var pwd = '';
    for (i = 0; i < len; i++) {
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}
function getRandomText(){ 
    eval( "var word=" +  '"\\u' + (Math.round(Math.random() * 20901) + 19968).toString(16)+'"')//生成随机汉字
    return word;
  }
let msgOK = (s) => {
    Toastify({
        text: s,
        duration: 3000,
        backgroundColor: "linear-gradient(to right, #00b09b, #00b09b)",
    }).showToast();
}
let msgFail = (s) => {
    Toastify({
        text: s,
        duration: 3000,
        backgroundColor: "linear-gradient(to right, #EF100F, #EF100F)",
    }).showToast();
}