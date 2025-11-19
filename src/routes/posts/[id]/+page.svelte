<script>
	import { user, isAdmin, isAuthor } from '$lib/store.js';
	import { db } from '$lib/supabase.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
  import { base } from '$app/paths';

	let post = null;
	let comments = [];
	let newComment = '';
	let isLoading = true;
	let isSubmitting = false;
	let error = '';

	$: postId = $page.params.id;

	onMount(async () => {
		await loadPostAndComments();
	});

	async function loadPostAndComments() {
		try {
			post = await db.getPost(postId);
			comments = await db.getComments(postId);

			if (!post) {
				error = 'Post not found';
			}
		} catch (err) {
			error = 'Failed to load post: ' + err.message;
		} finally {
			isLoading = false;
		}
	}

	function formatTime(timestamp) {
		if (!timestamp) return 'Recently';
		const date = new Date(timestamp);
		return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
	}

	async function editPost() {
    goto(`${base}/posts/${postId}/edit`);
	}

	async function deletePost() {
		if (!confirm('Delete post?')) return;

		try {
			const result = await db.deletePost(postId);

			if (result) {
				goto(`${base}/posts`);
			} else {
				error = 'Failed to delete post';
			}
		} catch (err) {
			error = 'Failed to delete post: ' + err.message;
		}
	}

	async function addComment() {
		if (!$user) {
			goto(`${base}/login`);
			return;
		}

		isSubmitting = true;
		error = '';

		try {
			const comment = await db.createComment({
				content: newComment,
				post_id: postId
			});

			if (comment) {
				newComment = '';
				await loadPostAndComments();
			} else {
				error = 'Failed to add comment';
			}
		} catch (err) {
			error = 'Failed to add comment: ' + err.message;
		} finally {
			isSubmitting = false;
		}
	}
</script>

{#if isLoading}
	<main class="container">
		<article>
			<p>Loading ...</p>
		</article>
	</main>
{:else if error}
	<main class="container">
		<article class="danger">
			<header>Error</header>
			{error}
		</article>
	</main>
{:else if post}
	<main class="container">
		<div class="grid">
			<div class="col-12 col-md-8">
				<article>
					<header>
						<h1>{post.title}</h1>
					</header>
          <div style="white-space: pre-wrap; line-height: 1.5;">
            {post.content}
          </div>
					<footer class="grid">
						<div>
							<small><strong>By : </strong>{post.author_name}</small>
							<br />
							<small><strong>Posted : </strong>{formatTime(post.created_at)}</small>
						</div>
            {#if isAuthor }
              <div class="text-right">
                <button type="button" class="secondary small" on:click={editPost}>
                  Edit
                </button>
              </div>
            {/if}
						{#if isAdmin() || isAuthor(post)}
							<div class="text-right">
								<button type="button" class="secondary small" on:click={deletePost}>
									Delete
								</button>
							</div>
						{/if}
					</footer>
				</article>

				<section aria-label="Comments">
					<header>
						<h2>Comments ({comments.length})</h2>
					</header>

					{#if $user}
						<form on:submit|preventDefault={addComment}>
							<label for="content">
								Add comment
								<textarea
									id="content"
									bind:value={newComment}
									placeholder="Share your thoughts ..."
									rows="3"
									required
									disabled={isSubmitting}
								></textarea>
							</label>
							<button type="submit" class="primary" disabled={isSubmitting}>
								{#if isSubmitting}Posting ...{:else}Post Comment{/if}
							</button>
						</form>
					{:else}
						<article class="secondary">
							<p><a href="login">Log in</a> to comment</p>
						</article>
					{/if}

					{#each comments as comment}
						<article>
							<blockquote style="white-space: pre-wrap; line-height: 1.5;">{comment.content}</blockquote>
							<footer>
								<div class="grid">
									<div>
										<small><strong>By : </strong>{comment.author_name}</small>
									</div>
									<div class="text-right">
										<small><strong>Posted : </strong>{formatTime(comment.created_at)}</small>
									</div>
								</div>
							</footer>
						</article>
					{/each}

					{#if comments.length === 0}
						<article class="secondary">
							<p>No comments</p>
						</article>
					{/if}
				</section>
			</div>
		</div>
	</main>
{:else}
	<main class="container">
		<article class="danger">
			<header>Error</header>
			Post not found
		</article>
	</main>
{/if}
