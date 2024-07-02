let startTime;
let endTime;
let seconds = 0;
let minutes = 0;
let isResting = false;
let isDownloading = false;
let restTimer = 0;
let repetitions = 0;
let connectionId = "";
let isCompleted = false;
const fps = 21;
const interval = 1000 / fps;

const video = document.getElementById("video");
const helperVideo = document.getElementById("helper-video");
const repetitionsCountElement = document.getElementById("repetition-count");
const timerElement = document.getElementById("timer");
const completeButton = document.getElementById("complete-btn");
const downloadButtonElement = document.getElementById("download-button");
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const ws = new WebSocket(`${protocol}://${window.location.host}/api/v1/ws`);
const accessToken = getCookie("access_token");
// const receivedImage = document.getElementById("received-image");

let currentExercise;
let currentExerciseIdx = 0;
let exercises = exercise ? [exercise] : workout.exercises;

if (exercises.length > 0) {
  initializeExercise(exercises[currentExerciseIdx]);
}

initializeVideoStream();

setTimeout(() => {
  video.addEventListener("play", startVideoProcessing);
  initializeVideoStream();
}, 5000);

ws.onmessage = handleWebSocketMessage;

completeButton.addEventListener("click", completeWorkout);

function initializeExercise(exercise) {
  currentExercise = exercise;
  restTimer = currentExercise.rest_time;
  helperVideo.src = `../../static/gif/${currentExercise.gif_link}`;
  document.querySelectorAll("[type='exercise-name']").forEach((el) => {
    el.innerText = currentExercise.name;
  });
}

function initializeVideoStream() {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
      })
      .catch(() => {
        showToast(
          "red",
          "Пожалуйста, разрешите доступ к камере и микрофону, чтобы начать тренировку"
        );
        redirectToWorkouts();
      });
  } else {
    showToast("red", "Camera access is not supported in this browser");
    redirectToWorkouts();
  }
}

function handleWebSocketMessage(event) {
  const message = JSON.parse(event.data);

  // We do not process the image
  // if (message.type === "image") {
  //   receivedImage.src = `data:image/jpeg;base64,${message.data}`;
  // }

  if (message.type === "count") {
    repetitions = parseInt(message.data);
    repetitionsCountElement.innerText = repetitions;
  }
  connectionId = message.connection_id;
}

function startVideoProcessing() {
  startTime = Date.now();
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  function sendFrame() {
    if (video.paused || video.ended) return;

    const aspectRatio = video.videoWidth / video.videoHeight;
    const targetHeight = 360;
    const targetWidth = aspectRatio * targetHeight;

    canvas.width = targetWidth;
    canvas.height = targetHeight;
    context.drawImage(video, 0, 0, targetWidth, targetHeight);

    canvas.toBlob(
      (blob) => {
        if (blob) {
          blob.arrayBuffer().then((buffer) => {
            let b64Data = isResting ? null : bufferToBase64(buffer);
            const data = JSON.stringify({
              type: currentExercise.exercise_id,
              data: b64Data,
              is_resting: isResting,
              is_downloading: isDownloading,
              is_completed: isCompleted,
            });
            ws.send(data);
          });
        }
      },
      "image/jpeg",
      0.5
    );

    setTimeout(sendFrame, interval);
  }

  setInterval(updateTimer, 1000);

  sendFrame();
}

async function completeWorkout() {
  isDownloading = true;
  completeButton.disabled = true;
  completeButton.innerText = "Скачивание...";

  try {
    const response = await fetch(
      `/api/v1/ws/download_video?connection_id=${connectionId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      const data = await response.json();
      showToast("red", data.detail);
      resetCompleteButton();
      return;
    }

    const blob = await response.blob();
    downloadBlob(blob, "video.mp4");
  } catch (e) {
    console.error("Failed to download the video", e);
    showToast("red", "Could not save the video. Please try again later.");
  } finally {
    resetCompleteButton();
  }

  ws.send(JSON.stringify({ type: "reset", connection_id: connectionId }));
  endTime = Date.now();
  endRestPeriod();
}

function updateTimer() {
  if (isResting || isDownloading || !startTime) return;

  const totalTimeSpentSeconds = parseInt((Date.now() - startTime) / 1000);
  const displaySeconds = totalTimeSpentSeconds % 60;

  if (totalTimeSpentSeconds % 60 === 0 && totalTimeSpentSeconds > 0) {
    seconds = 0;
    minutes++;
  }

  timerElement.innerText = `${minutes}:${
    displaySeconds < 10 ? "0" : ""
  }${displaySeconds}`;

  if (repetitions >= currentExercise.repetitions && !isResting) {
    endTime = Date.now();
    saveSession();
    startRestPeriod();
  }
}

function saveSession() {
  fetch(`/api/v1/workouts/sessions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      workout_id: workout.id,
      repetitions: repetitions,
      workout_exercise_id: currentExercise.id,
      started_at: new Date(startTime).toISOString(),
      finished_at: new Date(endTime).toISOString(),
    }),
  })
    .then((res) => {
      if (res.status !== 200) {
        showToast("red", "Failed to save the exercise session");
      }
    })
    .catch((err) => {
      console.error("Failed to complete workout", err);
    });
}

function startRestPeriod() {
  isResting = true;
  document.getElementById("time-label").innerText = "Отдых";
  helperVideo.src = "";
  updateRestTimer();
}

function updateRestTimer() {
  timerElement.innerText = `${restTimer >= 0 ? restTimer : 0}s`;
  if (restTimer > 0) {
    setTimeout(() => {
      restTimer--;
      updateRestTimer();
    }, 1000);
  } else if (!isDownloading) {
    endRestPeriod();
  }
}

function endRestPeriod() {
  isResting = false;
  document.getElementById("time-label").innerText = "Длительность";
  startTime = Date.now();
  currentExerciseIdx++;

  if (currentExerciseIdx < exercises.length) {
    initializeExercise(exercises[currentExerciseIdx]);
    repetitions = 0;
    ws.send(JSON.stringify({ type: "reset", connection_id: connectionId }));
    helperVideo.play();
  } else {
    isCompleted = true;
    showToast("green", "Тренировка завершена");
    setTimeout(() => {
      window.location.href = "/dashboard";
    }, 5000);
  }
}

function bufferToBase64(buffer) {
  let binary = "";
  let bytes = new Uint8Array(buffer);
  let len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

function showToast(color, message) {
  iziToast.show({
    color: color,
    position: "topRight",
    message: message,
    timeout: 5000,
  });
}

function redirectToWorkouts() {
  setTimeout(() => {
    window.location.href = "/workouts";
  }, 5000);
}

function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

function resetCompleteButton() {
  completeButton.disabled = false;
  completeButton.innerText = "Завершить";
  isDownloading = false;
}
