
function setrewatch(id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/film/rewatch/set',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id)+";count="+document.getElementById("numerinputRewatch_"+id).value);
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4){
            let rewatch=JSON.parse(xhr.response)['countreview'];
            document.getElementById("userRewatch_"+id).innerText= rewatch;
            document.getElementById("numerinputRewatch_"+id).value= rewatch;
        }
    }
}

function incrementrewatch(id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/film/rewatch/inc',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id));
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4){
            let rewatch=JSON.parse(xhr.response)['countreview'];
            document.getElementById("userRewatch_"+id).innerText= rewatch;
            document.getElementById("numerinputRewatch_"+id).value= rewatch;
        }
    }
}
function decrementrewatch(id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/film/rewatch/dec',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id));
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4){
            let rewatch=JSON.parse(xhr.response)['countreview'];
            document.getElementById("userRewatch_"+id).innerText= rewatch;
            document.getElementById("numerinputRewatch_"+id).value= rewatch;
        }
    }
}