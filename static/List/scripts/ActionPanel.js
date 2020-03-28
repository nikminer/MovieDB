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
     let request = await fetch("/list/set/rewatch",{
        method: 'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "listid="+encodeURIComponent(id)+";status="+status+(status=='set'?';count='+document.getElementById('numerinputRewatch_'+id).value:'')
     });
     if (request.ok){
         let response = await request.json();
         if (response.status){
             document.getElementById('numerinputRewatch_'+id).value=response.rewatch;
             let span = document.getElementById("userRewatch_"+id);
             if (span) span.innerText="Повторных просмотров: "+response.rewatch;
         }
     }
}

async function setEpisode(id, status){
     let request = await fetch("/list/set/episode",{
        method: 'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "listid="+encodeURIComponent(id)+";status="+status+(status=='set'?';count='+document.getElementById('numerinput_'+id).value:'')
     });
     if (request.ok){
         let response = await request.json();
         if (response.status){
             document.getElementById('numerinput_'+id).value=response.userepisode;
             let span = document.getElementById("userepisodeview_"+id);
             if (span) span.innerText=response.userepisode;
         }
     }
}

