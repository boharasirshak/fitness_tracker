let customExercises = [];
let workoutName = "";
const workoutPage = document.getElementById("workout-page");
const editWorkoutPage = document.getElementById("edit-workout-page");

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === "attributes" && mutation.attributeName === "style") {
      const displayValue = workoutPage.style.display;

      console.log(`Display value: ${displayValue}`);

      // CASE: the edit workout page is displayed
      if (displayValue === "none") {
        if (customExercises.length > 0) {
          const editBox = document.getElementById("edit-box");
          editBox.innerHTML = "";
          const title = document.createElement("h5");
          title.textContent = "Список упражнений";
          editBox.appendChild(title);

          for (const exercise of customExercises) {
            const timerEdit = document.createElement("div");
            timerEdit.className = "timer-edit";
            timerEdit.innerHTML = `
              <div class="squat-wrap">
                <img src="../static/images/squat.png" alt="" />
              </div>
              <h3>${exercise.name}</h3>
              <div class="timer-wrap">
                <span>0:10</span>
              </div>
            `;
            editBox.appendChild(timerEdit);
          }

          editBox.innerHTML += `
            <div class="flex align-center gap-20 btns-wrap">
              <button class="white-btn">
                <img src="../static/images/plus.svg" alt="" />Отдых
              </button>
              <button class="white-btn" onclick="showPage('workout-page')">
                <img src="../static/images/plus.svg" alt="" />Упражнение
              </button>
            </div>
          `;
        } else {
          document.getElementById("edit-box").innerHTML = `
          <h5>Список упражнений</h5>
              <div class="text-edit-wrap">
                <div
                  class="list-exercise"
                  id="add-exercise-btn"
                  style="cursor: pointer"
                  onclick="showPage('workout-page')"
                >
                  <img src="../static/images/plus.svg" alt="" />
                  Упражнение
                </div>
              </div>
          `;
        }

        // CASE: the choose workouts page is displayed
      } else {
        let workoutContainer = document.getElementById("workout-container");
        workoutContainer.innerHTML = "";
        for (const exercise of exercises) {
          const element = document.createElement("div");
          element.className = "workout-card new";
          element.innerHTML = `
          <img
              src="../static/images/exercise-1.png"
              alt=""
              class="exercise-img"
            />
            <h4>${exercise.name}</h4>
            <img src="../static/images/add-btn.svg" alt="" style="cursor: pointer;" />
            <div class="exercise-popup-wraps">
              <div class="exercise-pop-wrapper">
                <h4>${exercise.name}</h4>
                <div class="workout">
                  <img src="../static/images/exercise-1.png" alt="" />
                </div>
                <div class="timer-count">
                  <div class="plus-minus">
                    <img src="../static/images/minus.svg" alt="" />
                  </div>
                  <div class="timer-wraps">
                    <span>0:10</span>
                  </div>
                  <div class="plus-minus">
                    <img src="../static/images/plus.svg" alt="" />
                  </div>
                </div>
                <div class="flex align-center add-flex gap-20">
                  <button class="btn" onclick='addNewExercise({
                    "name": "${exercise.name}",
                    "id": "${exercise.id}",
                    "gif_link": "${exercise.gif_link}",
                    "video_link": "${exercise.video_link}",
                  })'>Добавить</button>
                  <div class="cross">
                    <img src="../static/images/cross.svg" alt="" />
                  </div>
                </div>
            </div>
          `;
          workoutContainer.appendChild(element);
        }

        const workoutCards = document.querySelectorAll(".workout-card");
        const closeBtns = document.querySelectorAll(".cross");

        workoutCards.forEach(function (card) {
          card.addEventListener("click", function () {
            const exercisePopup = this.querySelector(".exercise-popup-wraps");
            exercisePopup.classList.add("active");
          });
        });

        closeBtns.forEach(function (btn) {
          btn.addEventListener("click", function (event) {
            const exercisePopup = this.closest(".exercise-popup-wraps");
            exercisePopup.classList.remove("active");
            event.stopPropagation();
          });
        });
      }
    }
  });
});

observer.observe(workoutPage, { attributes: true, attributeFilter: ["style"] });
observer.observe(editWorkoutPage, {
  attributes: true,
  attributeFilter: ["style"],
});

function showPage(page) {
  const editWorkoutPage = document.getElementById("edit-workout-page");
  const workoutPage = document.getElementById("workout-page");

  if (page === "edit-workout-page") {
    editWorkoutPage.style.display = "";
    workoutPage.style.display = "none";
  } else {
    workoutPage.style.display = "";
    editWorkoutPage.style.display = "none";
  }
}

function addNewExercise(exercise) {
  console.log(exercise);
  customExercises.push(exercise);
  showPage("edit-workout-page");
}
