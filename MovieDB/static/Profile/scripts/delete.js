

function deleteNoti(obj){
    
    var xhr = new XMLHttpRequest()
    xhr.open('POST','/profile/noties/del',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xhr.send("id="+obj.id)

    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4)
            if (JSON.parse(xhr.response)["resp"])
                obj.parentElement.removeChild(obj)
    }
}