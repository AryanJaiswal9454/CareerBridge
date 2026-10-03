import { useEffect, useState } from "react";
import {
  Link,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import { AuthScreen } from "./Login";

import {
  ErrorBox,
  SuccessBox,
  Spinner,
} from "../components/Ui";

import OtpInput from "../components/OtpInput";


const OTP_COOLDOWN_SECONDS = 30;


/* =========================================================
   SIGNUP OTP COOLDOWN
========================================================= */

function getCooldownKey(email) {
  return `careerbridge_signup_otp_cooldown_${email
    .trim()
    .toLowerCase()}`;
}


function getStoredCooldown(email) {
  if (!email?.trim()) {
    return 0;
  }

  const key =
    getCooldownKey(email);

  const expiresAt = Number(
    sessionStorage.getItem(
      key
    ) || 0
  );

  const remaining = Math.ceil(
    (expiresAt - Date.now()) /
      1000
  );

  if (remaining <= 0) {
    sessionStorage.removeItem(
      key
    );

    return 0;
  }

  return remaining;
}


function saveCooldown(
  email,
  seconds = OTP_COOLDOWN_SECONDS
) {
  sessionStorage.setItem(
    getCooldownKey(email),
    String(
      Date.now() +
        seconds * 1000
    )
  );
}


/* =========================================================
   REGISTER
========================================================= */

export default function Register() {
  const {
    startSignup,
    completeSignup,
    resendOtp,
  } = useAuth();

  const navigate =
    useNavigate();


  /*
   * details = signup form
   * otp     = email verification
   */

  const [step, setStep] =
    useState("details");


  const [form, setForm] =
    useState({
      username: "",
      email: "",
      password: "",
    });


  const [code, setCode] =
    useState("");


  const [devOtp, setDevOtp] =
    useState("");


  const [error, setError] =
    useState("");

  const [notice, setNotice] =
    useState("");

  const [busy, setBusy] =
    useState(false);

  const [cooldown, setCooldown] =
    useState(0);


  /* =========================================================
     RESEND TIMER
  ========================================================= */

  useEffect(() => {
    if (
      step !== "otp" ||
      !form.email
    ) {
      setCooldown(0);
      return undefined;
    }


    setCooldown(
      getStoredCooldown(
        form.email
      )
    );


    const timer =
      window.setInterval(() => {
        setCooldown(
          getStoredCooldown(
            form.email
          )
        );
      }, 1000);


    return () =>
      window.clearInterval(
        timer
      );
  }, [
    step,
    form.email,
  ]);


  /* =========================================================
     FORM UPDATE
  ========================================================= */

  function updateField(
    key,
    value
  ) {
    setForm((current) => ({
      ...current,
      [key]: value,
    }));
  }


  /* =========================================================
     STEP 1 — SEND SIGNUP OTP
  ========================================================= */

  async function submitDetails(
    event
  ) {
    event.preventDefault();

    setBusy(true);

    setError("");
    setNotice("");


    try {
      const result =
        await startSignup(
          form.username.trim(),
          form.email.trim(),
          form.password
        );


      /*
       * Start resend cooldown only
       * after successful sending.
       */

      saveCooldown(
        form.email
      );

      setCooldown(
        OTP_COOLDOWN_SECONDS
      );


      setNotice(
        result.message ||
        "A verification code has been sent to your email."
      );


      /*
       * Development OTP support
       * remains exactly as before.
       */

      setDevOtp(
        result.dev_otp || ""
      );


      setCode("");

      setStep("otp");

    } catch (err) {

      setError(
        err.response?.data
          ?.error ||
        "Signup failed. Please try again."
      );

    } finally {

      setBusy(false);

    }
  }


  /* =========================================================
     STEP 2 — VERIFY SIGNUP OTP
  ========================================================= */

  async function submitCode(
    event
  ) {
    event.preventDefault();

    setError("");
    setNotice("");


    if (code.length !== 6) {
      setError(
        "Enter the complete 6-digit verification code."
      );

      return;
    }


    setBusy(true);


    try {

      await completeSignup(
        form.email,
        code
      );

      navigate(
        "/dashboard"
      );

    } catch (err) {

      setError(
        err.response?.data
          ?.error ||
        "Incorrect or expired code."
      );

    } finally {

      setBusy(false);

    }
  }


  /* =========================================================
     RESEND SIGNUP OTP
  ========================================================= */

  async function resend() {

    if (busy) {
      return;
    }


    /*
     * Frontend protection against
     * repeated email requests.
     */

    const remaining =
      getStoredCooldown(
        form.email
      );


    if (remaining > 0) {

      setCooldown(
        remaining
      );

      return;
    }


    setBusy(true);

    setError("");
    setNotice("");


    try {

      const result =
        await resendOtp(
          form.email
        );


      saveCooldown(
        form.email
      );

      setCooldown(
        OTP_COOLDOWN_SECONDS
      );


      /*
       * Clear old OTP boxes because
       * backend generated a new OTP.
       */

      setCode("");


      setNotice(
        result.message ||
        "A new verification code has been sent."
      );


      setDevOtp(
        result.dev_otp || ""
      );

    } catch (err) {

      const serverMessage =
        err.response?.data
          ?.error ||
        "Couldn't resend the code.";


      /*
       * Supports backend rate
       * limiting if enabled.
       */

      if (
        err.response?.status ===
        429
      ) {

        const retryAfter =
          Number(
            err.response?.data
              ?.retry_after || 30
          );


        saveCooldown(
          form.email,
          retryAfter
        );


        setCooldown(
          retryAfter
        );
      }


      setError(
        serverMessage
      );

    } finally {

      setBusy(false);

    }
  }


  /* =========================================================
     CHANGE EMAIL
  ========================================================= */

  function changeEmail() {

    setStep("details");

    setCode("");

    setDevOtp("");

    setError("");

    setNotice("");

    setCooldown(0);
  }


  /* =========================================================
     OTP SCREEN
  ========================================================= */

  if (step === "otp") {

    return (
      <AuthScreen
        title="Check your email"
        text={`We've sent a 6-digit verification code to ${form.email}.`}
      >

        <form
          className="auth-form"
          onSubmit={
            submitCode
          }
        >

          <ErrorBox>
            {error}
          </ErrorBox>


          <SuccessBox>
            {notice}
          </SuccessBox>


          {/* DEVELOPMENT OTP */}

          {devOtp && (
            <div className="alert alert-success">

              Dev mode
              (no email service
              configured yet):
              your code is{" "}

              <strong>
                {devOtp}
              </strong>

            </div>
          )}


          {/* SIX OTP BOXES */}

          <div>

            <label>
              6-digit verification code
            </label>


            <OtpInput
              value={code}
              onChange={setCode}
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


          {/* VERIFY */}

          <button
            className="button primary full"
            disabled={
              busy ||
              code.length !== 6
            }
          >

            {busy ? (
              <Spinner />
            ) : (
              "Verify & create account"
            )}

          </button>


          {/* RESEND */}

          <div
            style={{
              display: "flex",
              justifyContent:
                "center",
              alignItems:
                "center",
              gap: 6,
              flexWrap:
                "wrap",
              fontSize: 12,
            }}
          >

            <span className="muted">
              Didn't get it?
            </span>


            {cooldown > 0 ? (

              <span className="muted">
                Resend in{" "}
                {cooldown}s
              </span>

            ) : (

              <button
                type="button"
                onClick={
                  resend
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
                Resend code
              </button>

            )}


            <span className="muted">
              ·
            </span>


            <button
              type="button"
              onClick={
                changeEmail
              }
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

      </AuthScreen>
    );
  }


  /* =========================================================
     SIGNUP DETAILS
  ========================================================= */

  return (
    <AuthScreen
      title="Create your account"
      text="Build your career profile once, then let CareerBridge connect the pieces."
    >

      <form
        className="auth-form"
        onSubmit={
          submitDetails
        }
      >

        <ErrorBox>
          {error}
        </ErrorBox>


        {/* USERNAME */}

        <label>

          Username

          <input
            value={
              form.username
            }
            onChange={(e) =>
              updateField(
                "username",
                e.target.value
              )
            }
            autoComplete="username"
            required
          />

        </label>


        {/* EMAIL */}

        <label>

          Email

          <input
            type="email"
            value={
              form.email
            }
            onChange={(e) =>
              updateField(
                "email",
                e.target.value
              )
            }
            autoComplete="email"
            required
          />

        </label>


        {/* PASSWORD */}

        <label>

          Password

          <input
            type="password"
            value={
              form.password
            }
            onChange={(e) =>
              updateField(
                "password",
                e.target.value
              )
            }
            autoComplete="new-password"
            required
            minLength="6"
          />

        </label>


        {/* SEND OTP */}

        <button
          className="button primary full"
          disabled={
            busy ||
            !form.username.trim() ||
            !form.email.trim() ||
            form.password.length < 6
          }
        >

          {busy ? (
            <Spinner />
          ) : (
            "Send verification code"
          )}

        </button>


        <p className="auth-switch">

          Already registered?{" "}

          <Link to="/login">
            Sign in
          </Link>

        </p>

      </form>

    </AuthScreen>
  );
}