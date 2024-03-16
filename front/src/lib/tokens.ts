const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";

export async function verifyJwtToken(token: string) {
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

export async function refreshJwtToken(token: string) {
  const res = await fetch(`${BACKEND_URL}/api/v1/tokens/refresh`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  try {
    const data = await res.json();
    return {
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
    }
  } catch {
    return {};
  }
}
