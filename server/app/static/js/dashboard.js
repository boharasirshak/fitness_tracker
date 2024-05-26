let workouts;
let workout;
const daysOfWeeks = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];
const today = new Date();
var lastSevenDays = Array.from({ length: 7 }, (_, i) => {
  const date = new Date(today);
  date.setDate(today.getDate() - i);
  return date;
}).reverse();
let prevActiveDate;

(async () => {
  let accessToken = localStorage.getItem("access_token");

  let { res, data } = await getUserWorkouts(accessToken);
  if (res.status === 401) {
    window.location.href = "/login";
  }
  workouts = data.workouts;
  console.log(workouts);

  const workoutContainer = document.getElementById("workouts");
  const weekContainer = document.getElementById("week-container");

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

  for (const day of lastSevenDays) {
    const element = document.createElement("li");
    element.onclick = () => {
      if (prevActiveDate) {
        prevActiveDate.classList.remove("active");
      }
      prevActiveDate = element;
      element.classList.add("active");
      displayGraph(day, element);
    };

    element.innerHTML = `
      <div class="day">${daysOfWeeks[day.getDay()]}</div>
      <div class="date">${day.getDate()}</div>
    `;
    if (day.getDate() === today.getDate()) {
      element.click();
    }
    weekContainer.appendChild(element);
  }
})();

function displayGraph(intentedDay, newElement) {
  const groupedData = {};
  const labels = [];
  const datasets = [];

  for (const workout of workouts) {
    groupedData[workout.id] = {
      name: workout.name,
      sessions: [],
    };

    for (const session of workout.sessions) {
      const startDay = new Date(session.start_time).getDate();

      if (startDay === intentedDay.getDate()) {
        groupedData[workout.id].sessions.push({
          start_time: formatDateTime(session.start_time),
          end_time: formatDateTime(session.end_time),
        });
      }
    }
  }

  for (const workoutId in groupedData) {
    const workout = groupedData[workoutId];
    const data = [];

    for (const session of workout.sessions) {
      data.push({
        x: session.start_time,
        y: session.repetitions,
      });
    }

    datasets.push({
      label: workout.name,
      data: data,
      borderColor: "rgba(75, 192, 192, 1)",
      fill: false,
    });
  }

  clearCanvas();

  const ctx = document.getElementById("workout-chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Количество повторений за сеанс",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Повторения",
          },
        },
        x: {
          title: {
            display: true,
            text: "Время начала сеанса",
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
