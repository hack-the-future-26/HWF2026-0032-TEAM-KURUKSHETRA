import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
const protectedPaths=["/dashboard","/review","/history","/audit","/settings","/officers","/verify","/reports"];
// Firebase Auth is client-managed. Every protected API remains verified by the
// Firebase Admin SDK in Functions; this redirect is only an optimistic UI guard.
export function proxy(request:NextRequest){if(protectedPaths.some(path=>request.nextUrl.pathname.startsWith(path))&&!request.cookies.get("firebase-officer")){const url=new URL("/login",request.url);url.searchParams.set("next",request.nextUrl.pathname);return NextResponse.redirect(url)}return NextResponse.next()}
export const config={matcher:["/dashboard/:path*","/review/:path*","/history/:path*","/audit/:path*","/settings/:path*","/officers/:path*","/verify/:path*","/reports/:path*"]};
