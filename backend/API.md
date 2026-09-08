# GovVerify API

All responses use `{"success": true, "data": ...}`. Session-authenticated unsafe requests require the `X-CSRFToken` header obtained from `GET /api/auth/csrf/`.

| Endpoint | Method | Role | Purpose |
|---|---|---|---|
| `/api/auth/login/` | POST | Public | Official email/password login |
| `/api/auth/logout/` | POST | Officer | Invalidate the session |
| `/api/auth/me/` | GET | Officer | Current role and account status |
| `/api/auth/register/` | POST | Invitation | Complete a valid officer invitation with `{email,token,password,password_confirmation}` |
| `/api/officers/` | GET | Super admin | List official officers |
| `/api/officers/invite/` | POST | Super admin | Create invitation with `{email}` |
| `/api/officers/{id}/activate|deactivate|revoke/` | POST | Super admin | Change officer access |
| `/api/verification/` | GET, POST | Officer | List permitted records or create `{bidder_name,document_type}` |
| `/api/verification/{id}/upload/` | POST | Owner/admin | Multipart `file` (PDF/JPEG/PNG, ≤10 MB) |
| `/api/verification/{id}/` | GET, POST | Owner/admin | Read or run verification |
| `/api/verification/providers/` | GET | Officer | Provider configuration status |
| `/api/verification/audit/` | GET | Super admin | Immutable verification audit log |

The standard verification response includes `verification_id`, `document_type`, `status`, `source`, `requires_manual_review`, documents, and result details. Provider failure/unconfigured integration returns a controlled manual-review status; no API integration is represented as official verification.

Errors use 400/401/403/404/409/422/500 as appropriate and never return credentials or internal provider secrets.
