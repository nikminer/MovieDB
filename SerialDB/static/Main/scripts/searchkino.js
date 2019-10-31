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

function search(elem){
    
    if (elem.value.length>2){
        var xhr = new XMLHttpRequest();
        xhr.open('POST','/add/kinopoisk/search/',true);
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send("name="+elem.value);
        xhr.onreadystatechange=function(){
            if(xhr.status==200 && xhr.readyState==4){
                result.innerHTML="";
                resp=JSON.parse(xhr.response)
                console.log(resp)
                for (var i in resp['serials']['result']){
                    var serial=document.createElement("a")
                    var results=resp['serials']

                    var lable=document.createElement("span")
                    lable.innerHTML="Сериал"
                    serial.appendChild(lable)
                    var poster=document.createElement("img")
                    poster.src=results['result'][i]['poster'];
                    poster.className="poster"
                    serial.appendChild(poster)

                    var title=document.createElement("span")
                    title.innerHTML=results['result'][i]['name']+"/"+results['result'][i]['originalname']+" ("+results['result'][i]['year']+")"
                    title.className="postertitle"
                    serial.appendChild(title)
                    serial.href="kinopoisk/"+results['result'][i]['id']
                    serial.title=results['result'][i]['name']+"/"+results['result'][i]['originalname']+" ("+results['result'][i]['year']+")"
                    serial.className="Movie"
                    result.appendChild(serial)
                }

                for (var i in resp['films']['result']){
                    var serial=document.createElement("a")
                    var results=resp['films']

                    var lable=document.createElement("span")
                    lable.innerHTML="Фильм"
                    serial.appendChild(lable)
                    var poster=document.createElement("img")
                    poster.src=results['result'][i]['poster'];
                    poster.className="poster"
                    serial.appendChild(poster)

                    var title=document.createElement("span")
                    title.innerHTML=results['result'][i]['name']+"/"+results['result'][i]['originalname']+" ("+results['result'][i]['year']+")"
                    title.className="postertitle"
                    serial.appendChild(title)
                    serial.href="kinopoisk/"+results['result'][i]['id']
                    serial.title=results['result'][i]['name']+"/"+results['result'][i]['originalname']+" ("+results['result'][i]['year']+")"
                    serial.className="Movie"
                    result.appendChild(serial)
                }     
            }
        }
    }else
        result.innerHTML="";
}