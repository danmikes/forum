import { createClient } from '@supabase/supabase-js';
import { env } from '$env/dynamic/public';

const supabaseUrl = env.PUBLIC_SUPABASE_URL;
const supabaseKey = env.PUBLIC_SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
	throw new Error('Missing SupaBase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseKey);

export const auth = {
	async signIn(email, password) {
		const { data, error } = await supabase.auth.signInWithPassword({
			email,
			password
		});
		return { data, error };
	},

	async signUp(email, password, username) {
		const { data, error } = await supabase.auth.signUp({
			email,
			password,
			options: {
				data: {
					username: username
				}
			}
		});
		return { data, error };
	},

	async signOut() {
		const { error } = await supabase.auth.signOut();
		return { error };
	},

	async getSession() {
		const { data, error } = await supabase.auth.getSession();
		return { data, error };
	},

	async getUser() {
		const { data, error } = await supabase.auth.getUser();
		return { data, error };
	},

	async resetPassword(email) {
		const { data, error } = await supabase.auth.resetPasswordForEmail(email);
		return { data, error };
	}
};

export const db = {
	async getPosts() {
		const { data, error } = await supabase
			.from('posts')
			.select('*')
			.order('created_at', { ascending: false });

		if (error) throw error;
		return data;
	},

	async getPost(id) {
		const { data, error } = await supabase.from('posts').select('*').eq('id', id).single();

		if (error) throw error;
		return data;
	},

	async createPost(post) {
		const {
			data: { user }
		} = await supabase.auth.getUser();
		const postWithUser = {
			...post,
			author_id: user?.id,
			author_name: user?.user_metadata?.username || user?.email
		};

		const { data, error } = await supabase.from('posts').insert([postWithUser]).select().single();

		if (error) throw error;
		return data;
	},

	async updatePost(id, { title, content }) {
		const { data, error } = await supabase
			.from('posts')
			.update({
        title,
        content
      })
			.eq('id', id)
			.select()
			.single();

		if (error) throw error;
		return data;
	},

	async deletePost(id) {
		const { error: commentsError } = await supabase.from('comments').delete().eq('post_id', id);

		if (commentsError) throw commentsError;

		const { error } = await supabase.from('posts').delete().eq('id', id);

		if (error) throw error;
		return true;
	},

	async getComments(postId) {
		const { data, error } = await supabase
			.from('comments')
			.select('*')
			.eq('post_id', postId)
			.order('created_at', { ascending: true });

		if (error) throw error;
		return data;
	},

	async createComment(comment) {
		const {
			data: { user }
		} = await supabase.auth.getUser();
		const commentWithUser = {
			...comment,
			author_id: user?.id,
			author_name: user?.user_metadata?.username || user?.email
		};

		const { data, error } = await supabase
			.from('comments')
			.insert([commentWithUser])
			.select()
			.single();

		if (error) throw error;
		return data;
	}
};
