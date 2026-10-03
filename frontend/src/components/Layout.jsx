import { NavLink, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// [routePath, icon, label] — one row per sidebar entry.
const NAV_ITEMS = [
  ["dashboard", "⌂", "Dashboard"],
  ["profile", "◉", "My Profile"],
  ["resume", "▤", "Resume Analyzer"],
  ["generate-resume", "✦", "Generate New Resume"],
  ["job-description", "▣", "Job Description"],
  ["matching", "⇄", "Job Matching"],
  ["resume-tailoring", "✦", "Job-Specific Resume"],
  ["skill-gap", "△", "Skill Gap"],
  ["roadmap", "◎", "Career Roadmap"],
  ["interview", "◌", "Interview Coach"],
  ["job-readiness", "✓", "Job Readiness"],
  ["settings", "⚙", "Settings"],
];

export default function Layout({ children }) {
  const { user, isStaff, logout } = useAuth();
  const location = useLocation();
  const initial = (user || "U").charAt(0).toUpperCase();

  const navItems = isStaff ? [...NAV_ITEMS, ["admin/users", "👑", "Admin · Users"]] : NAV_ITEMS;
  const currentPage = navItems.find(([path]) => `/${path}` === location.pathname);
  const pageTitle = currentPage?.[2] || "Career Dashboard";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">CB</div>
          <div>
            <b>CareerBridge</b>
            <span>AI CAREER COMPANION</span>
          </div>
        </div>

        <div className="journey">
          <span>YOUR JOURNEY</span>
          <b>STUDENT → JOB READY</b>
        </div>

        <nav>
          {navItems.map(([path, icon, label]) => (
            <NavLink
              key={path}
              to={`/${path}`}
              className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
            >
              <i>{icon}</i>
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="side-bottom">
          <div className="mini-user">
            <div className="avatar">{initial}</div>
            <div>
              <b>{user || "Student"}</b>
              <span>CareerBridge member</span>
            </div>
          </div>
          <button className="logout" onClick={logout}>
            ↪ Sign out
          </button>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <span className="top-kicker">CAREERBRIDGE AI</span>
            <strong>{pageTitle}</strong>
          </div>
          <div className="top-right">
            <span className="status-dot" /> Workspace active
            <div className="top-avatar">{initial}</div>
          </div>
        </header>

        <div className="content">{children}</div>
      </main>
    </div>
  );
}