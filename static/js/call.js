var mediaConstraints = {
    audio: true, // We want an audio track
    video: true // ...and we want a video track
};

function sendToServer(msg) {
    socket.emit('connection', { msg:msg});
}

let pc;

const iceServers = {
        'iceServers': [
          {'urls': 'stun:stun.l.google.com:19302'},
          {'urls': 'turn:turn.example.com:3478', 'credential': 'password', 'username': 'username'}
        ]
};

navigator.mediaDevices.getUserMedia({video: true})
        .then(stream => {
          localStream = stream;
          document.getElementById("videoElement").setAttribute('autoplay', '');
          document.getElementById("videoElement").style.width = '200px';
          document.getElementById("videoElement").style.height = '200px';
          document.getElementById("videoElement").srcObject = localStream;
          pc = new RTCPeerConnection(iceServers);
          pc.addStream(stream);
          pc.onicecandidate = event => {
            if (event.candidate) {
                debugger
              socket.emit('candidate', event.candidate);
            }
          };
          pc.onaddstream = event => {
            document.getElementById("second_video").setAttribute('autoplay', '');
            document.getElementById("second_video").style.width = '200px';
            document.getElementById("second_video").style.height = '200px';
            document.getElementById("second_video").srcObject = event.stream;
          };
          socket.on('offer', data => {
            if(document.getElementById("user_id_sender").value == data.target){
                pc.setRemoteDescription(new RTCSessionDescription(data));
                pc.createAnswer()
                .then(answer => {
                    pc.setLocalDescription(answer);
                    socket.emit('answer', {target: document.getElementById("user_id_receiver").value, answer:answer});
                })
                .catch(error => {
                    console.log(error);
                });
            }
          });
          socket.on('answer', data => {
            if(document.getElementById("user_id_sender").value == data.target){
                pc.setRemoteDescription(new RTCSessionDescription(data));
            }
          });
          socket.on('candidate', data => {
            pc.addIceCandidate(new RTCIceCandidate(data));
          });
        })
        .catch(error => {
          console.log(error);
});

function call_call() {
    pc.createOffer()
      .then(offer => {
        pc.setLocalDescription(offer);
        socket.emit('offer', {target: document.getElementById("user_id_receiver").value, offer:offer});
      })
      .catch(error => {
        console.log(error);
      });
}


function call(){
    $("#videoElement").hide();
    $("#call_buttons").hide();
    $("#second_video").hide();

    var receiver = $('#user_id_receiver').val();
    socket.emit('send_id', { user_id:receiver});

    socket.on('send_login', function(event) {

        $('#header_text').text("Звонок пользователю "+ event.login)
    
    });

    var user_id_sender = document.getElementById("user_id_sender");
    var user_id_receiver = document.getElementById("user_id_receiver");
    socket.emit('call', { user_id_sender:user_id_sender.value,user_id_receiver:user_id_receiver.value});

    call_call();
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
    $("#second_video").show();
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
            $("#second_video").show();
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
      
    //   console.clear(); // clear console on each update
    //   console.log(`${hours}:${minutes}:${seconds}`); // display the elapsed time
      $('#header_text').text(hours+":"+minutes+":"+seconds)}, 1000); // update every second
  }