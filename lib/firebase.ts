"use client";
import {getApp,getApps,initializeApp} from "firebase/app";
import {getAuth,onAuthStateChanged,signInWithEmailAndPassword,signOut,User} from "firebase/auth";
const config={apiKey:process.env.NEXT_PUBLIC_FIREBASE_API_KEY,authDomain:process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,projectId:process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,storageBucket:process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,appId:process.env.NEXT_PUBLIC_FIREBASE_APP_ID};
function auth(){if(typeof window==="undefined")throw new Error("Firebase Auth is only available in the browser.");if(!config.apiKey||!config.authDomain||!config.projectId||!config.appId)throw new Error("Firebase web configuration is missing.");return getAuth(getApps().length?getApp():initializeApp(config));}
export const signInOfficer=(email:string,password:string)=>signInWithEmailAndPassword(auth(),email,password);
export const signOutOfficer=()=>signOut(auth());
export const getFirebaseIdToken=async()=>auth().currentUser?.getIdToken()||null;
export const waitForFirebaseUser=()=>new Promise<User|null>(resolve=>{const stop=onAuthStateChanged(auth(),user=>{stop();resolve(user)})});
