
$(function(){
    if (hasGetUserMedia()) {
        initCapture();
        handleScreenshots();
    } else {
        alert("getUserMedia() is not supported by your browser");
    }

});


function hasGetUserMedia() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

function initCapture() {
    console.log("Starting capture...");
    const constraints = {
        video: true,
    };

    const video = document.querySelector("video");

    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
    });

    // Begin capturing every second
    const interval = setInterval(function() {
        let image64 = getScreenshot();
        console.log(image64);
    }, 1000);
}

function handleScreenshots() {
    const screenshotButton = document.querySelector("#screenshot-btn");
    const video = document.querySelector("video");
    const img = document.querySelector("#screenshot-img");

    screenshotButton.onclick = video.onclick = function () {
        img.src = getScreenshot();
    };
}

function getScreenshot() {
    const video = document.querySelector("video");
    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    return canvas.toDataURL("image/webp");
}