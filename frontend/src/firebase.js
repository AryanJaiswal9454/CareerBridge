import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBhKz_qkoOAmf1vwWciaBhNyMaFJVP6u30",
  authDomain: "career-bridge-ai-50520.firebaseapp.com",
  projectId: "career-bridge-ai-50520",
  storageBucket: "career-bridge-ai-50520.firebasestorage.app",
  messagingSenderId: "867287809523",
  appId: "1:867287809523:web:7b002777791cf98a2fe686",
  measurementId: "G-6L2K6SF6T8"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export default app;