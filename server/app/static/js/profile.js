document.getElementById("form").addEventListener("submit", async e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const activityLevel = formData.get("activity_level");
    const weight = formData.get("weight");
    const height = formData.get("height");
    const phoneNum = formData.get("phone_number");

    if (
      Number.isNaN(parseInt(activityLevel)) ||
      Number.isNaN(parseInt(weight)) ||
      Number.isNaN(parseInt(height)) || 
      Number.isNaN(parseInt(phoneNum)) ||
      formData.get("weight") === "0" ||
      formData.get("height") === "0"
    ){
      document.getElementById('toast-success').style.display = 'none';
      document.getElementById('toast-danger').style.display = '';
      document.getElementById('toast-danger-text').innerText = 'Все поля обязательны для заполнения';
      return;
    }

    const data = JSON.parse(JSON.stringify(Object.fromEntries(formData)));
    data.activity_level = parseInt(activityLevel);
    data.weight = parseInt(weight);
    data.height = parseInt(height);

    const payload = JSON.stringify(data);

    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      window.location.href = "/login";
      return;
    }

    const response = await fetch("/api/v1/users", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      },
      body: payload
    });

    if (response.status >= 500) {
      try {
        const res = await response.json();
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = res.message;
      } catch {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'Произошла ошибка на сервере. Попробуйте позже';
      }
    }

    if (response.status === 409) {
      document.getElementById('toast-success').style.display = 'none';
      document.getElementById('toast-danger').style.display = '';
      document.getElementById('toast-danger-text').innerText = 'Номер телефона уже существует!';
      return;
    }

    if (response.status === 401) {
      window.location.href = "/login";
      return;
    }

    if (response.status === 422) {
      document.getElementById('toast-success').style.display = 'none';
      document.getElementById('toast-danger').style.display = '';
      document.getElementById('toast-danger-text').innerText = 'Неверные данные';
      return;
    }

    document.getElementById('toast-danger').style.display = 'none';
    document.getElementById('toast-success').style.display = '';
    document.getElementById('toast-success-text').innerText = 'Данные успешно обновлены';


});
