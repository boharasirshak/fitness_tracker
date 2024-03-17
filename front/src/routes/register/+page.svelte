<script lang="ts">
	import { goto } from "$app/navigation";
	import Alert from "$lib/components/Alert.svelte";
	import { isAuthenticated } from "$lib/stores";
	import { Button, Checkbox, Modal } from "flowbite-svelte";

	let defaultModal = false;
	let email = "";
	let message = "";
	let showAlert = false;
	let success = false;

	const alert = (msg: string, suc: boolean) => {
		showAlert = true;
		message = msg;
		success = suc;
	};

	console.log($isAuthenticated);

	const submit = async () => {
		const backendUrl = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";

		if (!email) {
			return alert("Please fill in all fields", false);
		}

		const res = await fetch(`${backendUrl}/api/v1/auth/register`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ email })
		});

		if (res.status >= 500) {
			return alert("Internal Server Error!", false);
		}

		const data = await res.json();
		if (res.status == 200) {
			alert(data.message, true);
		} else if (res.status === 409) {
			alert(data.detail, false);
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
					Register an new account
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
					<div class="flex items-center justify-between">
						<Checkbox>
							I agree with the
							<!-- svelte-ignore a11y-click-events-have-key-events -->
							<!-- svelte-ignore a11y-no-static-element-interactions -->
							<span
								on:click={() => (defaultModal = true)}
								class="text-primary-600 dark:text-primary-500 hover:underline ms-1 cursor-pointer"
								>terms and conditions</span
							>
							.
						</Checkbox>
					</div>
					<Modal title="Terms of Service" bind:open={defaultModal} autoclose>
						<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
							With less than a month to go before the European Union enacts new consumer privacy
							laws for its citizens, companies around the world are updating their terms of service
							agreements to comply.
						</p>
						<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
							The European Union’s General Data Protection Regulation (G.D.P.R.) goes into effect on
							May 25 and is meant to ensure a common set of data rights in the European Union. It
							requires organizations to notify users as soon as possible of high-risk data breaches
							that could personally affect them.
						</p>
						<svelte:fragment slot="footer">
							<Button>I accept</Button>
						</svelte:fragment>
					</Modal>

					<Button color="green" type="submit" id="submit" class="w-full" on:click={submit}
						>Register
					</Button>
					<p class="text-sm font-light text-gray-500 dark:text-gray-400">
						Already have an account? {" "}
						<a
							href="/login"
							class="font-medium text-primary-600 hover:underline dark:text-primary-500"
						>
							Login Now
						</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</section>

<Alert bind:open={showAlert} {message} {success} />
