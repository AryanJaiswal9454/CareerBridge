import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getAdminUsers, toggleUserActive } from "../api/admin";
import { Page } from "./Dashboard";
import { Card, ErrorBox, Spinner, Pill } from "../components/Ui";

export default function AdminUsers() {
  const { isStaff } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyId, setBusyId] = useState(null);

  function load() {
    setLoading(true);
    return getAdminUsers()
      .then((result) => setUsers(result.users || []))
      .catch((err) => setError(err.response?.data?.detail || "Unable to load users."))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    if (isStaff) load();
  }, [isStaff]);

  async function toggle(userId) {
    setBusyId(userId);
    setError("");
    try {
      const result = await toggleUserActive(userId);
      setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, is_active: result.is_active } : u)));
    } catch (err) {
      setError(err.response?.data?.error || "Couldn't update that user.");
    } finally {
      setBusyId(null);
    }
  }

  if (!isStaff) {
    return (
      <Page title="Admin" subtitle="Staff access only.">
        <Card>
          <p className="muted">
            You don't have admin access. Django's own admin panel is also available at{" "}
            <code>/admin</code> for anyone with staff/superuser status.
          </p>
        </Card>
      </Page>
    );
  }

  return (
    <Page title="All Users" subtitle="Every account registered on CareerBridge AI, with their activity so far.">
      <ErrorBox>{error}</ErrorBox>

      {loading ? (
        <div className="loading"><Spinner /></div>
      ) : (
        <Card>
          <div className="admin-table">
            <div className="admin-table-head">
              <span>User</span>
              <span>Joined</span>
              <span>Resumes</span>
              <span>JDs</span>
              <span>Matches</span>
              <span>Interviews</span>
              <span>Status</span>
              <span></span>
            </div>
            {users.map((user) => (
              <div className="admin-table-row" key={user.id}>
                <div>
                  <strong>{user.username}</strong>
                  <span>{user.email}</span>
                </div>
                <span>{new Date(user.date_joined).toLocaleDateString()}</span>
                <span>{user.resume_count}</span>
                <span>{user.job_count}</span>
                <span>{user.match_count}</span>
                <span>{user.interview_count}</span>
                <span>
                  {user.is_superuser && <Pill tone="ok">Superuser</Pill>}
                  {!user.is_superuser && user.is_staff && <Pill tone="ok">Staff</Pill>}
                  {!user.is_active && <Pill tone="bad">Suspended</Pill>}
                  {user.is_active && !user.is_staff && <Pill tone="neutral">Active</Pill>}
                </span>
                {!user.is_superuser && !user.is_staff && (
                  <button
                    className="button ghost small"
                    disabled={busyId === user.id}
                    onClick={() => toggle(user.id)}
                  >
                    {busyId === user.id ? <Spinner /> : user.is_active ? "Suspend" : "Reinstate"}
                  </button>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}
    </Page>
  );
}
