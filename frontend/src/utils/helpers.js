export function toArray(value, keys = []) {
  if (Array.isArray(value)) return value;
  for (const key of keys) {
    if (Array.isArray(value?.[key])) return value[key];
  }
  return [];
}

export function errorMessage(error, fallback = "Something went wrong. Please try again.") {
  const data = error?.response?.data;
  if (typeof data === "string") return data;
  if (data?.error) return data.error;
  if (data?.detail) return data.detail;
  if (data?.details) return data.details;
  if (data && typeof data === "object") {
    const first = Object.values(data).flat?.()[0];
    if (first) return String(first);
  }
  if (!error?.response) return "Unable to connect to the CareerBridge server.";
  return fallback;
}

export function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleDateString();
}

export function getInitials(name = "Student") {
  return name.trim().split(/\s+/).slice(0, 2).map((x) => x[0]).join("").toUpperCase() || "S";
}
