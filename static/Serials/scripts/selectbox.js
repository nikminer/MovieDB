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

async function setstatus(elem,id){
    if (!elem.selected) {
        let request = await fetch("/list/set/status", {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                "X-CSRFToken": getCookie("csrftoken"),
                'Content-Type': 'application/x-www-form-urlencoded'
            },

            body: "listid=" + encodeURIComponent(id) + "&status=" + encodeURIComponent(elem.value)
        });

        if (request.ok) {
            let response = await request.json();
            if (response.status) {

                Array.prototype.filter.call(
                    selectbox.getElementsByTagName('option'),
                    function (item) {
                        return item.selected
                    }
                )[0].selected = false;

                elem.selected = true;
                selectName.innerText = elem.label;
            }
        }
    }
    selectbox.open=false
}