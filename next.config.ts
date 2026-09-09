import type { NextConfig } from "next";
const configuredApiUrl=process.env.API_URL;
if(process.env.NODE_ENV==="production"&&!configuredApiUrl)throw new Error("API_URL is required for a production build.");
const apiUrl=(configuredApiUrl||"http://127.0.0.1:5001/demo-project/us-central1/api").replace(/\/$/,"");
const nextConfig: NextConfig = { reactStrictMode: true, async rewrites(){return [{source:"/backend-api/:path*",destination:`${apiUrl}/:path*`}]} };
export default nextConfig;
