create table if not exists tiers(
    tier_id uuid primary key default gen_random_uuid(),
    tier_name text not null unique check(tier_name in ('core', 'mantle', 'crust')),
    threshold decimal(3,2) not null unique check (threshold between 0 and 1)
)