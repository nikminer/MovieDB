function getImage(input){
    if (input.files.length==1 && input.files[0].type.match("image")){
        var filereader= new FileReader()
        filereader.onload = function (e) {
            previewposter.src=e.target.result
        }
        filereader.readAsDataURL(input.files[0])
        
        console.dir(filereader)
    }   

}