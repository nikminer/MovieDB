function search(elem){
    let groups=document.getElementsByClassName("group")
    for (let indexgroup=0; indexgroup<groups.length;indexgroup++){
        let serials = groups[indexgroup].getElementsByClassName("itemname")
        for (let i=0; i<serials.length;i++){
            if (elem.value.length>0){
                let parrentNode=findAncestor(serials[i],"item")
                parrentNode.style.display ="none";
                if (serials[i].innerText.toUpperCase().includes(elem.value.toUpperCase()))
                    parrentNode.style.display ="flex";
            }
            else
                findAncestor(serials[i],"item").style.display ="flex";
        }
    }
}

function findAncestor (el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
}