const fileInput = document.getElementById("file-input");
const profilePic = document.getElementById("profile-pic");
const activityLevels = [1, 2, 3];
var activityLevel = 1;

function changeActivityLevel(level) {
  activityLevel = level;
  document.getElementById(`btn-activity-level-${level}`).style.backgroundColor =
    "#958be4";

  const others = activityLevels.filter((l) => l !== level);
  others.forEach((l) => {
    document.getElementById(`btn-activity-level-${l}`).style = "";
  });
}

profilePic.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
    profilePic.src = e.target.result;
  };

  reader.readAsDataURL(file);

  const formData = new FormData();
  formData.append("photo", file);

  const accessToken = localStorage.getItem("access_token");

  const res = await fetch("/api/v1/users/photo", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: formData,
  });

  if (res.status === 401) {
    window.location.href = "/login";
  }

  if (res.status === 409) {
    document.getElementById("toast-success").style.display = "none";
    document.getElementById("toast-danger").style.display = "";
    document.getElementById("toast-danger-text").innerText =
      "Недопустимый тип файла";
  } else if (res.status === 200) {
    document.getElementById("toast-danger").style.display = "none";
    document.getElementById("toast-success").style.display = "";
    document.getElementById("toast-success-text").innerText =
      "Фотография профиля успешно обновлена";
  }
});

document.getElementById("submit").addEventListener("click", async () => {
  let name = document.getElementById("name").value;
  let gender = document.getElementById("male").checked ? "male" : "female";
  let height = document.getElementById("height").value;
  let weight = document.getElementById("weight").value;
  let age = document.getElementById("age").value;
  let desiredWeight = document.getElementById("desired-weight").value;

  if (
    Number.isNaN(parseInt(activityLevel)) ||
    Number.isNaN(parseInt(weight)) ||
    Number.isNaN(parseInt(height)) ||
    Number.isNaN(parseInt(desiredWeight)) ||
    Number.isNaN(parseInt(age))
  ) {
    document.getElementById("toast-success").style.display = "none";
    document.getElementById("toast-danger").style.display = "";
    document.getElementById("toast-danger-text").innerText =
      "Все поля обязательны для заполнения";
    return;
  }

  activityLevel = parseInt(activityLevel);
  weight = parseInt(weight);
  height = parseInt(height);
  desiredWeight = parseInt(desiredWeight);
  age = parseInt(age);

  const accessToken = localStorage.getItem("access_token");
  if (!accessToken) {
    window.location.href = "/login";
    return;
  }

  const response = await fetch("/api/v1/users", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    },
    body: JSON.stringify({
      username: name,
      gender,
      height,
      weight,
      age,
      desired_weight: desiredWeight,
      activity_level: activityLevel,
    }),
  });

  if (response.status >= 500) {
    try {
      const res = await response.json();
      document.getElementById("toast-success").style.display = "none";
      document.getElementById("toast-danger").style.display = "";
      document.getElementById("toast-danger-text").innerText = res.message;
    } catch {
      document.getElementById("toast-success").style.display = "none";
      document.getElementById("toast-danger").style.display = "";
      document.getElementById("toast-danger-text").innerText =
        "Произошла ошибка на сервере. Попробуйте позже";
    }
  }

  if (response.status === 409) {
    document.getElementById("toast-success").style.display = "none";
    document.getElementById("toast-danger").style.display = "";
    document.getElementById("toast-danger-text").innerText =
      "Номер телефона уже существует!";
    return;
  }

  if (response.status === 401) {
    window.location.href = "/login";
    return;
  }

  if (response.status === 422) {
    document.getElementById("toast-success").style.display = "none";
    document.getElementById("toast-danger").style.display = "";
    document.getElementById("toast-danger-text").innerText = "Неверные данные";
    return;
  }

  document.getElementById("toast-danger").style.display = "none";
  document.getElementById("toast-success").style.display = "";
  document.getElementById("toast-success-text").innerText =
    "Данные успешно обновлены";

  window.location.href = "/dashboard";
});
