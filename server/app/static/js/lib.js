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

async function refreshJwtToken(token) {
  const res = await fetch("/api/v1/tokens/refresh", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    return await res.json();
  } catch {
    return {};
  }
}

async function authFlow(success, failure) {
  let accessToken = localStorage.getItem("access_token");
  let refreshToken = localStorage.getItem("refresh_token");

  if (accessToken && refreshToken) {
    let isValid = await verifyJwtToken(accessToken);
    console.log(`Access token is: ${isValid ? "valid" : "invalid"}`);

    if (isValid) {
      if (success) {
        window.location.href = success;
      }
    } else {
      let { access_token, refresh_token } = await refreshJwtToken(refreshToken);

      if (access_token && refresh_token) {
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
        if (redirect) {
          window.location.href = success;
        }
      } else {
        console.log("Недопустимый токен обновления. Оставайтесь на странице.");
        if (failure) {
          window.location.href = failure;
        }
      }
    }
  } else {
    if (failure) {
      window.location.href = failure;
    }
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
      detail: "Internal Server Error",
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
      detail: "Internal Server Error",
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
      detail: "Internal Server Error",
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
      detail: "Internal Server Error",
    };
  }
}
