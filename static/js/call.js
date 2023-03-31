var mediaConstraints = {
  audio: true, // We want an audio track
  video: true // ...and we want a video track
};

function sendToServer(msg) {
  socket.emit('connection', { msg:msg});
}

function createPeerConnection() {
    myPeerConnection = new RTCPeerConnection({
        iceServers: [     // Information about ICE servers - Use your own!
          {
            urls: "stun:stun.l.google.com:19302"
          }
        ]
    });
  
    myPeerConnection.onicecandidate = handleICECandidateEvent;
    myPeerConnection.ontrack = handleTrackEvent;
    myPeerConnection.onnegotiationneeded = handleNegotiationNeededEvent;
    //myPeerConnection.onremovetrack = handleRemoveTrackEvent;
    //myPeerConnection.oniceconnectionstatechange = handleICEConnectionStateChangeEvent;
    //myPeerConnection.onicegatheringstatechange = handleICEGatheringStateChangeEvent;
    //myPeerConnection.onsignalingstatechange = handleSignalingStateChangeEvent;
}

function handleGetUserMediaError(e) {
    switch(e.name) {
      case "NotFoundError":
        alert("Unable to open your call because no camera and/or microphone" +
              "were found.");
        break;
      case "SecurityError":
      case "PermissionDeniedError":
        // Do nothing; this is the same as the user canceling the call.
        break;
      default:
        alert("Error opening your camera and/or microphone: " + e.message);
        break;
    }
}

function handleNegotiationNeededEvent() {
    myPeerConnection.createOffer().then(function(offer) {
      return myPeerConnection.setLocalDescription(offer);
    })
    .then(function() {

      var msg = {
          name: document.getElementById("user_id_sender").value,
          target: document.getElementById("user_id_receiver").value,
          type: "video-offer",
          sdp: myPeerConnection.localDescription
        };

      sendToServer(msg);
  })
  .catch(reportError);
}

socket.on('handleVideoOfferMsg', function(msg) {

    var user_id_sender = document.getElementById("user_id_sender").value;
    if(user_id_sender == msg.msg.target){
        targetUsername = msg.msg.name;
        createPeerConnection();
    
        var desc = new RTCSessionDescription(msg.msg.sdp);
    
        myPeerConnection.setRemoteDescription(desc).then(function () {
            return navigator.mediaDevices.getUserMedia(mediaConstraints);
        })
        .then(function(localStream) {
            $("#videoElement").show();
            document.getElementById("videoElement").setAttribute('autoplay', '');
            document.getElementById("videoElement").style.width = '200px';
            document.getElementById("videoElement").style.height = '200px';
            document.getElementById("videoElement").srcObject = localStream;
    
            localStream.getTracks().forEach(track => myPeerConnection.addTrack(track, localStream));
        })
        .then(function() {
            return myPeerConnection.createAnswer();
        })
        .then(function(answer) {
            return myPeerConnection.setLocalDescription(answer);
        })
        .then(function() {
            var msg = {
                name: document.getElementById("user_id_sender").value,
                target: document.getElementById("user_id_receiver").value,
                type: "video-answer",
                sdp: myPeerConnection.localDescription
            };
            sendToServer(msg);
        })
        .catch(handleGetUserMediaError);
        }
});

socket.on('handleVideoAnswerMsg', function(msg) {

    var user_id_sender = document.getElementById("user_id_sender").value;
    if(user_id_sender == msg.msg.target){
        myPeerConnection.setRemoteDescription(new RTCSessionDescription(msg.msg.sdp));
    }
});

function handleICECandidateEvent(event) {
  if (event.candidate) {
    sendToServer({
      type: "new-ice-candidate",
      target: document.getElementById("user_id_receiver").value,
      candidate: event.candidate
    });
  }
}

socket.on('handleNewICECandidateMsg', function(msg) {

    var candidate = new RTCIceCandidate(msg.msg.candidate);
    myPeerConnection.addIceCandidate(candidate)
    .catch(reportError);

});

function handleTrackEvent(event) {
    // document.getElementById("second_video").srcObject = event.streams[0];
    // document.getElementById("second_video").style.width = '200px';
    // document.getElementById("second_video").style.height = '200px';
    var video = document.querySelector("#second_video");
    video.srcObject = event.streams[0]
    // video.setAttribute('playsinline', '');
    video.setAttribute('autoplay', '');
    // video.setAttribute('muted', '');
    video.style.width = '200px';
    video.style.height = '200px';
    $("#second_video").show();

    var qwe = document.getElementById("second_video");
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

  createPeerConnection();

  navigator.mediaDevices.getUserMedia(mediaConstraints)
  .then(function(localStream) {
    document.getElementById("videoElement").setAttribute('autoplay', '');
    document.getElementById("videoElement").style.width = '200px';
    document.getElementById("videoElement").style.height = '200px';
    document.getElementById("videoElement").srcObject = localStream;

    localStream.getTracks().forEach(track => myPeerConnection.addTrack(track, localStream));
    socket.emit('send_answer', { answer:true, user_id_receiver:user_id_receiver.value, user_id_sender:user_id_sender.value});
  })
  .catch(handleGetUserMediaError);
}

socket.on('receive_answer', function(event) {
  
  var user_id_sender = document.getElementById("user_id_sender").value;
  if(user_id_sender == event.receiver){
      $("#loader").hide();
      if(event.answer == false){
          console.log("dfsgverbhe")
          $('#body_text').text(event.sender+" не отвечает")
      }
      else if(event.answer == true){  
          console.log("dfsgverbhe")
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
    $('#header_text').text(hours+":"+minutes+":"+seconds)
  }, 1000); // update every second
}