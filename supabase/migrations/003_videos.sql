create table if not exists video_core (
    video_id text primary key,
    channel_id text not null references channel_core(channel_id),

    title text not null,
    descr text,
    duration integer not null,
    published_at timestamp not null,
    view_count integer not null,
    like_count integer not null,
    comment_count integer not null,
    thumbnail_default thumbnail,
    thumbnail_md thumbnail,
    thumbnail_high thumbnail,
    thumbnail_standard thumbnail,
    thumbnail_maxres thumbnail,
    category_id text,
    live_broadcast_content text,
    default_language text
);
