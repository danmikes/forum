<script>
	import { user, flashMessages } from '$lib/store.js';
	import { auth } from '$lib/supabase.js';
	import { goto } from '$app/navigation';
	import { base } from '$app/paths';

	async function handleLogout() {
		await auth.signOut();
		goto('${base}/');
	}
</script>

<nav class="container-fluid">
	<ul>
		<li><strong><a href="{base}/">Forum</a></strong></li>
    <li><a href="{base}/posts">Posts</a></li>
	</ul>
	<ul>
		{#if $user}
			<li>
				<a href="profile"
					>{$user.user_metadata?.username || $user.email?.split('@')[0] || 'Profile'}</a
				>
			</li>
			<li><button type="button" class="secondary" on:click={handleLogout}>Logout</button></li>
		{:else}
			<li><a href="login" role="button">Login</a></li>
			<li><a href="register" role="button" class="secondary">Register</a></li>
		{/if}
	</ul>
</nav>

<main class="container">
	{#each $flashMessages as message}
		<article class={message.category === 'error' ? 'danger' : 'success'}>
			<header>
				{message.category.charAt(0).toUpperCase() + message.category.slice(1)}
			</header>
			{message.text}
		</article>
	{/each}

	<slot />
</main>
