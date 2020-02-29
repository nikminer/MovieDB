function drag(ev){
    ev.dataTransfer.setData('text/plain',null)

    if (ev.currentTarget.className=="season"){
        ev.dataTransfer.setData("id", ev.currentTarget.id);
        ev.dataTransfer.setData("type", "season");
    }
    else if (ev.currentTarget.className == "allseason"){
         ev.dataTransfer.setData("id", ev.currentTarget.id);
         ev.dataTransfer.setData("type", "allseason");
    }

    faststatus.style.opacity=1;
    faststatus.style.zIndex=0;
    
}

function drop(ev) {
    ev.preventDefault();
    let Group=null
    if (ev.currentTarget.className=="group"){
            Group=ev.currentTarget;
    }

    if (Group!=null)
        sendStatus(ev.dataTransfer.getData("id"),Group,ev.dataTransfer.getData("type"))
}

function droptoPlan(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("planned"),ev.dataTransfer.getData("type"))
}

function droptoWatch(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("watch"),ev.dataTransfer.getData("type"))
}

function droptoWatched(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("watched"),ev.dataTransfer.getData("type"))
}

function droptoRewatch(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("rewatch"),ev.dataTransfer.getData("type"))
}

function droptoDrop(ev){
    ev.preventDefault()
    sendStatus(ev.dataTransfer.getData("id"),document.getElementById("drop"), ev.dataTransfer.getData("type"))
}

function sendStatus(id,Group,DataType){
    let list = [];

    if(DataType=="season")
        list.push(id.split(':')[1]);
    else if(DataType=="allseason"){
        let seasons = document.getElementById(id).parentElement.getElementsByClassName("season");
        for (let i=0;i<seasons.length;i++)
            list.push(seasons[i].id.split(':')[1]);
    }

    let xhr = new XMLHttpRequest()
    xhr.open('POST','/serial/season/set/status',true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xhr.send("listid="+encodeURIComponent(list.join(';'))+";status="+encodeURIComponent(Group.id))
    xhr.onreadystatechange=function(){
        if(xhr.status==200 && xhr.readyState==4)
            if (JSON.parse(xhr.response)['status']=="changestatus"){
                moveitem(list,Group);
            }
    }
}

function moveitem(list,Group){
    for (let i=0;i<list.length;i++){
        let DropItem=document.getElementById("season:"+list[i])
        let Parrentelm=DropItem.parentElement
        let serialid=Group.id+"_"+Parrentelm.id.split('_')[1];

         if (document.getElementById(serialid)==null){
            let SerialDetails=document.createElement("details")

            SerialDetails.className="serial"
            SerialDetails.id=serialid
            SerialDetails.appendChild(Parrentelm.children[0].cloneNode(true))

            SerialDetails.appendChild(DropItem)

            let allitems = document.createElement("div")
            allitems.className="allseason";
            allitems.id="all:"+serialid;
            allitems.ondragend =function (){
                faststatus.style.zIndex=-10;
                faststatus.style.opacity=0;
            }

            allitems.draggable=true;
            allitems.ondragstart=drag;
            allitems.innerHTML="<a>Переместить все сезоны</a>";
            SerialDetails.appendChild(allitems)

            Group.appendChild(SerialDetails)

        }
        else{
             let Parentelem = document.getElementById(serialid)
             Parentelem.insertBefore(DropItem,Parentelem.getElementsByClassName('allseason')[0])
        }

        if (Parrentelm.children.length<=2)
            Parrentelm.remove();
    }




    let Groups=document.getElementsByClassName("group")
    for (var i=0 ;i< Groups.length;i++){
        if (Groups[i].children.length<=1)
            Groups[i].innerHTML+="<span class=simplespan>Пусто</span>";
        if (Groups[i].children[1].className == "simplespan" && Groups[i].children.length!=2)
            Groups[i].children[1].remove()
    }

}


function allowDrop(ev) {
    ev.preventDefault();
}