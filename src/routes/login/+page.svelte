<script>
	import { auth } from '$lib/supabase.js';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let isLoading = false;
	let error = '';

	async function handleSubmit() {
		isLoading = true;
		error = '';

		try {
			const { data, error: supabaseError } = await auth.signIn(email, password);

			if (supabaseError) throw supabaseError;

			if (data.user) {
				goto('./');
			}
		} catch (err) {
			error = err.message;
		} finally {
			isLoading = false;
		}
	}
</script>

<main class="container">
	<article class="grid">
		<div style="max-width: 400px; margin: 0 auto;">
			<hgroup style="text-align: center;">
				<h2>Login</h2>
				<h3>ReWelcome</h3>
			</hgroup>

			{#if error}
				<article class="danger">
					<header>Error</header>
					{error}
				</article>
			{/if}

			<form on:submit|preventDefault={handleSubmit}>
				<label for="email">
          Email
					<input type="email" id="email" bind:value={email} placeholder="your@email.com" required />
				</label>
				<label for="password">
					Password
					<input
						type="password"
						id="password"
						bind:value={password}
						placeholder="Enter your password"
						required
					/>
				</label>
				<button type="submit" class="primary" disabled={isLoading}>
					{#if isLoading}Logging in ...{:else}Login{/if}
				</button>
			</form>

			<footer style="text-align: center; margin-top: 1rem;">
				<p>No account? <a href="./register">Register!</a></p>
			</footer>
		</div>
	</article>
</main>
