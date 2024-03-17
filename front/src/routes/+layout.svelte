<script>
	import { accessToken, isAuthenticated, refreshToken } from "$lib/stores";
	import { refreshJwtToken, verifyJwtToken } from "$lib/tokens";
	import { onMount } from "svelte";
	import "../app.css";

	onMount(async () => {
		const accToken = localStorage.getItem("accessToken");
		const refToken = localStorage.getItem("refreshToken");

		if (!accToken || !refToken) {
			isAuthenticated.set(false);
      return;
		}

		const isValid = await verifyJwtToken(accToken);
		if (isValid) {
			accessToken.set(accToken);
			refreshToken.set(refToken);
			isAuthenticated.set(true);
			return;
		}

		const resp = await refreshJwtToken(refToken);
		if (resp.accessToken && resp.refreshToken) {
			localStorage.setItem("accessToken", resp.accessToken);
			localStorage.setItem("refreshToken", resp.refreshToken);
			accessToken.set(resp.accessToken);
			refreshToken.set(resp.refreshToken);
			isAuthenticated.set(true);
			return;
		}

		isAuthenticated.set(false);
	});
</script>

<slot />
