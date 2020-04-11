

function drag(ev){
    ev.dataTransfer.setData('text/plain',null)

    if (ev.currentTarget.className==="season" && ev.dataTransfer.getData("id")===""){
        ev.dataTransfer.setData("id", ev.currentTarget.id);
        ev.dataTransfer.setData("type", "season");
    }

    if (ev.currentTarget.className === "item" && ev.dataTransfer.getData("id")===""){
         ev.dataTransfer.setData("id", ev.currentTarget.id);
         ev.dataTransfer.setData("type", "item");
    }

    faststatus.style.opacity=1;
    faststatus.style.zIndex=0;

}

function drop(ev) {
    ev.preventDefault();
    if (ev.currentTarget.className==="group")
        sendStatus(ev.dataTransfer.getData("id"),ev.currentTarget.id,ev.dataTransfer.getData("type"))
}
function fastdrop(ev,groupname) {
    sendStatus(ev.dataTransfer.getData("id"),groupname,ev.dataTransfer.getData("type"))
}

function allowDrop(ev) {
    ev.preventDefault();
}


async function sendStatus(id,Groupid,DataType){
    let list = [];

    if(DataType==="season")
        list.push(id);
    else if(DataType==="item"){
        let seasons = document.getElementById(id).getElementsByClassName("season");
        if (seasons.length>0)
            for (let i=0;i<seasons.length;i++)
                list.push(seasons[i].id);
        else
            list.push(id);
    }

    if (id.split(':')[0] === Groupid){
        return;
    }

    let request = await fetch("/list/set/status",{
        method: 'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded'
        },

        body: "listid="+encodeURIComponent(list.join(';'))+";status="+ encodeURIComponent(Groupid)
     });
     if (request.ok){
         let response = await request.json();
         if (response.status){
             moveitem(id,response.userstatus);
         }
     }
}

function moveitem(itemid, userstatus){
    MovedItem = document.getElementById(itemid)
    TargetGroup = document.getElementById(userstatus);

    let scrolledElem = MovedItem;

    if (MovedItem.className==="item"){
        let newid= [TargetGroup.id,MovedItem.id.split(':')[1]].join(':');

        if (document.getElementById(newid)){
            let target=document.getElementById(newid);
            let seasons = MovedItem.getElementsByClassName('season');
            while (seasons.length>0)
                target.insertAdjacentElement('beforeend',seasons[0]);

            scrolledElem=target;
            MovedItem.remove();
        }

        else{
            TargetGroup.children[0].insertAdjacentElement('afterend',MovedItem)
            if (MovedItem.id.split(':').length>1)
                MovedItem.id= newid;
        }
    }
    else if (MovedItem.className==="season"){
        let newid= [TargetGroup.id,MovedItem.parentElement.id.split(':')[1]].join(':');
        let parent=MovedItem.parentElement;

        if (document.getElementById(newid)){
            let target=document.getElementById(newid)

            target.insertAdjacentElement('beforeend',MovedItem);
        }

        else {
            let newparent=parent.cloneNode(false);
            newparent.appendChild(parent.getElementsByClassName('itemheader')[0].cloneNode(true));
            newparent.appendChild(MovedItem);
            newparent.id=newid;
            TargetGroup.insertAdjacentElement('beforeend',newparent);
        }

        if (parent.children.length<=1)
            parent.remove();
    }

    scrolledElem.scrollIntoView({ block: 'center',  behavior: 'auto' });

    for (let i of document.getElementsByClassName("group") ){
        if (i.children.length<2)
           i.innerHTML+="<span class=simplespan>Пусто</span>";
        if (i.children.length!==2 &&  i.getElementsByClassName("simplespan").length>0){
            i.getElementsByClassName("simplespan")[0].remove()
        }
    }
}


