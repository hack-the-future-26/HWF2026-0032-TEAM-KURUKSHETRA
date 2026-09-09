import type { NextConfig } from "next";
const configuredFirebaseApiUrl=process.env.FIREBASE_API_URL;
if(process.env.NODE_ENV==="production"&&!configuredFirebaseApiUrl)throw new Error("FIREBASE_API_URL is required for a production build.");
const firebaseApiUrl=(configuredFirebaseApiUrl||"http://127.0.0.1:5001/demo-project/us-central1/api").replace(/\/$/,"");
const nextConfig: NextConfig = { reactStrictMode: true, async rewrites(){return [{source:"/backend-api/:path*",destination:`${firebaseApiUrl}/:path*`}]} };
export default nextConfig;
