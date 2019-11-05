
function setRating(obj,id){
    var xhr = new XMLHttpRequest();
    xhr.open('POST','/film/set/rating',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("listid="+encodeURIComponent(id)+";rating="+obj.value);
}