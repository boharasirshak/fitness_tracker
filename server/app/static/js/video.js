let workout;
let startTime;
let endTime;
let seconds = 0;
let minutes = 0;
let isResting = false;
let restTimer = 0;
let repetitions = 0;
const fps = 30;
let isCustom = false;
const interval = 1000 / fps;
let connectionId = "";

const accessToken = localStorage.getItem("access_token");
const workoutId = window.location.pathname.split("/").pop();
const video = document.getElementById("video");
const repetitionsCountElement = document.getElementById("repetition-count");
const restTimerElement = document.getElementById("rest-timer");
const timerElement = document.getElementById("timer");
const downloadButton = document.getElementById("download-button");
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const ws = new WebSocket(`${protocol}://${window.location.host}/api/v1/ws`);

if (!accessToken) {
  console.error("Access token not found");
  alert("Access token not found");
  window.location.href = "/login";
}

if (Number.isNaN(parseInt(workoutId))) {
  console.error("Invalid workout id");
  alert("Invalid workout id");
  window.location.href = "/dashboard";
}

function updateTimer() {
  if (isResting) {
    return;
  }

  let timeSpentSeconds = (Date.now() - startTime) / 1000;
  let displaySeconds = 0;

  if (timeSpentSeconds >= 60) {
    displaySeconds = 0;
    minutes++;
  } else {
    displaySeconds = Math.round(timeSpentSeconds);
  }

  timerElement.innerText = `${minutes}:${
    displaySeconds < 10 ? "0" : ""
  }${displaySeconds}`;

  if (startTime === undefined) {
    return;
  }

  if (isCustom) {
    return;
  }

  if (timeSpentSeconds >= workout.total_time && !isResting) {
    endTime = Date.now();
    isResting = true;
    startRestPeriod();

    fetch(`/api/v1/workouts/sessions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        workout_id: workout.id,
        start_time: new Date(startTime).toISOString(),
        end_time: new Date(endTime).toISOString(),
        repetitions: repetitions,
      }),
    })
      .then((res) => {
        if (res.status !== 200) {
          // handle token expiration
        }
      })
      .catch((err) => {
        console.error("Failed to complete workout", err);
      });
  }
}

function startRestPeriod() {
  isResting = true;
  document.getElementById("rest-timer-container").removeAttribute("hidden");
  // debug this.
  document.getElementById("helper-video").pause();
  updateRestTimer();
}

function updateRestTimer() {
  restTimerElement.innerText = `${restTimer}s`;
  if (restTimer > 0) {
    setTimeout(() => {
      restTimer--;
      updateRestTimer();
    }, 1000);
  } else {
    endRestPeriod();
  }
}

function endRestPeriod() {
  isResting = false;
  document.getElementById("rest-timer-container").setAttribute("hidden", "");
  console.log("Resting complete..");
  startTime = Date.now();
  restTimer = workout.rest_time;
  repetitions = 0;
  ws.send(
    JSON.stringify({
      type: "reset",
      connection_id: connectionId,
    })
  );
  document.getElementById("helper-video").play();
}

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
          const b64Data = bufferToBase64(buffer);
          const data = JSON.stringify({
            type: workout.exercise.id,
            data: b64Data,
            is_resting: isResting,
          });
          ws.send(data);
        });
      },
      "image/jpeg",
      0.9
    );
    setTimeout(sendFrame, interval);
  };

  setInterval(updateTimer, 1000);

  // do not send data if the exercise is custom
  if (workout.exercise.id === "custom") {
    return;
  }

  sendFrame();
});

function bufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

(async () => {
  let { res, data } = await getWorkoutData(accessToken, workoutId);
  if (res.status !== 200) {
    console.error("Failed to get workout data");
    alert((data && data.detail) || "Failed to get workout data");
    window.location.href = "/dashboard";
    return;
  }
  workout = data;

  if (workout.exercise.id === "custom") {
    isCustom = true;
    document
      .getElementById("video-container")
      .classList.replace("grid-cols-2", "grid-cols-1");
    document.getElementById("helper-video-container").style.display = "none";
    document.getElementById("download-button").disabled = true;
  } else {
    document
      .getElementById("video-container")
      .classList.replace("grid-cols-2", "grid-cols-2");
  }
  document.getElementById("workout-name").innerText = data.name;
  document.getElementById("exercise-name").innerText = data.exercise.name;

  document.getElementById(
    "helper-video"
  ).src = `../../static/videos/${data.exercise.video_link}`;
  restTimer = data.rest_time;

  // start the video stream when we have the workout data
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
      })
      .catch(function (err) {
        if (err.name === "NotAllowedError") {
          alert(
            "Пожалуйста, разрешите доступ к камере и микрофону, чтобы начать тренировку"
          );
        } else {
          console.error(
            "An error occurred while accessing camera and microphone:",
            err
          );
        }
      });
  }
})();

ws.onmessage = function (event) {
  const message = JSON.parse(event.data);

  if (message.type === "image") {
    // This is no longer required as we are not displaying the received image
    // receivedImg.src = `data:image/jpeg;base64,${message.data}`;
  } else if (message.type === "count") {
    repetitions = parseInt(message.data);
    repetitionsCountElement.innerText = repetitions;
  }
  connectionId = message.connection_id;
};

document
  .getElementById("download-button")
  .addEventListener("click", async () => {
    document.getElementById("download-button").disabled = true;
    document.getElementById("download-button").innerText = "Скачивание...";

    try {
      const response = await fetch(
        `/api/v1/ws/download_video?connection_id=${connectionId}`,
        {
          method: "GET",
        }
      );
      if (!response.ok) {
        const data = await response.json();
        alert(data.detail);
        document.getElementById("download-button").disabled = false;
        document.getElementById("download-button").innerText = "Скачать";
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "video.mp4";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error("Could not download video:", error);
    } finally {
      document.getElementById("download-button").disabled = false;
      document.getElementById("download-button").innerText = "Скачать";
    }
  });
