let startTime;
let endTime;
let seconds = 0;
let minutes = 0;
let isResting = false;
let isPaused = false;
let restTimer = 0;
let repetitions = 0;
const fps = 30;
const interval = 1000 / fps;
let isCustom = false;
let connectionId = "";

const video = document.getElementById("video");
const repetitionsCountElement = document.getElementById("repetition-count");
const restTimerElement = document.getElementById("rest-timer");
const timerElement = document.getElementById("timer");
const downloadButtonElement = document.getElementById("download-button");
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const ws = new WebSocket(`${protocol}://${window.location.host}/api/v1/ws`);

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch(() => {
      iziToast.show({
        color: "red",
        position: "topRight",
        message:
          "Пожалуйста, разрешите доступ к камере и микрофону, чтобы начать тренировку",
        timeout: 5000,
      });
      setTimeout(() => {
        window.location.href = "/workouts";
      }, 5000);
    });
} else {
  iziToast.show({
    color: "red",
    position: "topRight",
    message: "Camers access is not supported in this browser",
    timeout: 5000,
  });
  setTimeout(() => {
    window.location.href = "/workouts";
  }, 5000);
}

// ws.onmessage = function (event) {
//   const message = JSON.parse(event.data);

//   if (message.type === "image") {
//   } else if (message.type === "count") {
//     repetitions = parseInt(message.data);
//     repetitionsCountElement.innerText = repetitions;
//   }
//   connectionId = message.connection_id;
// };

video.addEventListener("play", () => {
  startTime = Date.now();
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  const sendFrame = () => {
    if (video.paused || video.ended) {
      console.log("Video paused, ended.");
      return;
    }

    const aspectRatio = video.videoWidth / video.videoHeight;
    let targetHeight = 240;
    let targetWidth = aspectRatio * targetHeight;

    canvas.width = targetWidth;
    canvas.height = targetHeight;

    context.drawImage(video, 0, 0, targetWidth, targetHeight);
    canvas.toBlob(
      (blob) => {
        blob.arrayBuffer().then((buffer) => {
          // const b64Data = bufferToBase64(buffer);
          // const data = JSON.stringify({
          //   type: workout.exercise.id,
          //   data: b64Data,
          //   is_resting: isResting,
          // });
          // ws.send(data);
        });
      },
      "image/jpeg",
      0.9
    );
    setTimeout(sendFrame, interval);
  };

  // setInterval(updateTimer, 1000);

  // do not send data if the exercise is custom
  // if (workout.exercise.id === "custom") {
  //   return;
  // }

  sendFrame();
});
