alter table tiers 
drop constraint tiers_tier_name_check;

alter table tiers 
add constraint tiers_tier_name_check 
check (tier_name in ('core', 'mantle', 'crust', 'archive'));

insert into tiers (tier_name, threshold)
values ('core', 0.75),
       ('mantle', 0.40),
       ('crust', 0.15),
       ('archive', 0);