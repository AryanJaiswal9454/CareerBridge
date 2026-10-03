import {
  createUserWithEmailAndPassword,
  sendEmailVerification,
  reload,
} from "firebase/auth";

import { auth } from "../firebase";


export async function createFirebaseAccount(email, password) {
  const credential = await createUserWithEmailAndPassword(
    auth,
    email,
    password
  );

  await sendEmailVerification(credential.user);

  return credential.user;
}


export async function isFirebaseEmailVerified() {
  const user = auth.currentUser;

  if (!user) {
    throw new Error("No Firebase signup session found.");
  }

  await reload(user);

  return auth.currentUser.emailVerified;
}


export async function getFirebaseIdToken(forceRefresh = true) {
  const user = auth.currentUser;

  if (!user) {
    throw new Error("No Firebase authentication session found.");
  }

  return await user.getIdToken(forceRefresh);
}