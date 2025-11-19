create table posts (
  id bigserial primary key,
  title text not null,
  content text not null,
  author_id uuid not null,
  author_name text not null,
  created_at timestamp default now()
);

create table comments (
  id bigserial primary key,
  post_id bigint references posts(id),
  content text not null,
  author_id uuid not null,
  author_name text not null,
  created_at timestamp default now()
);
