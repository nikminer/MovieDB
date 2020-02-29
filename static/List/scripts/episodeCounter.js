
function setepisode(id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/serial/season/num/set',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id)+";count="+document.getElementById("numerinput_"+id).value);
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4){
            episode=JSON.parse(xhr.response)['userepisode']
            document.getElementById("userepisodeview_"+id).innerText= episode
            document.getElementById("numerinput_"+id).value= episode
        }
    }
}
function increment(id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/serial/season/num/inc',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id));
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4){
            episode=JSON.parse(xhr.response)['userepisode']
            document.getElementById("userepisodeview_"+id).innerText= episode
            document.getElementById("numerinput_"+id).value= episode
        }
    }
}
function decrement(id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/serial/season/num/dec',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id));
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4){
            episode=JSON.parse(xhr.response)['userepisode']
            document.getElementById("userepisodeview_"+id).innerText= episode
            document.getElementById("numerinput_"+id).value= episode
        }
    }
}