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
const fps = 30;
const interval = 1000 / fps;

const video = document.getElementById("video");
const helperVideo = document.getElementById("helper-video");
const repetitionsCountElement = document.getElementById("repetition-count");
const timerElement = document.getElementById("timer");
const downloadButtonElement = document.getElementById("download-button");
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const ws = new WebSocket(`${protocol}://${window.location.host}/api/v1/ws`);
const accessToken = getCookie("access_token");

let currentExercise;
let currentExerciseIdx = 0;
let exercises = [];

// TODO: add a case for single exercise

if (exercise === null) {
  exercises = workout.exercises;
  currentExercise = exercises[currentExerciseIdx];
  restTimer = currentExercise.rest_time;
  helperVideo.src = `../../static/videos/${currentExercise.video_link}`;
  document.querySelectorAll("[type='exercise-name']").forEach((el) => {
    el.innerText = currentExercise.name;
  });
}

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

ws.onmessage = function (event) {
  const message = JSON.parse(event.data);

  if (message.type === "count") {
    repetitions = parseInt(message.data);
    repetitionsCountElement.innerText = repetitions;
  }
  connectionId = message.connection_id;
};

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
      },
      "image/jpeg",
      0.9
    );
    setTimeout(sendFrame, interval);
  };

  setInterval(() => {
    if (!isDownloading) {
      updateTimer();
    }
  }, 1000);

  sendFrame();
});

document.getElementById("complete-btn").addEventListener("click", async () => {
  isDownloading = true;
  document.getElementById("complete-btn").disabled = true;
  document.getElementById("complete-btn").innerText = "Скачивание...";

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
      iziToast.show({
        color: "red",
        position: "topRight",
        message: data.detail,
        timeout: 3000,
      });
      document.getElementById("complete-btn").disabled = false;
      document.getElementById("complete-btn").innerText = "Завершить";
      isDownloading = false;
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
    window.URL.revokeObjectURL(url);
  } catch (e) {
    console.error("Failed to download the video", e);
    iziToast.show({
      color: "red",
      position: "topRight",
      message: "Could not save the video. Please try again later.",
      timeout: 3000,
    });
  } finally {
    document.getElementById("complete-btn").disabled = false;
    document.getElementById("complete-btn").innerText = "Завершить";
    isDownloading = false;
  }

  const data = JSON.stringify({
    type: "reset",
    connection_id: connectionId,
  });
  ws.send(data);
  endTime = Date.now();
  endRestPeriod();
});

function updateTimer() {
  if (isResting) {
    return;
  }

  if (isDownloading) {
    return;
  }

  let totalTimeSpentSeconds = parseInt((Date.now() - startTime) / 1000);
  let seconds = 0;

  if (totalTimeSpentSeconds > 0 && totalTimeSpentSeconds % 60 === 0) {
    seconds = 0;
    minutes++;
  } else {
    seconds = Math.round(totalTimeSpentSeconds % 60);
  }

  timerElement.innerText = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;

  if (startTime === undefined) {
    return;
  }

  if (totalTimeSpentSeconds >= currentExercise.total_time && !isResting) {
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
    }),
  })
    .then((res) => {
      if (res.status !== 200) {
        iziToast.show({
          color: "red",
          position: "topRight",
          message: "Failed to save the exercise session",
          timeout: 1000,
        });
      }
    })
    .catch((err) => {
      console.error("Failed to complete workout", err);
    });
}

function startRestPeriod() {
  isResting = true;
  document.getElementById("time-label").innerText = "Отдых";
  document.getElementById("helper-video").src = "";
  updateRestTimer();
}

function updateRestTimer() {
  timerElement.innerText = `${restTimer >= 0 ? restTimer : 0}s`;
  if (restTimer > 0) {
    setTimeout(() => {
      restTimer--;
      updateRestTimer();
    }, 1000);
  } else {
    // to prevent condition where the user completes the exercise before the rest period ends
    if (!isDownloading) {
      endRestPeriod();
    }
  }
}

function endRestPeriod() {
  isResting = false;
  document.getElementById("time-label").innerText = "Длительность";
  startTime = Date.now();
  currentExerciseIdx++;

  if (exercises.length >= currentExerciseIdx + 1) {
    currentExercise = exercises[currentExerciseIdx];
    restTimer = currentExercise.rest_time;
    helperVideo.src = `../../static/videos/${currentExercise.video_link}`;
    restTimer = currentExercise.rest_time;
    repetitions = 0;
    ws.send(
      JSON.stringify({
        type: "reset",
        connection_id: connectionId,
      })
    );
    document.querySelectorAll("[type='exercise-name']").forEach((el) => {
      el.innerText = currentExercise.name;
    });
    document.getElementById("helper-video").play();
  } else {
    isCompleted = true;
    iziToast.show({
      color: "green",
      position: "topRight",
      message: "Тренировка завершена",
      timeout: 5000,
    });
    setTimeout(() => {
      window.location.href = "/dashboard";
    }, 5000);
  }
}
