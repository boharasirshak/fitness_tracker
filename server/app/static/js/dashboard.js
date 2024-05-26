let workouts;
let workout;

(async () => {
  let accessToken = localStorage.getItem("access_token");

  let { res, data } = await getUserWorkouts(accessToken);
  if (res.status === 401) {
    window.location.href = "/login";
  }
  workouts = data.workouts;

  const workoutContainer = document.getElementById("workouts");

  data.workouts.forEach((workout) => {
    const li = document.createElement("div");

    li.innerHTML = `
      <div class="workout-coolection">
        <div class="workout-image">
          <video
            src="../static/videos/${workout.exercise.video_link}" 
            alt="squat"
            alt="exercise video"
            playsinline
            autoplay
            muted
            loop
        />
        </div>
        <div class="workout-name-wrap">
          <h5>${workout.name}</h5>
          <a href="/workouts/start/${workout.id}">
            <img
              src="../static/assets/images/gradient-arrow.svg"
              alt="arrow"
            />
          </a>
        </div>
      </div>
    `;
    workoutContainer.appendChild(li);
  });

  const groupedData = {};
  const weekContainer = document.getElementById("week-container");
  const today = new Date();
  const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);

  // if (workouts.length === 0) {
  //   const element = document.createElement("div");
  //   element.innerHTML = `
  //     <li>
  //       <div class="day">No sessions</div>
  //       <div class="date">No sessions</div>
  //     </li>
  //   `;
  //   weekContainer.appendChild(element);
  // }

  for (const workout in workouts) {
  }

  for (const session of workouts.sessions) {
    const startTime = new Date(session.start_time);
    const dayOfMonth = getDayOfMonth(session.start_time);
    const dayOfWeek = getDayOfWeek(session.start_time);

    if (startTime >= lastWeek) {
      if (!groupedData[dayOfMonth]) {
        groupedData[dayOfMonth] = {
          dayOfWeek: dayOfWeek,
          sessions: [],
        };
      }
      groupedData[dayOfMonth].sessions.push({
        start_time: session.start_time,
        end_time: session.end_time,
      });
    }

    for (const [day, dayData] of Object.entries(groupedData)) {
      const element = document.createElement("div");
      element.innerHTML = `
        <li onclick="displayGraph('${JSON.stringify(dayData.sessions)}')>
          <div class="day">${dayData.dayOfWeek}</div>
          <div class="date">${day}</div>
        </li>
      `;
      weekContainer.appendChild(element);
    }
  }
})();

function displayGraph(sessionsData) {
  const sessions = JSON.parse(sessionsData);

  const labels = sessions.map((session) =>
    new Date(session.start_time).toLocaleTimeString()
  );

  const data = sessions.map((session) => {
    const startTime = new Date(session.start_time);
    const endTime = new Date(session.end_time);
    const duration = endTime.getTime() - startTime.getTime();
    return duration / (1000 * 60); // Convert duration to minutes
  });

  const ctx = document.getElementById("chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Duration (minutes)",
          data: data,
          pointRadius: data.map((entry) => (entry === 0 ? 0 : 3)),
          fill: false,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Time / Duration",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Duration (minutes)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Session Start Time",
          },
        },
      },
    },
  });
}

function clearCanvas() {
  const existingChart = Chart.getChart("workout-chart");
  if (existingChart) {
    existingChart.destroy();
  }

  const canvas = document.getElementById("workout-chart");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function getDayOfMonth(dateString) {
  const date = new Date(dateString);
  return date.getDate();
}

function getDayOfWeek(dateString) {
  const daysOfWeek = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const date = new Date(dateString);
  return daysOfWeek[date.getDay()];
}

function formatDateTime(dateTimeStr) {
  const dateTime = luxon.DateTime.fromISO(dateTimeStr);
  return dateTime.toFormat("h':'mm a");
}
