function drag(ev){
    ev.dataTransfer.setData('text/plain',null)
    if (ev.currentTarget.className=="film")
        ev.dataTransfer.setData("id", ev.currentTarget.id);

    faststatus.style.opacity=1
    faststatus.style.zIndex=0;
}

function drop(ev) {
    ev.preventDefault()
    
    Group=null
    if (ev.currentTarget.className=="group"){
        Group=ev.currentTarget;
    }
    
    if (Group!=null) 
        sendStatus(ev.dataTransfer.getData("id"),Group,Group.id)
}

function droptoPlan(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("planned"),"planned")
}

function droptoWatch(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("watch"),"watch")
}

function droptoWatched(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("watched"),"watched")
}

function droptoRewatch(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("rewatch"),"rewatch")
}

function droptoDrop(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("drop"),"drop")
}

function sendStatus(id,Group,status){
    var xhr = new XMLHttpRequest()
    xhr.open('POST','/film/set/status',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xhr.send("listid="+encodeURIComponent(id.split(':')[1])+";status="+encodeURIComponent(status))
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4)
            if (JSON.parse(xhr.response)['status']=="changestatus")
                moveitem(id,Group)
    }
}

function moveitem(id,Group){

    if (Group.children[1].className!="legend")
        Group.innerHTML+="<div class='legend'><span>Название</span><span>Оценка</span></div>"
    
    Group.appendChild(document.getElementById(id))

    if (Group.children[1].className=="simplespan")
        Group.removeChild(Group.children[1])

    Groups=document.getElementsByClassName("group")
    for (var i=0 ;i< Groups.length;i++)
        if (Groups[i].children.length==2 && Groups[i].children[1].className=="legend"){
            Groups[i].children[1].remove()
            Groups[i].innerHTML+="<span class=simplespan>Пусто</span>"
        }
}

function allowDrop(ev) {
    ev.preventDefault()
}