// Run only from a secured administrator machine after creating the Auth user.
// Requires Application Default Credentials and server-only Supabase credentials.
const {initializeApp,applicationDefault}=require("firebase-admin/app");
const {getAuth}=require("firebase-admin/auth");
const {createClient}=require("@supabase/supabase-js");
const email=process.env.INITIAL_ADMIN_EMAIL;
if(!email||!process.env.SUPABASE_URL||!process.env.SUPABASE_SERVICE_ROLE_KEY)throw new Error("Set INITIAL_ADMIN_EMAIL, SUPABASE_URL, and SUPABASE_SERVICE_ROLE_KEY.");
initializeApp({credential:applicationDefault()});
(async()=>{const user=await getAuth().getUserByEmail(email.toLowerCase());const db=createClient(process.env.SUPABASE_URL,process.env.SUPABASE_SERVICE_ROLE_KEY,{auth:{autoRefreshToken:false,persistSession:false}});const {error}=await db.from("officers").upsert({firebase_uid:user.uid,email:user.email,role:"SUPER_ADMIN",is_active:true},{onConflict:"firebase_uid"});if(error)throw error;console.log("Initial administrator authorized.")})().catch(error=>{console.error(error.message);process.exitCode=1});
