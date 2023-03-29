function call(){
    $("#videoElement").hide();
    $("#call_buttons").hide();

    var receiver = $('#user_id_receiver').val();
    socket.emit('send_id', { user_id:receiver});

    socket.on('send_login', function(event) {

        $('#header_text').text("Звонок пользователю "+ event.login)
    
    });

    var user_id_sender = document.getElementById("user_id_sender");
    var user_id_receiver = document.getElementById("user_id_receiver");
    socket.emit('call', { user_id_sender:user_id_sender.value,user_id_receiver:user_id_receiver.value});
}

socket.on('user_call', function(event) {

    var user_id_sender = document.getElementById("user_id_sender").value;
    if(user_id_sender == event.receiver){
        $("#loader").hide();
        $("#call_buttons").show();

        $('#header_text').text(event.caller+" вызывает")
        $('#call_window').modal('show')
    }

});

function decline(){
    $('#call_window').modal('hide')
    var user_id_sender = document.getElementById("user_id_sender");
    var user_id_receiver = document.getElementById("user_id_receiver");
    socket.emit('send_answer', { answer:false, user_id_receiver:user_id_receiver.value, user_id_sender:user_id_sender.value});
}

function accept(){
    startTimer();
    $("#call_buttons").hide();
    $("#videoElement").show();
    var user_id_sender = document.getElementById("user_id_sender");
    var user_id_receiver = document.getElementById("user_id_receiver");
    socket.emit('send_answer', { answer:true, user_id_receiver:user_id_receiver.value, user_id_sender:user_id_sender.value});
}

socket.on('receive_answer', function(event) {
    
    var user_id_sender = document.getElementById("user_id_sender").value;
    if(user_id_sender == event.receiver){
        $("#loader").hide();
        if(event.answer == false){
            $('#body_text').text(event.sender+" не отвечает")
        }
        else if(event.answer == true){  
            startTimer();  
            $("#videoElement").show();
        }
    }

});

function startTimer() {
    let startTime = Date.now(); // record the start time
    
    setInterval(function() {
      let elapsedTime = Date.now() - startTime; // calculate elapsed time
      let hours = Math.floor(elapsedTime / 3600000); // calculate hours
      let minutes = Math.floor((elapsedTime % 3600000) / 60000); // calculate minutes
      let seconds = Math.floor((elapsedTime % 60000) / 1000); // calculate seconds
      
      // add leading zero if necessary
      hours = hours < 10 ? '0' + hours : hours;
      minutes = minutes < 10 ? '0' + minutes : minutes;
      seconds = seconds < 10 ? '0' + seconds : seconds;
      
      console.clear(); // clear console on each update
      console.log(`${hours}:${minutes}:${seconds}`); // display the elapsed time
      $('#header_text').text(hours+":"+minutes+":"+seconds)
    }, 1000); // update every second
  }