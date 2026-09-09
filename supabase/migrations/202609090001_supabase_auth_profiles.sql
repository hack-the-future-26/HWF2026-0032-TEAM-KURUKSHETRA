-- Additive migration: legacy Firebase-linked rows remain readable and untouched.
alter table public.officers add column if not exists auth_user_id uuid unique references auth.users(id) on delete cascade;
alter table public.officer_invitations add column if not exists accepted_auth_user_id uuid unique references auth.users(id) on delete restrict;
create index if not exists officers_auth_user_id_idx on public.officers(auth_user_id);

create or replace function public.handle_supabase_officer_signup()
returns trigger language plpgsql security definer set search_path = public as $$
declare invitation public.officer_invitations;
begin
  select * into invitation from public.officer_invitations
    where email = new.email
      and token_hash = coalesce(new.raw_user_meta_data ->> 'invitation_token_hash', '')
      and status = 'PENDING'
      and expires_at > now()
    for update;
  if not found then
    return new;
  end if;
  insert into public.officers(firebase_uid, auth_user_id, email, role, is_active)
    values (new.id::text, new.id, new.email, 'OFFICER', true);
  update public.officer_invitations
    set status = 'ACCEPTED', accepted_by = new.id::text, accepted_auth_user_id = new.id, accepted_at = now()
    where id = invitation.id;
  insert into public.audit_logs(user_uid, user_email, action, resource, status, metadata)
    values (new.id::text, new.email, 'OFFICER_REGISTERED', 'OFFICER', 'success', '{}'::jsonb);
  return new;
end $$;

drop trigger if exists on_supabase_officer_signup on auth.users;
create trigger on_supabase_officer_signup after insert on auth.users
  for each row execute procedure public.handle_supabase_officer_signup();

-- The browser never accesses application tables directly. The API uses the service role,
-- while RLS remains enabled as a defense-in-depth boundary.
insert into storage.buckets (id, name, public)
values ('verification-evidence', 'verification-evidence', false)
on conflict (id) do nothing;
