socket.on('message', function(data) {
    document.getElementById("message-list").innerHTML +=
              "<p><b>"+data.sender+"</b>: "+data.message+' <font class="small" color="grey">'+data.time+"</font></p>";
    
    //делает так чтобы сообщения показывались снизу
    var element = document.getElementById("message-list");
    element.scrollTop = element.scrollHeight;
  });

  $(function() {
    $('#message-form').submit(function(event) {
      event.preventDefault();
      var messageInput = $('#message-input');
      if(messageInput.val() !== ""){
        var message = messageInput.val();
        var user_id_receiverInput = $('#user_id_receiver');
        var user_id_receiver = user_id_receiverInput.val();

        //const file = document.getElementById("myFile").files;
        //let formData = new FormData();
        
        //var totalfiles = document.getElementById('myFile').files.length;
        //for (var index = 0; index < totalfiles; index++) {
         // formData.append("files[]", document.getElementById('myFile').files[index]);
        //}

        //fetch('/files', {method: "POST", body:formData});
        //const previewImage = document.getElementById("img-preview");
        //previewImage.src = "/" + file.name;

        messageInput.val('');
        socket.emit('send', { message: message, user_id_receiver: user_id_receiver});
      }
    });
  });

 
  
  //делает так чтобы сообщения показывались снизу
  var element = document.getElementById("message-list");
  element.scrollTop = element.scrollHeight;