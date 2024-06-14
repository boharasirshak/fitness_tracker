const customWorkoutList = document.getElementById("custom-workout-list");

for (const workout of workouts) {
  const div = document.createElement("div");
  div.className = "workout-card";
  div.innerHTML = `
  <h4>${workout.name}</h4>
  <img src="../static/images/gradient-arrow.svg" alt="" />
  `;
  div.style.cursor = "pointer";
  div.onclick = function () {
    window.location.href = `/workouts/${workout.id}/start`;
  };
  customWorkoutList.appendChild(div);
}

var workoutCards = document.querySelectorAll(".workout-card");
workoutCards.forEach(function (card) {
  card.addEventListener("click", function () {
    var popupWrap = this.querySelector(".exercise-popup-wraps");
    popupWrap.classList.add("active");
  });
});

var closeBtns = document.querySelectorAll(".cross");
closeBtns.forEach(function (btn) {
  btn.addEventListener("click", function (event) {
    var popupWrap = this.closest(".exercise-popup-wraps");
    popupWrap.classList.remove("active");
    event.stopPropagation();
  });
});
