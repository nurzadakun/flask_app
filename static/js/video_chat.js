$(document).ready(() => {
    var localStream;

    $("#turnOnCamera").click(() => {
      var video = document.querySelector("#videoElement");
      // video.setAttribute('playsinline', '');
      video.setAttribute('autoplay', '');
      // video.setAttribute('muted', '');
      video.style.width = '200px';
      video.style.height = '200px';
      if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
          localStream = stream;
          video.srcObject = stream;
        })
        .catch(function (err0r) {
          console.log("Something went wrong!");
        });
      }
    });
});