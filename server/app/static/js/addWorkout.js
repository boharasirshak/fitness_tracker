let customExercises = [];
let editWorkoutPage = document.getElementById("edit-workout-page");
let editBox = document.getElementById("edit-box");
let workoutContainer = document.getElementById("workout-container");

const observer = new MutationObserver(updateUI);
observer.observe(document.getElementById("workout-page"), {
  attributes: true,
  attributeFilter: ["style"],
});
observer.observe(document.getElementById("edit-workout-page"), {
  attributes: true,
  attributeFilter: ["style"],
});

function updateUI(mutations) {
  mutations.forEach((mutation) => {
    if (mutation.type === "attributes" && mutation.attributeName === "style") {
      if (editWorkoutPage.style.display === "none") {
        workoutContainer.innerHTML = "";
        exercises.forEach((exercise) => {
          createWorkoutCard(exercise);
        });
      } else {
        editBox.innerHTML = "";
        editBox.appendChild(createExerciseList());
      }
    }
  });
}

function createWorkoutCard(exercise) {
  const card = document.createElement("div");
  card.className = "workout-card new";
  card.innerHTML = `
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
          <div class="plus-minus" type="minus" style="cursor: pointer;">
            <img src="../static/images/minus.svg" alt="" />
          </div>
          <div class="timer-wraps" type="timer">
            <input value="10" type="timer"/>
          </div>
          <div class="plus-minus" type="plus" style="cursor: pointer;">
            <img src="../static/images/plus.svg" alt="" />
          </div>
        </div>
        <div class="flex align-center add-flex gap-20">
          <button class="btn" type="add" >Добавить</button>
          <div class="cross">
            <img src="../static/images/cross.svg" alt="" />
          </div>
        </div>
    </div>
  `;

  workoutContainer.appendChild(card);

  let timer = 10;
  const exercisePopup = card.querySelector(".exercise-popup-wraps");
  const closeBtn = card.querySelector(".cross");
  const plusBtn = card.querySelector(".plus-minus[type='plus']");
  const minusBtn = card.querySelector(".plus-minus[type='minus']");
  const timerInput = card.querySelector("input[type='timer']");
  const addBtn = card.querySelector(".btn[type='add']");

  card.addEventListener("click", () => exercisePopup.classList.add("active"));
  closeBtn.addEventListener("click", (event) => {
    exercisePopup.classList.remove("active");
    event.stopPropagation();
  });

  plusBtn.addEventListener("click", () => {
    timer += 1;
    timerInput.value = timer;
  });

  minusBtn.addEventListener("click", () => {
    if (timer <= 1) return;
    timer -= 1;
    timerInput.value = timer;
  });

  addBtn.addEventListener("click", () => {
    const newExercise = {
      name: exercise.name,
      id: exercise.id,
      gif_link: exercise.gif_link,
      video_link: exercise.video_link,
      duration: timer,
      rest_timeout: 0,
    };
    customExercises.push(newExercise);
    console.log(customExercises);
  });
}

function createExerciseList() {
  const list = document.createElement("div");
  const title = document.createElement("h5");
  title.textContent = "Список упражнений";
  list.appendChild(title);

  if (customExercises.length > 0) {
    customExercises.forEach((exercise) => {
      const exerciseElement = document.createElement("div");
      exerciseElement.className = "timer-edit";
      exerciseElement.innerHTML = `
      <div class="squat-wrap">
        <img src="../static/images/squat.png" alt="" />
      </div>
      <h3>${exercise.name}</h3>
      <div class="timer-wrap">
        <input value="${exercise.duration}" />
      </div>
      `;
      list.appendChild(exerciseElement);

      if (exercise.rest_timeout > 0) {
        const restElement = document.createElement("div");
        restElement.className = "timer-edit";
        restElement.innerHTML = `
        <div class="center-wrap">
          <img src="../static/images/dots.svg" alt="" />
          </div>
          <h3>Отдых</h3>
          <div class="timer-wrap">
            <input value="${exercise.rest_timeout}" />
          </div>
        `;
        list.appendChild(restElement);
      }
    });
    editBox.appendChild(createButtons());
  } else {
    const container = document.createElement("div");
    container.className = "text-edit-wrap";

    const addExerciseBtn = document.createElement("div");
    addExerciseBtn.className = "list-exercise";
    addExerciseBtn.id = "add-exercise-btn";
    addExerciseBtn.style.cursor = "pointer";
    addExerciseBtn.onclick = () => showPage("workout-page");
    addExerciseBtn.innerHTML =
      "<img src='../static/images/plus.svg' alt='' /> Упражнение";
    container.appendChild(addExerciseBtn);
    list.appendChild(container);
  }

  return list;
}

function createButtons() {
  const buttonsWrapper = document.createElement("div");
  buttonsWrapper.className = "flex align-center gap-20 btns-wrap";

  const restBtn = document.createElement("button");
  restBtn.className = "white-btn";
  restBtn.innerHTML = "<img src='../static/images/plus.svg' alt='' />Отдых";
  buttonsWrapper.appendChild(restBtn);

  const exerciseBtn = document.createElement("button");
  exerciseBtn.className = "white-btn";
  exerciseBtn.onclick = () => showPage("workout-page");
  exerciseBtn.innerHTML =
    "<img src='../static/images/plus.svg' alt='' />Упражнение";
  buttonsWrapper.appendChild(exerciseBtn);

  restBtn.onclick = () => {
    let lastExercise = customExercises[customExercises.length - 1];
    if (lastExercise && lastExercise.rest_timeout > 0) {
      lastExercise.rest_timeout += 10;
    } else {
      lastExercise.rest_timeout = 10;
    }
    customExercises.pop();
    customExercises.push(lastExercise);
    updateUI([{ type: "attributes", attributeName: "style" }]);
  };

  return buttonsWrapper;
}

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
  customExercises.push(exercise);
  showPage("edit-workout-page");
}
