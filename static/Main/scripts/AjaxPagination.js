
async function getPages(elem, nextpage) {
    let request = await fetch(nextpage,{
        method: 'GET',
        headers:{
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
    if (request.ok){
        let temp=elem.parentElement.parentElement;
        elem.parentElement.remove();
        temp.innerHTML+=await request.text();
    }
}