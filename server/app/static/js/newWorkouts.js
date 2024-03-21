document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault()
  const formdata = new FormData(e.target)
  const data = Object.fromEntries(formdata)

  if (
    Number.isNaN(parseInt(data.total_time)) ||
    Number.isNaN(parseInt(data.rest_time))
  ) {
    document.getElementById('toast-success').style.display = 'none';
    document.getElementById('toast-danger').style.display = '';
    document.getElementById('toast-danger-text').innerText = 'некоторые поля ввода недопустимы.';
    return;
  }

  data.total_time = parseInt(data.total_time)
  data.rest_time = parseInt(data.rest_time)

  const response = await fetch('/api/v1/workouts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify(data),
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

  if (response.status === 401) {
    window.location.href = "/login";
    return;
  }

  const res = await response.json();

  if (response.status === 422) {
    document.getElementById('toast-success').style.display = 'none';
    document.getElementById('toast-danger').style.display = '';
    document.getElementById('toast-danger-text').innerText = 'Неверные данные';
    return;
  } else if (response.status === 200) {
    document.getElementById('toast-danger').style.display = 'none';
    document.getElementById('toast-success').style.display = '';
    document.getElementById('toast-success-text').innerText = res.message;

    window.location.href = "/dashboard";
  }else {
    document.getElementById('toast-success').style.display = 'none';
    document.getElementById('toast-danger').style.display = '';
    document.getElementById('toast-success-text').innerText = res.detail;
  }
})
