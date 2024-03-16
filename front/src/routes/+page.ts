export const ssr = false;

import { accessToken, isAuthenticated, refreshToken } from "$lib/stores";
import { refreshJwtToken, verifyJwtToken } from "$lib/tokens";

export async function load() {
	const accToken = localStorage.getItem('accessToken');
  const refToken = localStorage.getItem('refreshToken');

  if (!accToken || !refToken) {
    isAuthenticated.set(false);
    return {};
  }

  const isValid = await verifyJwtToken(accToken);
  if (isValid) {
    accessToken.set(accToken);
    refreshToken.set(refToken);
    isAuthenticated.set(true);
    return {};
  }

  const resp = await refreshJwtToken(refToken);
  if (resp.accessToken && resp.refreshToken) {
    accessToken.set(resp.accessToken);
    refreshToken.set(resp.refreshToken);
    isAuthenticated.set(true);
  }
  
  isAuthenticated.set(false);
  return {};
}
