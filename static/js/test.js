const peerConnection = new RTCPeerConnection();

  // Add the video track to the peer connection
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
      const localVideo = document.createElement('video');
      localVideo.srcObject = stream;
      localVideo.muted = true;
      localVideo.play();
      document.body.appendChild(localVideo);
      stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));
    })
    .catch(error => console.error('Error accessing media devices:', error));

  // Listen for ICE candidates
  peerConnection.onicecandidate = event => {
    if (event.candidate) {
      socket.emit('candidate', event.candidate);
    }
  };

  peerConnection.ontrack = event => {
    const remoteVideo = document.getElementById('remoteVideo');
    remoteVideo.srcObject = event.streams[0];
    remoteVideo.play();
  };

  peerConnection.createOffer()
  .then(offer => {
    return peerConnection.setLocalDescription(offer);
  })
  .then(() => {
    socket.emit('offer', peerConnection.localDescription);
  })
  .catch(error => console.error('Error creating or setting local description:', error));

// Handle SDP answer from the server
socket.on('answer', answer => {
  peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
});

// Handle ICE candidates from the server
socket.on('candidate', candidate => {
  peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
});