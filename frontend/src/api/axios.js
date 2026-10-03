import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000,
});


/*
=========================================================
AUTHENTICATION HELPERS
=========================================================
*/

function isPublicAuthEndpoint(url) {
  const path = String(url || "");

  // Only these authentication endpoints are public.
  // IMPORTANT: /auth/admin/* and /auth/password/change/ are protected
  // endpoints and MUST receive the JWT Authorization header.
  return (
    path.includes("/auth/login/") ||
    path.includes("/auth/signup/") ||
    path.includes("/auth/refresh/") ||
    path.includes("/auth/password/request-otp/") ||
    path.includes("/auth/password/reset-otp/")
  );
}


function clearLocalSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("username");
  localStorage.removeItem("is_staff");

  /*
   * AuthContext listens for this event and changes the
   * React authentication state.
   */
  window.dispatchEvent(
    new Event("auth-expired")
  );
}


/*
=========================================================
SINGLE REFRESH REQUEST
=========================================================

Several protected pages can load simultaneously.

For example:

Dashboard
Resume
Roadmap
Matching
Interviews

may all receive 401 at the same time.

We therefore allow only ONE refresh request to run.
The other requests wait for the same promise.
*/

let refreshPromise = null;


async function refreshAccessToken() {

  if (refreshPromise) {
    return refreshPromise;
  }

  const refreshToken =
    localStorage.getItem("refresh_token");

  if (!refreshToken) {
    throw new Error(
      "No refresh token is available."
    );
  }


  refreshPromise = axios
    .post(
      `${API_BASE_URL}/auth/refresh/`,
      {
        refresh: refreshToken,
      },
      {
        timeout: 30000,
      }
    )

    .then((response) => {

      const newAccessToken =
        response.data?.access;


      if (!newAccessToken) {

        throw new Error(
          "Refresh endpoint did not return an access token."
        );

      }


      localStorage.setItem(
        "access_token",
        newAccessToken
      );


      /*
       * If the backend rotates the refresh token,
       * keep the new refresh token too.
       */
      if (response.data?.refresh) {

        localStorage.setItem(
          "refresh_token",
          response.data.refresh
        );

      }


      return newAccessToken;

    })

    .finally(() => {

      refreshPromise = null;

    });


  return refreshPromise;
}


/*
=========================================================
REQUEST INTERCEPTOR
=========================================================
*/

api.interceptors.request.use(
  (config) => {

    const url =
      String(config.url || "");


    /*
     * NEVER attach an old JWT to:
     *
     * /auth/login/
     * /auth/refresh/
     * /auth/login/request-otp/
     * /auth/login/verify-otp/
     * /auth/signup/...
     * /auth/password/...
     */
    if (isPublicAuthEndpoint(url)) {

      if (
        config.headers?.Authorization
      ) {

        delete config.headers.Authorization;

      }

      return config;
    }


    const accessToken =
      localStorage.getItem(
        "access_token"
      );


    if (accessToken) {

      config.headers =
        config.headers || {};

      config.headers.Authorization =
        `Bearer ${accessToken}`;

    }


    return config;

  },

  (error) =>
    Promise.reject(error)
);


/*
=========================================================
RESPONSE INTERCEPTOR
=========================================================
*/

api.interceptors.response.use(

  (response) =>
    response,


  async (error) => {

    const original =
      error.config;


    const url =
      String(
        original?.url || ""
      );


    const authEndpoint =
      isPublicAuthEndpoint(url);


    /*
     * Authentication endpoints should never cause
     * automatic refresh.
     */
    if (
      error.response?.status !== 401 ||
      original?._retry ||
      authEndpoint
    ) {

      return Promise.reject(
        error
      );

    }


    original._retry = true;


    try {

      const newAccessToken =
        await refreshAccessToken();


      original.headers =
        original.headers || {};


      original.headers.Authorization =
        `Bearer ${newAccessToken}`;


      /*
       * Retry the original request once.
       */
      return api(original);

    } catch (refreshError) {

      /*
       * The refresh token itself is no longer usable.
       *
       * Do NOT keep sending:
       *
       * 401 → refresh → 500 → 401 → refresh...
       *
       * Clear the stale session and let AuthContext
       * redirect the user to login.
       */
      clearLocalSession();


      return Promise.reject(
        refreshError
      );

    }

  }

);


export default api;