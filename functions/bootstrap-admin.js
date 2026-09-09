// Run only from a secured administrator machine after creating the Supabase Auth user.
// Requires server-only Supabase credentials.
const {createClient}=require("@supabase/supabase-js");
const email=process.env.INITIAL_ADMIN_EMAIL;
if(!email||!process.env.SUPABASE_URL||!process.env.SUPABASE_SERVICE_ROLE_KEY)throw new Error("Set INITIAL_ADMIN_EMAIL, SUPABASE_URL, and SUPABASE_SERVICE_ROLE_KEY.");
(async()=>{const db=createClient(process.env.SUPABASE_URL,process.env.SUPABASE_SERVICE_ROLE_KEY,{auth:{autoRefreshToken:false,persistSession:false}});const {data,error:listError}=await db.auth.admin.listUsers({page:1,perPage:1000});if(listError)throw listError;const user=data.users.find(candidate=>candidate.email?.toLowerCase()===email.toLowerCase());if(!user)throw new Error("No Supabase Auth user exists for INITIAL_ADMIN_EMAIL.");const {error}=await db.from("officers").upsert({firebase_uid:user.id,auth_user_id:user.id,email:user.email,role:"SUPER_ADMIN",is_active:true},{onConflict:"firebase_uid"});if(error)throw error;console.log("Initial administrator authorized.")})().catch(error=>{console.error(error.message);process.exitCode=1});
