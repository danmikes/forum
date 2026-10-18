<script>
  import { user } from '$lib/store.js';
  import { db, auth } from '$lib/supabase.js';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { base } from '$app/paths';

  let title = '';
  let content = '';
  let isLoading = false;
  let error = '';

  $: postId = $page.params.id;

  onMount(async () => {
    const { data: { user: currentUser } } = await auth.getUser();

    if (!currentUser) {
      goto('./login');
      return;
    }

    await loadPost();
  });

  async function loadPost() {
    isLoading = true;
    try {
      const post = await db.getPost(postId);

      const { data: { user: currentUser } } = await auth.getUser();
      if (post.author_id !== currentUser.id) {
        error = 'You can only edit your own posts';
        goto(`${base}/posts`);
        return;
      }

      title = post.title;
      content = post.content;
    } catch (err) {
      error = 'Failed to load post: ' + err.message;
    } finally {
      isLoading = false;
    }
  }

  async function handleSubmit() {
    const { data: { user: currentUser } } = await auth.getUser();

    if (!currentUser) {
      error = 'You must be logged in to edit a post';
      goto(`${base}/login`);
      return;
    }

    isLoading = true;
    error = '';

    try {
      const post = await db.updatePost(postId, {
        title: title,
        content: content
      });

      if (post) {
        goto(`${base}/posts/${postId}`);
      } else {
        error = 'Failed to update post';
      }
    } catch (err) {
      error = 'Failed to update post: ' + err.message;
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="container">
  <article class="grid">
    <div>
      <hgroup>
        <h1>Edit Post</h1>
      </hgroup>

      {#if error}
        <article class="danger">
          <header>Error</header>
          {error}
        </article>
      {/if}

      <form on:submit|preventDefault={handleSubmit}>
        <label>
          Title
          <input
            type="text"
            bind:value={title}
            placeholder="Enter post title"
            required
            disabled={isLoading}
          />
        </label>

        <label>
          Content
          <textarea
            bind:value={content}
            placeholder="Write your post content here..."
            rows="10"
            required
            disabled={isLoading}
          ></textarea>
        </label>

        <button type="submit" class="primary" disabled={isLoading}>
          {#if isLoading}Updating ...{:else}Update Post{/if}
        </button>
        <a href="posts/{postId}" role="button" class="secondary" style="width: 100%;">
          Cancel
        </a>
      </form>
    </div>
  </article>
</main>
