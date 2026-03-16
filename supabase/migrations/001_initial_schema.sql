-- Deal Hunter Pro X — Initial Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- USERS (extends Supabase auth.users)
create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  name text,
  access_code text unique,
  plan text default 'free' check (plan in ('free', 'pro')),
  sub_start date,
  sub_end date,
  telegram_chat_id text,
  created_at timestamptz default now()
);

-- DEALS
create table public.deals (
  id uuid default uuid_generate_v4() primary key,
  platform text not null,
  title text not null,
  price numeric not null,
  market_price numeric,
  discount_pct numeric generated always as (
    case when market_price > 0
    then round(((market_price - price) / market_price) * 100, 1)
    else null end
  ) stored,
  is_smoking_deal boolean generated always as (
    case when market_price > 0
    then ((market_price - price) / market_price) >= 0.35
    else false end
  ) stored,
  category text,
  location text,
  scam_score numeric default 0,
  listing_url text,
  seller_info jsonb,
  scraped_at timestamptz default now(),
  expires_at timestamptz default now() + interval '7 days',
  is_active boolean default true
);

-- DEAL VIEWS (exclusivity tracking)
create table public.deal_views (
  id uuid default uuid_generate_v4() primary key,
  deal_id uuid references public.deals(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  viewed_at timestamptz default now(),
  unique(deal_id, user_id)
);

-- ALERTS (user-defined watchlist)
create table public.alerts (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  keywords text[],
  max_price numeric,
  platform text,
  category text,
  active boolean default true,
  created_at timestamptz default now()
);

-- SCRAPE JOBS (track scraper health)
create table public.scrape_jobs (
  id uuid default uuid_generate_v4() primary key,
  platform text not null,
  started_at timestamptz default now(),
  finished_at timestamptz,
  deals_found int default 0,
  status text default 'running' check (status in ('running', 'success', 'failed')),
  error_msg text
);

-- Row Level Security
alter table public.profiles enable row level security;
alter table public.deals enable row level security;
alter table public.deal_views enable row level security;
alter table public.alerts enable row level security;

-- Policies: users see their own profile
create policy "own profile" on public.profiles
  for all using (auth.uid() = id);

-- Policies: active deals visible to all authenticated users
create policy "deals visible to auth users" on public.deals
  for select using (auth.role() = 'authenticated' and is_active = true);

-- Policies: users manage their own views + alerts
create policy "own views" on public.deal_views
  for all using (auth.uid() = user_id);

create policy "own alerts" on public.alerts
  for all using (auth.uid() = user_id);

-- Auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, name)
  values (new.id, new.raw_user_meta_data->>'name');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
