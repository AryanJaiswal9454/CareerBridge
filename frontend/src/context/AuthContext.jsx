import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  loginUser,
  verifyLoginOtp,
  logoutUser,
  isAuthenticated,
  isStaffUser,
  requestSignupOtp,
  verifySignupOtp,
  resendSignupOtp,
} from "../api/auth";

const AuthContext = createContext(null);


export function AuthProvider({ children }) {
  const [user, setUser] = useState(
    localStorage.getItem("username") || ""
  );

  const [authenticated, setAuthenticated] =
    useState(isAuthenticated());

  const [isStaff, setIsStaff] =
    useState(isStaffUser());

  const [email, setEmail] = useState(
    localStorage.getItem("email") || ""
  );

  const [isSuperuser, setIsSuperuser] = useState(
    localStorage.getItem("is_superuser") === "true"
  );


  /*
   * If the API interceptor determines that the access/refresh
   * session is invalid, update React authentication state too.
   */
  useEffect(() => {
    function handleExpired() {
      setAuthenticated(false);
      setUser("");
      setIsStaff(false);
      setEmail("");
      setIsSuperuser(false);
    }

    window.addEventListener(
      "auth-expired",
      handleExpired
    );

    return () => {
      window.removeEventListener(
        "auth-expired",
        handleExpired
      );
    };
  }, []);


  /* =========================
     PASSWORD LOGIN
  ========================= */

  async function login(username, password) {
    const data = await loginUser(
      username,
      password
    );

    setUser(
      data.user?.username || username
    );

    setAuthenticated(true);

    setIsStaff(!!data.user?.is_staff);
    setEmail(data.user?.email || "");
    setIsSuperuser(!!data.user?.is_superuser);

    return data;
  }


  /* =========================
     OTP LOGIN
  ========================= */

  async function loginWithOtp(email, code) {
    const data = await verifyLoginOtp(
      email,
      code
    );

    /*
     * VERY IMPORTANT:
     *
     * Saving the JWT in localStorage alone is not enough.
     * ProtectedRoute uses React state, so we must also update
     * authenticated/user/isStaff here.
     */
    setUser(
      data.user?.username || ""
    );

    setAuthenticated(true);

    setIsStaff(!!data.user?.is_staff);
    setEmail(data.user?.email || "");
    setIsSuperuser(!!data.user?.is_superuser);

    return data;
  }


  /* =========================
     SIGNUP
  ========================= */

  async function startSignup(
    username,
    email,
    password
  ) {
    return requestSignupOtp(
      username,
      email,
      password
    );
  }


  async function completeSignup(
    email,
    code
  ) {
    const data = await verifySignupOtp(
      email,
      code
    );

    setUser(
      data.user?.username || ""
    );

    setAuthenticated(true);

    setIsStaff(!!data.user?.is_staff);
    setEmail(data.user?.email || "");
    setIsSuperuser(!!data.user?.is_superuser);

    return data;
  }


  async function resendOtp(email) {
    return resendSignupOtp(email);
  }


  /* =========================
     LOGOUT
  ========================= */

  function logout() {
    logoutUser();

    setUser("");
    setAuthenticated(false);
    setIsStaff(false);
    setEmail("");
    setIsSuperuser(false);
  }


  const value = useMemo(
    () => ({
      user,
      authenticated,
      isStaff,
      email,
      isSuperuser,

      login,
      loginWithOtp,

      startSignup,
      completeSignup,
      resendOtp,

      logout,
    }),
    [
      user,
      authenticated,
      isStaff,
      email,
      isSuperuser,
    ]
  );


  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}


export const useAuth = () =>
  useContext(AuthContext);