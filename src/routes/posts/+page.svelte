<script>
	import { goto } from '$app/navigation';
	import { user, isAdmin, isAuthor } from '$lib/store.js';
	import { db } from '$lib/supabase.js';
	import { onMount } from 'svelte';
  import { base } from '$app/paths';

	let posts = [];
	let isLoading = true;
	let error = '';

	onMount(async () => {
		try {
			posts = await db.getPosts();
		} catch (err) {
			console.error('Failed to fetch posts:', err);
			error = 'Failed to load posts';
		} finally {
			isLoading = false;
		}
	});

	function formatTime(timestamp) {
		if (!timestamp) return '';
		const date = new Date(timestamp);
		return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
	}

	async function editPost(id) {
    goto(`${base}/posts/${id}/edit`);
	}

  async function deletePost(id) {
		if (!confirm('Delete Post?')) return;

		try {
			const result = await db.deletePost(id);

			if (result) {
				posts = posts.filter((post) => post.id !== id);
			} else {
				alert('Failed to delete post');
			}
		} catch (err) {
			console.error('Failed to delete post', err);
			alert('Failed to delete post: ' + err.message);
		}
	}
</script>

<main class="container">
	<div class="grid">
		<section class="col-12 col-md-8">
			<div class="row" style="display: flex; justify-content: space-between; align-items: center;">
				<h1>Posts</h1>

				{#if $user}
					<a href="posts/create" role="button" class="secondary">Create Post</a>
				{/if}
			</div>

			{#if error}
				<article class="danger">
					<header>Error</header>
					{error}
				</article>
			{/if}

			{#if isLoading}
				<article>
					<p>Loading posts ...</p>
				</article>
			{:else if posts.length > 0}
				{#each posts as post (post.id)}
					<article>
						<header>
							<h2><a href="posts/{post.id}">{post.title}</a></h2>
						</header>
						<div style="white-space: pre-wrap; line-height: 1.5;">
							{post.content.slice(0, 200)}{#if post.content.length > 200}...{/if}
            </div>
						<footer class="grid">
							<div>
								<small><strong>By : </strong> {post.author_name}</small>
								<br />
								<small><strong>Posted : </strong> {formatTime(post.created_at)}</small>
							</div>
							{#if isAdmin() || isAuthor(post) }
								<div class="text-right">
									<button
										type="button"
										class="secondary small"
										on:click={() => editPost(post.id)}
									>
										Edit
									</button>
								</div>
								<div class="text-right">
									<button
										type="button"
										class="secondary small"
										on:click={() => deletePost(post.id)}
									>
										Delete
									</button>
								</div>
							{/if}
						</footer>
					</article>
				{/each}
			{:else}
				<article class="text-center">
					<p>No posts</p>
				</article>
			{/if}
		</section>
	</div>
</main>
