<script lang="ts">
	import { goto } from "$app/navigation";
	import Alert from "$lib/components/Alert.svelte";
	import { accessToken, isAuthenticated, refreshToken } from "$lib/stores";
	import { Button } from 'flowbite-svelte';

	let email = "";
	let password = "";
	let message = "";
	let showAlert = false;
	let success = false;

	const alert = (msg: string, suc: boolean) => {
		showAlert = true;
		message = msg;
		success = suc;
	};

	const submit = async () => {
		const backendUrl = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";

    if (!email || !password) {
			return alert("Please fill in all fields", false);
    }

		const res = await fetch(`${backendUrl}/api/v1/auth/login`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ email, password })
		});

    if (res.status >= 500) {
      return alert("Internal Server Error!", false);
    }

    const data = await res.json();
		if (res.status == 200) {
			localStorage.setItem("accessToken", data.access_token);
			localStorage.setItem("refreshToken", data.refresh_token);
			accessToken.set(data.access_token);
			refreshToken.set(data.refresh_token);
			isAuthenticated.set(true);
			alert("Logged in successfully", true);

			setTimeout(() => {goto("/dashboard").then(() => {})}, 1000);

		} else if (res.status === 401) {
			alert("Incorrect email or password", false);

		} else if (res.status === 422) {
			alert("Please fill in all fields", false);

		} else {
			alert("An error occurred", false);
		}
	};
</script>

{#if $isAuthenticated}
	{
		goto("/dashboard").then(() => {})
	}
{/if}

<section class="bg-gray-50 dark:bg-gray-900">
	<div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
		<div
			class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
		>
			<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
				<h1
					class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
				>
					Sign in to your account
				</h1>
				<div class="space-y-4 md:space-y-6">
					<div>
						<label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
							Your email
						</label>
						<input
							type="email"
							name="email"
							id="email"
							class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
							placeholder="name@company.com"
							required
							bind:value={email}
						/>
					</div>
					<div>
						<label
							for="password"
							class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
						>
							Password
						</label>
						<input
							type="password"
							name="password"
							id="password"
							placeholder="••••••••"
							class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
							required
							bind:value={password}
						/>
					</div>
					<div class="flex items-center justify-between">
						<div class="flex items-start">
							<div class="flex items-center h-5">
								<input
									id="remember"
									aria-describedby="remember"
									type="checkbox"
									class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
									required
								/>
							</div>
							<div class="ml-3 text-sm">
								<label for="remember" class="text-gray-500 dark:text-gray-300"> Remember me </label>
							</div>
						</div>
						<!-- <a href="#" class="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500">forgot password?</a> -->
					</div>
					<Button 
						color="green"
						type="submit"
						id="submit"
						class="w-full"
						on:click={submit}
					>Sign In
					</Button>
					<p class="text-sm font-light text-gray-500 dark:text-gray-400">
						Don’t have an account yet?{" "}
						<a
							href="/register"
							class="font-medium text-primary-600 hover:underline dark:text-primary-500"
						>
							Register Now
						</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</section>

<Alert bind:open={showAlert} {message} {success}  />
