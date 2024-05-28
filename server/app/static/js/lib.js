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
