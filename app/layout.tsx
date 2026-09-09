import "./globals.css";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "GeM Verify", description: "AI-assisted public procurement compliance" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
