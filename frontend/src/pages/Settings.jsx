import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { changePassword } from "../api/auth";
import { Page } from "./Dashboard";
import { Card, ErrorBox, SuccessBox, ToggleSwitch, Spinner } from "../components/Ui";

export default function Settings() {
  const { user, email, isStaff, isSuperuser, logout } = useAuth();
  const [ok, setOk] = useState("");
  const [error, setError] = useState("");
  const [compact, setCompact] = useState(localStorage.getItem("careerbridge_compact") === "true");
  const [saving, setSaving] = useState(false);
  const [passwords, setPasswords] = useState({ current: "", next: "", confirm: "" });

  function savePreference() {
    localStorage.setItem("careerbridge_compact", compact);
    setOk("Workspace preference saved.");
    setError("");
  }

  async function submitPassword(event) {
    event.preventDefault();
    setError("");
    setOk("");
    if (passwords.next.length < 6) {
      setError("New password must be at least 6 characters.");
      return;
    }
    if (passwords.next !== passwords.confirm) {
      setError("New password and confirmation do not match.");
      return;
    }
    setSaving(true);
    try {
      const result = await changePassword(passwords.current, passwords.next, passwords.confirm);
      setOk(result.message || "Password changed successfully. Please sign in again.");
      setPasswords({ current: "", next: "", confirm: "" });
    } catch (err) {
      setError(err.response?.data?.error || "Unable to change password.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Page title="Settings" subtitle="Manage your CareerBridge account, security and workspace preferences.">
      <ErrorBox>{error}</ErrorBox>
      <SuccessBox>{ok}</SuccessBox>

      <div className="two-column">
        <Card title="Account" subtitle="Your authenticated CareerBridge account.">
          <div className="settings-profile">
            <div className="avatar large">{(user || "U").charAt(0).toUpperCase()}</div>
            <div>
              <strong>{user || "Student"}</strong>
              <span>{email || "No email available"}</span>
              <span>{isSuperuser ? "Superuser" : isStaff ? "Staff account" : "Student account"}</span>
            </div>
          </div>
          <button className="button ghost" onClick={logout}>Sign out</button>
        </Card>

        <Card title="Workspace" subtitle="Presentation preferences for this CareerBridge workspace.">
          <label className="toggle">
            <ToggleSwitch checked={compact} onChange={(e) => setCompact(e.target.checked)} />
            <span>Compact information density</span>
          </label>
          <button className="button primary" onClick={savePreference}>Save preference</button>
        </Card>
      </div>

      <Card className="section-card" title="Change password" subtitle="Use your current password to create a new password. Your existing resume, JD, match and roadmap data remain untouched.">
        <form className="form-grid" onSubmit={submitPassword}>
          <label>Current password<input type="password" value={passwords.current} onChange={(e) => setPasswords({ ...passwords, current: e.target.value })} autoComplete="current-password" required /></label>
          <label>New password<input type="password" value={passwords.next} onChange={(e) => setPasswords({ ...passwords, next: e.target.value })} minLength={6} autoComplete="new-password" required /></label>
          <label>Confirm new password<input type="password" value={passwords.confirm} onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })} minLength={6} autoComplete="new-password" required /></label>
          <div style={{ alignSelf: "end" }}>
            <button className="button primary" disabled={saving}>{saving ? <><Spinner /> Saving…</> : "Change password"}</button>
          </div>
        </form>
      </Card>

      <Card className="section-card" title="About CareerBridge AI">
        <p className="muted">CareerBridge connects profile evidence, resume analysis, an exact company job description, matching, skill gaps, a career roadmap, interview practice and a final readiness signal.</p>
      </Card>
    </Page>
  );
}
