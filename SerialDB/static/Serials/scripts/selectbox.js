window.onload = function() {
    for (var i=1; i<selectbox.children.length;i++){
        if (selectbox.children[i].selected){
            selectName.innerText=selectbox.children[i].label;
            break;
        }
    }
};

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setstatus(elem,id){
    if (!elem.selected){
        var xhr = new XMLHttpRequest();
        xhr.open('POST','/serial/season/set/status',true);
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send("listid="+id+";status="+encodeURIComponent(elem.value));
        selectName.innerText=elem.label;
    }
    selectbox.open=false
}