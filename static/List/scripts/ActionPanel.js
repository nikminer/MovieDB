async function setRating(obj, id){
     await fetch("/list/set/rating",{
        method: 'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "listid="+encodeURIComponent(id)+";rating="+ obj.value
     });
}

async function setReWatch(id, status){
     let request = await fetch("/list/rewatch",{
        method: 'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "listid="+encodeURIComponent(id)+";status="+status
     });

     if (request.ok){
         console.log(await request.text())
     }
}

