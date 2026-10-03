import { useState } from "react";
import { Link } from "react-router-dom";

export function Card({ title, subtitle, children, className = "" }) {
  return (
    <div className={`card ${className}`}>
      {title && (
        <div className="card-head">
          <h2>{title}</h2>
          {subtitle && <p>{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
}

export function Spinner() {
  return <span className="spinner" />;
}

export function Empty({ icon = "○", title, text, to, label }) {
  return (
    <div className="empty">
      <div className="empty-icon">{icon}</div>
      <strong>{title}</strong>
      <p>{text}</p>
      {to && (
        <Link className="button ghost small" to={to}>
          {label}
        </Link>
      )}
    </div>
  );
}

export function ErrorBox({ children }) {
  return children ? <div className="alert alert-error">{children}</div> : null;
}

export function SuccessBox({ children }) {
  return children ? <div className="alert alert-success">{children}</div> : null;
}

// Circular progress ring used for readiness/match scores.
export function Gauge({ value = 0, size = 150, stroke = 13, label, sublabel }) {
  const clamped = Math.max(0, Math.min(100, value));
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - clamped / 100);

  return (
    <div className="gauge" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="var(--gauge-track)"
          strokeWidth={stroke}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="url(#gaugeGrad)"
          strokeWidth={stroke}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <defs>
          <linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="var(--accent)" />
            <stop offset="100%" stopColor="var(--accent2)" />
          </linearGradient>
        </defs>
      </svg>
      <div className="gauge-center">
        <strong>{Math.round(clamped)}%</strong>
        {label && <span>{label}</span>}
        {sublabel && <em>{sublabel}</em>}
      </div>
    </div>
  );
}

// Thin horizontal progress bar. tone: "default" | "ok" | "warn" | "bad"
export function Bar({ value = 0, tone = "default" }) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className={`bar-track tone-${tone}`}>
      <div className="bar-fill" style={{ width: `${clamped}%` }} />
    </div>
  );
}

// Small rounded status label. tone: "neutral" | "ok" | "warn" | "bad"
export function Pill({ tone = "neutral", children }) {
  return <span className={`pill tone-${tone}`}>{children}</span>;
}

// A hidden-checkbox pill toggle switch (see .toggle-switch in App.css).
export function ToggleSwitch({ checked, onChange }) {
  return (
    <label className="toggle-switch">
      <input type="checkbox" checked={checked} onChange={onChange} />
      <span className="track" />
    </label>
  );
}

// Renders a skill's suggested learning links: full-course videos, official
// documentation, an AI-picked video when available, and anything the
// community has shared for that skill. onUpvote is optional.
export function ResourceLinks({ resources, onUpvote }) {
  if (!resources || !resources.length) {
    return null;
  }

  return (
    <div className="resource-links">
      {resources.map((resource, index) => (
        <div key={resource.id || index} className={`resource-chip${resource.ai_recommended ? " ai" : ""}${resource.community ? " community" : ""}`}>
          <a href={resource.url} target="_blank" rel="noopener noreferrer" className="resource-chip-link">
            <span className="resource-icon">
              {resource.type === "doc" ? "📄" : resource.community ? "🌐" : "▶"}
            </span>
            <span className="resource-text">
              <strong>{resource.title}</strong>
              <em>
                {resource.provider}
                {resource.ai_recommended ? " · AI pick" : ""}
                {resource.community ? " · community" : ""}
              </em>
            </span>
          </a>
          {resource.community && onUpvote && (
            <button className="resource-upvote" onClick={() => onUpvote(resource.id)} title="This helped me">
              ▲ {resource.upvotes || 0}
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

// A small inline form so any user can share a link for a skill — it then
// shows up for everyone else studying that same skill.
export function AddResourceForm({ skill, onSubmit }) {
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(e) {
    e.preventDefault();
    if (!title.trim() || !url.trim()) return;

    setBusy(true);
    setMessage("");
    try {
      await onSubmit({ skill, title: title.trim(), url: url.trim() });
      setTitle("");
      setUrl("");
      setOpen(false);
      setMessage("Shared — thanks for helping other learners!");
    } catch (err) {
      setMessage(err.response?.data?.error || "Couldn't share that link.");
    } finally {
      setBusy(false);
    }
  }

  if (!open) {
    return (
      <button type="button" className="add-resource-trigger" onClick={() => setOpen(true)}>
        + Share a resource you found helpful
      </button>
    );
  }

  return (
    <form className="add-resource-form" onSubmit={submit}>
      <input
        placeholder="Resource title (e.g. 'Best SQL joins explainer')"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        placeholder="https://…"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <div className="add-resource-actions">
        <button type="submit" className="button primary small" disabled={busy}>
          {busy ? "Sharing…" : "Share with everyone"}
        </button>
        <button type="button" className="button ghost small" onClick={() => setOpen(false)}>
          Cancel
        </button>
      </div>
      {message && <span className="add-resource-message">{message}</span>}
    </form>
  );
}
