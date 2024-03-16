const BACKEND_URL = process.env.REACT_APP_BACKEND_URL ?? "http://localhost:8000";

async function verifyJwtToken(token: string) {
  const res = await fetch(`${BACKEND_URL}/api/v1/tokens/verif`, {
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

async function refreshJwtToken(token: string) {
  const res = await fetch(`${BACKEND_URL}/api/v1/tokens/refresh`, {
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
