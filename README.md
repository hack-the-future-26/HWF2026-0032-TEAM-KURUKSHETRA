# GeM Verify

GeM Verify is an officer-only document-verification workspace. Its production architecture is Vercel for the Next.js frontend, Firebase Authentication and Cloud Functions for identity/API handling, Supabase PostgreSQL for application data, and Firebase Storage for evidence files. Railway, Render, Django sessions, and Firestore are not part of the active deployment path.

## Supabase PostgreSQL data model

- `officers`: Firebase UID, official email, role, and active status.
- `officer_invitations`: hashed invitation token, authorized email, expiry, and acceptance state.
- `verifications` and `verification_documents`: officer-owned verification records and Firebase Storage metadata.
- `audit_logs`: append-only function audit events.
- `user_settings`: officer-owned preferences.

All protected HTTP API operations verify a Firebase ID token, then read authorization and write data through a server-only Supabase service-role client. Supabase RLS is enabled without browser policies, and Firebase Storage denies direct browser access; privileged changes flow through Cloud Functions.

## Local development

1. Copy `.env.example` to `.env.local` and fill in the Firebase web app configuration.
2. Set `FIREBASE_API_URL=http://127.0.0.1:5001/<firebase-project-id>/us-central1/api` in `.env.local`.
3. Install root and function dependencies: `npm install` and `npm install --prefix functions`.
4. Authenticate Firebase CLI and select the real project: `firebase login`, then run `firebase use --add` to add its project ID to `.firebaserc`.
5. Authenticate Supabase CLI, link the existing project, and apply the migration: `supabase login`, `supabase link`, then `supabase db push`.
6. Start the frontend: `npm run dev`.

The initial administrator must first be created in Firebase Authentication by an authorized owner. On a secured administrator machine with Application Default Credentials, run `INITIAL_ADMIN_EMAIL=owner@example.gov node functions/bootstrap-admin.js`. It only grants the already-created Firebase Auth user the Supabase PostgreSQL `SUPER_ADMIN` profile; it never accepts or stores a password.

## Production deployment

1. Enable Firebase Authentication email/password, Storage, and Cloud Functions in the selected Firebase project. Cloud Functions deployment may require billing.
2. In the linked existing Supabase project, apply `supabase/migrations/202609070001_initial_schema.sql` with `supabase db push`.
3. Store `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` as Firebase Functions secrets using `firebase functions:secrets:set`; never set them in Vercel.
4. Set the real project ID in `.firebaserc` and deploy: `firebase deploy --only functions,storage`.
5. In Vercel, set the public `NEXT_PUBLIC_FIREBASE_*` web configuration values and the server-only `FIREBASE_API_URL` to the actual deployed `api` function URL, such as `https://us-central1-your-project.cloudfunctions.net/api`.
6. Redeploy Vercel. Browser calls to `/backend-api/*` are rewritten to the Firebase HTTP function.

Never put service-account credentials, Admin SDK keys, government API credentials, or the initial administrator password in Vercel public variables or Git.

## API compatibility

The Firebase HTTP function exposes `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me`, `/officers`, `/officers/invite`, `/verification`, `/verification/{id}`, `/verification/{id}/upload`, and `/settings`. It intentionally has no Django CSRF endpoint because Firebase bearer-token authentication replaces session cookies and CSRF tokens.

The previous Django `backend/` directory is retained only as an un-deployed migration reference until the production rollout has been verified. It has no Firebase/Vercel deployment configuration.
# govverify-platform
# govverify-platform
# govverify-platform
# govverify-platform
