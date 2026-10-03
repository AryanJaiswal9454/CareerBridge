import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Resume from "./pages/Resume";
import ResumeGenerator from "./pages/ResumeGenerator";
import JobDescription from "./pages/JobDescription";
import Matching from "./pages/Matching";
import ResumeTailoring from "./pages/ResumeTailoring";
import SkillGap from "./pages/SkillGap";
import Roadmap from "./pages/Roadmap";
import Interview from "./pages/Interview";
import JobReadiness from "./pages/JobReadiness";
import Settings from "./pages/Settings";
import AdminUsers from "./pages/AdminUsers";

// Small helper so every protected page gets the sidebar/topbar shell
// without repeating <ProtectedRoute><Layout>...</Layout></ProtectedRoute>
// on every single route below.
function Private({ children }) {
  return (
    <ProtectedRoute>
      <Layout>{children}</Layout>
    </ProtectedRoute>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          <Route path="/dashboard" element={<Private><Dashboard /></Private>} />
          <Route path="/profile" element={<Private><Profile /></Private>} />
          <Route path="/resume" element={<Private><Resume /></Private>} />
          <Route path="/generate-resume" element={<Private><ResumeGenerator /></Private>} />
          <Route path="/job-description" element={<Private><JobDescription /></Private>} />
          <Route path="/matching" element={<Private><Matching /></Private>} />
          <Route path="/resume-tailoring" element={<Private><ResumeTailoring /></Private>} />
          <Route path="/skill-gap" element={<Private><SkillGap /></Private>} />
          <Route path="/roadmap" element={<Private><Roadmap /></Private>} />
          <Route path="/interview" element={<Private><Interview /></Private>} />
          <Route path="/job-readiness" element={<Private><JobReadiness /></Private>} />
          <Route path="/settings" element={<Private><Settings /></Private>} />
          <Route path="/admin/users" element={<Private><AdminUsers /></Private>} />

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
