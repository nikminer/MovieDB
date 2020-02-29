function setRating(obj,id){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/serial/season/set/rating',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id)+";rating="+obj.value);
}