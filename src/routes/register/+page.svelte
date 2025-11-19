<script>
	import { auth } from '$lib/supabase.js';
	import { goto } from '$app/navigation';
  import { base } from '$app/paths';

	let username = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let isLoading = false;
	let error = '';

	$: passwordsMatch = password === confirmPassword;
	$: isPasswordValid = password.length >= 6;

	async function handleSubmit() {
		if (!passwordsMatch) {
			error = 'Passwords do not match';
			return;
		}

		if (!isPasswordValid) {
			error = 'Password must be at least 6 characters';
			return;
		}

		isLoading = true;
		error = '';

		try {
			const { data, error: supabaseError } = await auth.signUp(email, password, username);

			if (supabaseError) throw supabaseError;

			if (data.user) {
				goto(`${base}/`);
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
				<h2>Register</h2>
				<h3>Join our community</h3>
			</hgroup>

			{#if error}
				<article class="danger">
					<header>Error</header>
					{error}
				</article>
			{/if}

			<form on:submit|preventDefault={handleSubmit}>
				<label for="username">
					Username
					<input
						type="text"
						id="username"
						bind:value={username}
						placeholder="Choose a username"
						required
					/>
				</label>

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
						placeholder="At least 6 characters"
						required
						class:invalid={password && !isPasswordValid}
					/>
					{#if password && !isPasswordValid}
						<small style="color: var(--pico-color-red-500)"
							>Password 6 characters or more</small
						>
					{/if}
				</label>

				<label for="confirmPassword">
					Confirm Password
					<input
						type="password"
						id="confirmPassword"
						bind:value={confirmPassword}
						placeholder="Confirm your password"
						required
						class:invalid={confirmPassword && !passwordsMatch}
					/>
					{#if confirmPassword && !passwordsMatch}
						<small style="color: var(--pico-color-red-500)">Passwords match not</small>
					{/if}
				</label>

				<button
					type="submit"
					class="primary"
					disabled={isLoading || (confirmPassword && !passwordsMatch) || !isPasswordValid}
				>
					{#if isLoading}Registering ...{:else}Register{/if}
				</button>
			</form>

			<footer style="text-align: center; margin-top: 1rem;">
				<p>Have account? <a href="./login">Login!</a></p>
			</footer>
		</div>
	</article>
</main>
