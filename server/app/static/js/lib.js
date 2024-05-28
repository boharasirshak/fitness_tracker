async function verifyJwtToken(token) {
  const res = await fetch("/api/v1/tokens/verify", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    return res.status === 200;
  } catch {
    return false;
  }
}

async function getUser(token) {
  const res = await fetch("/api/v1/users/me", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    return {
      res,
      data: await res.json(),
    };
  } catch {
    return {
      res,
      detail: "внутренняя ошибка сервера",
    };
  }
}

async function getAllExercises(token) {
  const res = await fetch("/api/v1/exercises", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    return {
      res,
      data: await res.json(),
    };
  } catch {
    return {
      res,
      detail: "внутренняя ошибка сервера",
    };
  }
}

async function getUserWorkouts(token) {
  const res = await fetch("/api/v1/workouts", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    return {
      res,
      data: await res.json(),
    };
  } catch {
    return {
      res,
      detail: "внутренняя ошибка сервера",
    };
  }
}

async function getWorkoutData(token, workout_id) {
  const res = await fetch(`/api/v1/workouts/${workout_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    return {
      res,
      data: await res.json(),
    };
  } catch {
    return {
      res,
      detail: "внутренняя ошибка сервера",
    };
  }
}

function setCookie(name, value, expiryDays) {
  const d = new Date();
  if (expiryDays) {
    d.setTime(d.getTime() + 60 * 60 * 24 * expiry);
    document.cookie = `${name}=${value};expires=${d.toUTCString()}`;
  } else {
    document.cookie = `${name}=${value};expires=Tue, 19 Jan 2038 04:14:07 GMT`;
  }
}
