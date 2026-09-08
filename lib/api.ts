import {getFirebaseIdToken} from "@/lib/firebase";
const base="/backend-api";
function networkMessage(){return "The officer service could not be reached. Check the Firebase Functions deployment and try again."}
export async function api<T>(path:string,init:RequestInit={}){const headers:Record<string,string>={...((init.headers||{}) as Record<string,string>)};if(!(init.body instanceof FormData))headers["content-type"]="application/json";const token=await getFirebaseIdToken();if(token)headers.authorization=`Bearer ${token}`;let response:Response;try{response=await fetch(`${base}${path}`,{...init,headers})}catch{throw new Error(networkMessage())}const body=await response.json().catch(()=>null);if(!response.ok)throw new Error(body?.error?.message||`The server returned ${response.status}.`);return body as T}
export type Page<T>={success:boolean;data:{results:T[];count:number;page:number;total_pages:number}};
export type Audit={id:string;user_email:string;action:string;event_type:string;status:string;result:string;description:string;metadata:Record<string,unknown>;created_at:string};
export type History={id:string;action:string;event_type:string;status:string;related_object:string;metadata:Record<string,unknown>;created_at:string};
