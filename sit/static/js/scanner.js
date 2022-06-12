
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
    // Get device info
    const videoSelect = document.querySelector("select#videoSource")
    const video = document.querySelector("video");

    navigator.mediaDevices
        .enumerateDevices()
        .then(gotDevices)
        .then(getStream);

    videoSelect.onchange = getStream;

    function gotDevices(deviceInfos) {
        let lastUsedCamera = localStorage.getItem('lastUsedCamera');
        for (let i = 0; i !== deviceInfos.length; ++i) {
            const deviceInfo = deviceInfos[i];
            const option = document.createElement("option");
            option.value = deviceInfo.deviceId;
            if (deviceInfo.kind === "videoinput") {
                option.text = deviceInfo.label || "camera " + (videoSelect.length + 1);
                videoSelect.appendChild(option);
            }

            if (lastUsedCamera === deviceInfo.deviceId) {
                videoSelect.value = deviceInfo.deviceId;
            }
        }
    }

    function getStream() {
        localStorage.setItem('lastUsedCamera', videoSelect.value);
        if (window.stream) {
            window.stream.getTracks().forEach(function (track) {
                track.stop();
            });
        }

        const constraints = {
            video: {
                deviceId: { exact: videoSelect.value },
                height: 360,
                width: 480
            },
        };

        navigator.mediaDevices
            .getUserMedia(constraints)
            .then(gotStream);
    }

    function gotStream(stream) {
        window.stream = stream; // make stream available to console
        video.srcObject = stream;
    }

    console.log("Starting capture...");

    // Begin capturing every second
    const interval = setInterval(function() {
        sendScreenshot();
    }, 1000);
}

function sendScreenshot() {
    let image64 = getScreenshot();

    let fd = new FormData();
    fd.append( 'image_source', image64 );

    $.ajax({
        url: '/api/scan_barcode',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            if (data !== "") {
                console.log("Redirecting to " + data)
                window.location.href = data;
            }
        }
    });
}


function getScreenshot() {
    const video = document.querySelector("video");
    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    return canvas.toDataURL("image/webp");
}
