<script>
	import { user } from '$lib/store.js';
	import { auth } from '$lib/supabase.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
  import { base } from '$app/paths';

	let isLoading = true;

	onMount(async () => {
		const {
			data: { user: currentUser }
		} = await auth.getUser();

		if (!currentUser) {
			goto(`${base}/login`);
		} else {
			isLoading = false;
		}
	});

	async function handleLogout() {
		await auth.signOut();
		goto(`${base}/`);
	}
</script>

{#if isLoading}
	<main class="container">
		<article class="text-center">
			<p>Loading ...</p>
		</article>
	</main>
{:else if $user}
	<main class="container">
		<article class="grid">
			<div class="text-center">
				<hgroup>
					<h2>Profile</h2>
					<h3>Your Account</h3>
				</hgroup>

				<dl style="text-align: left; max-width: 300px; margin: 0 auto;">
					<dt><strong>Username</strong></dt>
					<dd>{$user.user_metadata?.username || $user.email?.split('@')[0] || 'User'}</dd>

					<dt><strong>Email</strong></dt>
					<dd>{$user.email}</dd>

					<dt><strong>User ID</strong></dt>
					<dd><kbd>{$user.id?.slice(0, 8)}...</kbd></dd>

					{#if $user.role || $user.user_metadata?.role}
						<dt><strong>Role</strong></dt>
						<dd>{$user.role || $user.user_metadata?.role}</dd>
					{/if}
				</dl>

				<div class="grid" style="gap: 1rem; margin-top: 2rem; max-width: 300px; margin: 2rem auto;">
					<a href="./" role="button" class="primary">Back to Forum</a>
					<button on:click={handleLogout} class="secondary">Logout</button>
				</div>
			</div>
		</article>
	</main>
{:else}
	<main class="container">
		<article class="text-center">
			<p>Redirecting to login...</p>
		</article>
	</main>
{/if}
