alter table channel_core alter column country drop not null;

alter table channel_details alter column published_at drop not null;

alter table video_core alter column like_count drop not null;
alter table video_core alter column comment_count drop not null;
