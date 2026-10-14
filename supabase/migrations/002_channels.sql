create table if not exists channel_core (
    channel_id text primary key,
    handle text unique not null,
    country char(2) not null,
    uploads_playlist_id text unique not null
);

do $$
begin
create type thumbnail as (
    url text, 
    width integer,
    height integer
);
exception 
    when duplicate_object then null;
end;
$$;

create table if not exists channel_details(
    channel_id text primary key references channel_core(channel_id),
    tier_id uuid references tiers(tier_id),
    title text not null,
    descr text,
    published_at timestamp,
    thumbnail_default thumbnail,
    thumbnail_md thumbnail,
    thumbnail_high thumbnail,
    thumbnail_maxres thumbnail
);

create table if not exists channel_stats(
    channel_id text primary key references channel_core(channel_id),
    view_count bigint not null default 0,
    subscriber_count bigint not null default 0,
    video_count bigint not null default 0,
    hidden_subscriber_count boolean not null default false
);


