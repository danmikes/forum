import { get, writable } from 'svelte/store';
import { supabase } from '$lib/supabase.js';

export const user = writable(null);
export const flashMessages = writable([]);

supabase.auth.getSession().then(({ data: { session } }) => {
	user.set(session?.user || null);
});

supabase.auth.onAuthStateChange((event, session) => {
	if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
		user.set(session.user);
	} else if (event === 'SIGNED_OUT') {
		user.set(null);
	}
});

export function addFlashMessage(category, text) {
	flashMessages.update((messages) => [...messages, { category, text }]);

	setTimeout(() => {
		flashMessages.update((messages) => messages.filter((m) => m.text !== text));
	}, 5000);
}

export function isAdmin() {
  const adminUserId = [
    '1386d05e-89f6-45d2-bd25-13e93cc27768',
  ]

  return adminUserId.includes(get(user)?.id);
}

export function isAuthor(post) {
  return get(user)?.id === post?.author_id;
}
