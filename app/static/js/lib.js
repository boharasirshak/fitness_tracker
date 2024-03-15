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
