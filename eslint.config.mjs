import nextVitals from "eslint-config-next/core-web-vitals";

const config = [
  { ignores: [".next/**", "backend/**", "coverage/**", "functions/**", "supabase/.temp/**"] },
  ...nextVitals,
];

export default config;
