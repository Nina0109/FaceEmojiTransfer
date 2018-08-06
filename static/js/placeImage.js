function change() {
	var pic = document.getElementById("preview"),
	    file = document.getElementById("f");
  
	var ext=file.value.substring(file.value.lastIndexOf(".")+1).toLowerCase();
	console.log(file.value);
	console.log(ext);

     // Check file type
    if(ext!='png'&&ext!='jpg'&&ext!='jpeg'){
         alert("Must be a .jpg or .png or .jpeg file"); 
		 return;
    }
	html5Reader(file); 
}

 function html5Reader(file){
     var file = file.files[0];
     var reader = new FileReader();
     reader.readAsDataURL(file);
     reader.fileName = file.name;
     reader.onload = function(e){
         var pic = document.getElementById("preview");
         console.log(this.fileName);
         console.log(this.result);
         pic.src=this.result;
         var imgMsg={name:this.fileName,
         			 base64:this.result}
         // send(imgMsg);

     }
 }

function send(imgMsg){         
        var submitArr = [];
        //console.log(imgMsg.name);
        //console.log(imgMsg.base64);        
        submitArr.push(imgMsg);
        // console.log('提交的数据：'+JSON.stringify(submitArr))   
        $.ajax({      
            url : 'https://www.baidu.com',      
            type : 'POST',   
            data : JSON.stringify(submitArr),      
            dataType: 'json',
            //processData: false,   用FormData传fd时需有这两项      
            //contentType: false,      
            success : function(data){      
                console.log('Data returned back：'+JSON.stringify(data))      
          　},  
            error : function(data){
            	console.log("enenene")
            	console.log(data);
            }
  
        });      
    }      

