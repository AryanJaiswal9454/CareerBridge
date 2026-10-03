import api from "./axios";

function storeSession(data, fallbackUsername = "") {
  if (!data?.access || !data?.refresh) {
    throw new Error(
      "The server did not return a valid login session."
    );
  }

  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);

  localStorage.setItem(
    "username",
    data.user?.username || fallbackUsername || ""
  );

  localStorage.setItem(
    "is_staff",
    data.user?.is_staff ? "true" : "false"
  );

  localStorage.setItem(
    "is_superuser",
    data.user?.is_superuser ? "true" : "false"
  );

  localStorage.setItem(
    "email",
    data.user?.email || ""
  );
}


/* =========================
   PASSWORD LOGIN
========================= */

export async function loginUser(username, password) {
  const response = await api.post("/auth/login/", {
    username,
    password,
  });

  storeSession(response.data, username);

  return response.data;
}


/* =========================
   LOGIN OTP
========================= */

/*
 * STEP 1:
 * Request OTP using username OR email.
 */
export async function requestLoginOtp(identifier) {
  const response = await api.post(
    "/auth/login/request-otp/",
    {
      identifier: identifier.trim(),
    }
  );

  return response.data;
}


/*
 * STEP 2:
 * Verify OTP.
 *
 * Django returns the normal JWT access + refresh tokens.
 */
export async function verifyLoginOtp(email, code) {
  const response = await api.post(
    "/auth/login/verify-otp/",
    {
      email: email.trim(),
      code: code.trim(),
    }
  );

  storeSession(response.data);

  return response.data;
}


/* =========================
   PASSWORD RESET
========================= */

export async function requestPasswordResetOtp(email) {
  const response = await api.post(
    "/auth/password/request-otp/",
    {
      email: email.trim(),
    }
  );

  return response.data;
}


export async function resetPasswordOtp(
  email,
  code,
  newPassword
) {
  const response = await api.post(
    "/auth/password/reset-otp/",
    {
      email: email.trim(),
      code: code.trim(),
      new_password: newPassword,
    }
  );

  return response.data;
}


/* =========================
   SIGNUP OTP
========================= */

export async function requestSignupOtp(
  username,
  email,
  password
) {
  const response = await api.post(
    "/auth/signup/request-otp/",
    {
      username,
      email,
      password,
    }
  );

  return response.data;
}


export async function verifySignupOtp(email, code) {
  const response = await api.post(
    "/auth/signup/verify-otp/",
    {
      email: email.trim(),
      code: code.trim(),
    }
  );

  storeSession(response.data);

  return response.data;
}


export async function resendSignupOtp(email) {
  const response = await api.post(
    "/auth/signup/resend-otp/",
    {
      email: email.trim(),
    }
  );

  return response.data;
}


/* =========================
   CHANGE PASSWORD
========================= */

export async function changePassword(
  currentPassword,
  newPassword,
  confirmPassword = ""
) {
  const response = await api.post(
    "/auth/password/change/",
    {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    }
  );

  return response.data;
}


/* =========================
   SESSION HELPERS
========================= */

export function logoutUser() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("username");
  localStorage.removeItem("is_staff");
  localStorage.removeItem("is_superuser");
  localStorage.removeItem("email");
}


export function isAuthenticated() {
  return !!localStorage.getItem("access_token");
}


export function isStaffUser() {
  return localStorage.getItem("is_staff") === "true";
}