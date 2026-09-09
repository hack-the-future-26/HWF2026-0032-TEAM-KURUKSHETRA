create extension if not exists pgcrypto;
create extension if not exists citext;

create table public.officers (
  firebase_uid text primary key check (char_length(firebase_uid) between 1 and 128),
  email citext not null unique,
  role text not null default 'OFFICER' check (role in ('SUPER_ADMIN','OFFICER')),
  is_active boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table public.officer_invitations (
  id uuid primary key default gen_random_uuid(),
  email citext not null unique,
  token_hash text not null unique,
  status text not null default 'PENDING' check (status in ('PENDING','ACCEPTED','REVOKED','EXPIRED')),
  created_by text not null references public.officers(firebase_uid) on delete restrict,
  accepted_by text references public.officers(firebase_uid) on delete restrict,
  expires_at timestamptz not null,
  accepted_at timestamptz,
  revoked_at timestamptz,
  created_at timestamptz not null default now(),
  check ((status = 'ACCEPTED') = (accepted_at is not null))
);
create table public.verifications (
  id uuid primary key default gen_random_uuid(),
  verification_id text not null unique,
  bidder_name text not null check (char_length(trim(bidder_name)) > 0),
  document_type text not null check (char_length(trim(document_type)) > 0),
  status text not null default 'PENDING' check (status in ('PENDING','VERIFIED','FAILED','PARTIALLY_VERIFIED','MANUAL_REVIEW','API_UNAVAILABLE','INVALID_DOCUMENT')),
  source text not null default 'MANUAL_VERIFICATION_REQUIRED',
  requires_manual_review boolean not null default true,
  officer_uid text not null references public.officers(firebase_uid) on delete restrict,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table public.verification_documents (
  id uuid primary key default gen_random_uuid(),
  verification_id uuid not null references public.verifications(id) on delete cascade,
  original_name text not null,
  mime_type text not null check (mime_type in ('application/pdf','image/jpeg','image/png')),
  size_bytes bigint not null check (size_bytes between 1 and 10485760),
  sha256 char(64) not null,
  storage_path text not null unique,
  created_at timestamptz not null default now()
);
create table public.audit_logs (
  id uuid primary key default gen_random_uuid(),
  user_uid text references public.officers(firebase_uid) on delete set null,
  user_email citext,
  action text not null,
  resource text not null,
  status text not null default 'success',
  result text,
  description text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create table public.user_settings (
  officer_uid text primary key references public.officers(firebase_uid) on delete cascade,
  full_name text not null default '',
  job_title text not null default '',
  notification_preferences jsonb not null default '{"email":true}'::jsonb,
  ai_preferences jsonb not null default '{"concise":true}'::jsonb,
  updated_at timestamptz not null default now()
);
create index verifications_officer_created_idx on public.verifications(officer_uid, created_at desc);
create index verifications_status_created_idx on public.verifications(status, created_at desc);
create index audit_logs_created_idx on public.audit_logs(created_at desc);
create index audit_logs_user_created_idx on public.audit_logs(user_uid, created_at desc);
create index invitations_pending_expiry_idx on public.officer_invitations(expires_at) where status = 'PENDING';
alter table public.officers enable row level security;
alter table public.officer_invitations enable row level security;
alter table public.verifications enable row level security;
alter table public.verification_documents enable row level security;
alter table public.audit_logs enable row level security;
alter table public.user_settings enable row level security;

create or replace function public.set_updated_at()
returns trigger language plpgsql as $$ begin new.updated_at = now(); return new; end $$;
create trigger officers_set_updated_at before update on public.officers for each row execute function public.set_updated_at();
create trigger verifications_set_updated_at before update on public.verifications for each row execute function public.set_updated_at();
create trigger settings_set_updated_at before update on public.user_settings for each row execute function public.set_updated_at();

create or replace function public.accept_officer_invitation(p_invitation_id uuid,p_uid text,p_email citext)
returns void language plpgsql security definer set search_path = public as $$
declare invitation public.officer_invitations;
begin
  select * into invitation from public.officer_invitations where id = p_invitation_id for update;
  if not found or invitation.status <> 'PENDING' or invitation.expires_at <= now() or invitation.email <> p_email then
    raise exception 'Invalid or expired invitation';
  end if;
  insert into public.officers(firebase_uid,email,role,is_active) values (p_uid,p_email,'OFFICER',true);
  update public.officer_invitations set status='ACCEPTED',accepted_by=p_uid,accepted_at=now() where id=p_invitation_id;
  insert into public.audit_logs(user_uid,user_email,action,resource,status,metadata) values(p_uid,p_email,'OFFICER_REGISTERED','OFFICER','success','{}');
end $$;

revoke all on function public.accept_officer_invitation(uuid,text,citext) from public;
grant execute on function public.accept_officer_invitation(uuid,text,citext) to service_role;
