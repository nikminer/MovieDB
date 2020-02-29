function search(elem){
    let groups=document.getElementsByClassName("group")
    for (let indexgroup=0; indexgroup<groups.length;indexgroup++){
        let films = groups[indexgroup].getElementsByClassName("filmname")
        for (let i=0; i<films.length;i++){
            if (elem.value.length>0){
                let parrent=findAncestor(films[i],"film")
                parrent.style.display ="none";
                if (films[i].innerText.toUpperCase().includes(elem.value.toUpperCase()))
                    parrent.style.display ="grid";
            }
            else
                findAncestor(films[i],"film").style.display ="grid";  
        }
    }
}
function findAncestor (el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
}