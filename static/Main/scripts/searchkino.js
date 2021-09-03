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

async function searchTMDB(){
    elem = document.getElementById("searchbox");

    let request = await fetch("/add/tmdb/search/",{
        method: 'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "name="+elem.value
     });

    if (request.ok)
        results.innerHTML=await request.text();
}

async function searchOnMWL(){
    elem = document.getElementById("searchbox");

    let request = await fetch("/search/"+elem.value,{
        method: 'GET', 
     });

    if (request.ok)
        results.innerHTML=await request.text();
}

function onchangeInputSearch(){
    searchBtn.disabled = searchbox.value.length == 0
}