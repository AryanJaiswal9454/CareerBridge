import { useEffect, useState } from "react";
import {
  Link,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import {
  requestPasswordResetOtp,
  resetPasswordOtp,
} from "../api/auth";

import {
  ErrorBox,
  SuccessBox,
} from "../components/Ui";

import OtpInput from "../components/OtpInput";

const OTP_COOLDOWN_SECONDS = 30;


/* =========================================================
   OTP COOLDOWN HELPERS
========================================================= */

function getCooldownKey(type, email) {
  return `careerbridge_${type}_otp_cooldown_${email
    .trim()
    .toLowerCase()}`;
}


function getStoredCooldown(type, email) {
  if (!email?.trim()) {
    return 0;
  }

  const key = getCooldownKey(
    type,
    email
  );

  const expiresAt = Number(
    sessionStorage.getItem(key) || 0
  );

  const remaining = Math.ceil(
    (expiresAt - Date.now()) / 1000
  );

  if (remaining <= 0) {
    sessionStorage.removeItem(key);
    return 0;
  }

  return remaining;
}


function saveCooldown(type, email) {
  const expiresAt =
    Date.now() +
    OTP_COOLDOWN_SECONDS * 1000;

  sessionStorage.setItem(
    getCooldownKey(type, email),
    String(expiresAt)
  );
}


/* =========================================================
   LOGIN PAGE
========================================================= */

export default function Login() {
  const { login } = useAuth();

  const navigate = useNavigate();

  /*
   * password
   * reset
   */
  const [mode, setMode] =
    useState("password");


  /* =========================
     PASSWORD LOGIN
  ========================= */

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");


  /* =========================
     PASSWORD RESET
  ========================= */

  const [resetEmail, setResetEmail] =
    useState("");

  const [resetOtp, setResetOtp] =
    useState("");

  const [newPassword, setNewPassword] =
    useState("");

  const [resetSent, setResetSent] =
    useState(false);

  const [resetCooldown, setResetCooldown] =
    useState(0);


  /* =========================
     GENERAL STATE
  ========================= */

  const [error, setError] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [busy, setBusy] =
    useState(false);


  /* =========================================================
     RESEND COOLDOWN TIMER
  ========================================================= */

  useEffect(() => {
    if (
      !resetSent ||
      !resetEmail
    ) {
      setResetCooldown(0);
      return undefined;
    }

    setResetCooldown(
      getStoredCooldown(
        "reset",
        resetEmail
      )
    );

    const timer =
      window.setInterval(() => {
        setResetCooldown(
          getStoredCooldown(
            "reset",
            resetEmail
          )
        );
      }, 1000);

    return () =>
      window.clearInterval(timer);
  }, [
    resetSent,
    resetEmail,
  ]);


  /* =========================================================
     HELPERS
  ========================================================= */

  function clearMessages() {
    setError("");
    setMessage("");
  }


  function switchMode(next) {
    setMode(next);

    clearMessages();

    if (next === "password") {
      setResetSent(false);
      setResetOtp("");
      setNewPassword("");
      setResetCooldown(0);
    }
  }


  function openForgotPassword() {
    setMode("reset");

    clearMessages();

    setResetSent(false);
    setResetOtp("");
    setNewPassword("");
  }


  /* =========================================================
     PASSWORD LOGIN
  ========================================================= */

  async function submitPassword(event) {
    event.preventDefault();

    clearMessages();

    setBusy(true);

    try {
      await login(
        username,
        password
      );

      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Unable to sign in."
      );
    } finally {
      setBusy(false);
    }
  }


  /* =========================================================
     SEND PASSWORD RESET OTP
  ========================================================= */

  async function sendResetOtp(event) {
    event?.preventDefault();

    clearMessages();

    if (!resetEmail.trim()) {
      setError(
        "Enter the email connected to your account."
      );

      return;
    }


    /*
     * Prevent duplicate OTP requests.
     */
    const existingCooldown =
      getStoredCooldown(
        "reset",
        resetEmail
      );

    if (existingCooldown > 0) {
      setResetCooldown(
        existingCooldown
      );

      setError(
        `Please wait ${existingCooldown} seconds before requesting another OTP.`
      );

      return;
    }


    setBusy(true);

    try {
      const result =
        await requestPasswordResetOtp(
          resetEmail
        );


      /*
       * Start cooldown only after
       * successful OTP request.
       */
      saveCooldown(
        "reset",
        resetEmail
      );

      setResetCooldown(
        OTP_COOLDOWN_SECONDS
      );

      setResetSent(true);

      setResetOtp("");

      setMessage(
        result.message ||
        "Password reset OTP sent. Check your email."
      );
    } catch (err) {
      const serverMessage =
        err.response?.data?.error ||
        "Unable to send reset OTP.";


      /*
       * Support backend rate limiting
       * if it is added later.
       */
      if (
        err.response?.status === 429
      ) {
        const retryAfter =
          Number(
            err.response?.data
              ?.retry_after || 30
          );

        saveCooldown(
          "reset",
          resetEmail
        );

        setResetCooldown(
          retryAfter
        );
      }

      setError(serverMessage);
    } finally {
      setBusy(false);
    }
  }


  /* =========================================================
     RESET PASSWORD
  ========================================================= */

  async function resetPassword(event) {
    event.preventDefault();

    clearMessages();


    if (resetOtp.length !== 6) {
      setError(
        "Enter the complete 6-digit OTP."
      );

      return;
    }


    if (newPassword.length < 6) {
      setError(
        "New password must be at least 6 characters."
      );

      return;
    }


    setBusy(true);

    try {
      await resetPasswordOtp(
        resetEmail,
        resetOtp,
        newPassword
      );


      setMessage(
        "Password reset successfully. You can now sign in with your new password."
      );


      setMode("password");

      setResetSent(false);
      setResetOtp("");
      setNewPassword("");
      setResetCooldown(0);

      setPassword("");
    } catch (err) {
      setError(
        err.response?.data?.error ||
        "Unable to reset password."
      );
    } finally {
      setBusy(false);
    }
  }


  /* =========================================================
     UI
  ========================================================= */

  return (
    <AuthScreen
      title="Welcome back"
      text="Sign in with your password or securely reset it if you have forgotten it."
    >

      {/* =====================================================
          LOGIN MODE SELECTOR
      ===================================================== */}

      <div
        className="segmented"
        style={{
          marginBottom: 16,
        }}
      >
        <button
          type="button"
          className={
            mode === "password"
              ? "selected"
              : ""
          }
          onClick={() =>
            switchMode("password")
          }
        >
          Password
        </button>

        <button
          type="button"
          className={
            mode === "reset"
              ? "selected"
              : ""
          }
          onClick={
            openForgotPassword
          }
        >
          Forgot Password
        </button>
      </div>


      <ErrorBox>
        {error}
      </ErrorBox>

      <SuccessBox>
        {message}
      </SuccessBox>


      {/* =====================================================
          NORMAL PASSWORD LOGIN
      ===================================================== */}

      {mode === "password" && (
        <form
          className="auth-form"
          onSubmit={submitPassword}
        >

          <label>
            Username or email

            <input
              value={username}
              onChange={(e) =>
                setUsername(
                  e.target.value
                )
              }
              required
              autoComplete="username"
              placeholder="Username or email"
            />
          </label>


          <label>
            Password

            <input
              type="password"
              value={password}
              onChange={(e) =>
                setPassword(
                  e.target.value
                )
              }
              required
              autoComplete="current-password"
              placeholder="Enter password"
            />
          </label>


          {/* Forgot password shortcut */}

          <div
            style={{
              display: "flex",
              justifyContent:
                "flex-end",
              marginTop: -7,
            }}
          >
            <button
              type="button"
              onClick={
                openForgotPassword
              }
              style={{
                border: 0,
                background:
                  "transparent",
                color: "#22D3EE",
                cursor: "pointer",
                padding: 0,
                fontSize: 12,
                fontWeight: 700,
              }}
            >
              Forgot password?
            </button>
          </div>


          <button
            className="button primary full"
            disabled={busy}
          >
            {busy
              ? "Signing in…"
              : "Sign in to CareerBridge"}
          </button>

        </form>
      )}


      {/* =====================================================
          FORGOT PASSWORD
      ===================================================== */}

      {mode === "reset" && (
        <div className="auth-form">

          <h3
            style={{
              margin: 0,
            }}
          >
            Reset your password
          </h3>


          {/* =================================================
              STEP 1 — EMAIL
          ================================================= */}

          {!resetSent ? (
            <form
              className="auth-form"
              onSubmit={
                sendResetOtp
              }
            >

              <p
                className="muted"
                style={{
                  margin: 0,
                }}
              >
                Enter the email linked
                to your CareerBridge
                account. We will send
                a 6-digit verification
                code.
              </p>


              <label>
                Account email

                <input
                  type="email"
                  value={resetEmail}
                  onChange={(e) =>
                    setResetEmail(
                      e.target.value
                    )
                  }
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                  autoFocus
                />
              </label>


              <button
                className="button primary full"
                disabled={busy}
              >
                {busy
                  ? "Sending…"
                  : "Send reset OTP"}
              </button>

            </form>
          ) : (

            /* =================================================
               STEP 2 — OTP + NEW PASSWORD
            ================================================= */

            <form
              className="auth-form"
              onSubmit={
                resetPassword
              }
            >

              <p
                className="muted"
                style={{
                  margin: 0,
                }}
              >
                Verification code sent
                to{" "}
                <strong>
                  {resetEmail}
                </strong>
              </p>


              {/* SIX OTP BOXES */}

              <div>
                <label>
                  6-digit verification code
                </label>

                <OtpInput
                  value={resetOtp}
                  onChange={
                    setResetOtp
                  }
                  disabled={busy}
                  autoFocus
                  error={!!error}
                />

                <p
                  className="muted"
                  style={{
                    textAlign:
                      "center",
                    margin:
                      "5px 0 0",
                    fontSize: 12,
                  }}
                >
                  Enter the code from
                  your email.
                </p>
              </div>


              {/* NEW PASSWORD */}

              <label>
                New password

                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) =>
                    setNewPassword(
                      e.target.value
                    )
                  }
                  minLength={6}
                  autoComplete="new-password"
                  placeholder="At least 6 characters"
                  required
                />
              </label>


              {/* RESET BUTTON */}

              <button
                className="button primary full"
                disabled={
                  busy ||
                  resetOtp.length !== 6 ||
                  newPassword.length < 6
                }
              >
                {busy
                  ? "Resetting…"
                  : "Set new password"}
              </button>


              {/* RESEND / CHANGE EMAIL */}

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "center",
                  gap: 6,
                  alignItems:
                    "center",
                  flexWrap:
                    "wrap",
                  fontSize: 12,
                }}
              >

                <span className="muted">
                  Didn't receive it?
                </span>


                {resetCooldown > 0 ? (

                  <span className="muted">
                    Resend in{" "}
                    {resetCooldown}s
                  </span>

                ) : (

                  <button
                    type="button"
                    onClick={
                      sendResetOtp
                    }
                    disabled={busy}
                    style={{
                      border: 0,
                      background:
                        "transparent",
                      color:
                        "#22D3EE",
                      cursor:
                        busy
                          ? "not-allowed"
                          : "pointer",
                      padding: 0,
                      fontSize: 12,
                      fontWeight: 800,
                    }}
                  >
                    Resend OTP
                  </button>

                )}


                <span className="muted">
                  ·
                </span>


                <button
                  type="button"
                  onClick={() => {
                    setResetSent(
                      false
                    );

                    setResetOtp(
                      ""
                    );

                    clearMessages();
                  }}
                  style={{
                    border: 0,
                    background:
                      "transparent",
                    color:
                      "#22D3EE",
                    cursor:
                      "pointer",
                    padding: 0,
                    fontSize: 12,
                    fontWeight: 800,
                  }}
                >
                  Change email
                </button>

              </div>

            </form>
          )}


          {/* BACK TO LOGIN */}

          <button
            type="button"
            className="button ghost full"
            onClick={() =>
              switchMode(
                "password"
              )
            }
          >
            Back to sign in
          </button>

        </div>
      )}


      <p className="auth-switch">
        New to CareerBridge?{" "}
        <Link to="/register">
          Create an account
        </Link>
      </p>

    </AuthScreen>
  );
}


/* =========================================================
   SHARED AUTH SCREEN
========================================================= */

export function AuthScreen({
  title,
  text,
  children,
}) {
  return (
    <div className="auth-page">

      <div className="auth-art">

        <div className="art-brand">

          <div className="brand-mark">
            CB
          </div>

          <b>
            CareerBridge
          </b>

        </div>


        <div className="art-copy">

          <span>
            FROM WHERE YOU ARE
          </span>

          <h1>
            To where
            <br />
            <i>
              you want to be.
            </i>
          </h1>

          <p>
            Turn a resume and a
            real company job
            description into a
            focused plan for
            getting job-ready.
          </p>

        </div>


        <div className="art-flow">

          <span>
            RESUME
          </span>

          <b>→</b>

          <span>
            AI MATCH
          </span>

          <b>→</b>

          <span>
            ROADMAP
          </span>

          <b>→</b>

          <span>
            JOB READY
          </span>

        </div>

      </div>


      <div className="auth-panel">

        <div className="auth-card">

          <span className="eyebrow">
            CAREERBRIDGE AI
          </span>

          <h2>
            {title}
          </h2>

          <p>
            {text}
          </p>

          {children}

        </div>

      </div>

    </div>
  );
}