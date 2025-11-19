<script>
	import { user } from '$lib/store.js';
	import { base } from '$app/paths';
</script>

<main class="container">
	<div class="grid">
		<section class="col-12">
			<hgroup class="text-center">
				<h1>Deep Forum</h1>
			</hgroup>

			<div class="grid" style="margin: 2rem 0;">
				<div class="col-12 col-md-4 text-center">
					<article style="border: none; padding: 1rem;">
						<h3>📝 Discuss</h3>
					</article>
				</div>
				<div class="col-12 col-md-4 text-center">
					<article style="border: none; padding: 1rem;">
						<h3>🤝 Engage</h3>
					</article>
				</div>
				<div class="col-12 col-md-4 text-center">
					<article style="border: none; padding: 1rem;">
						<h3>💡 Learn</h3>
					</article>
				</div>
			</div>

			<div class="text-center" style="margin-top: 2rem;">
				{#if $user}
					<a href="posts/create" role="button" class="secondary">Create Post</a>
				{/if}
			</div>
		</section>
	</div>
</main>
