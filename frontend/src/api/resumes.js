
import api from "./axios";

export const getResumes = async () =>
  (await api.get("/resumes/")).data;

export const uploadResume = async (title, file) => {
  const formData = new FormData();

  if (title?.trim()) {
    formData.append("title", title.trim());
  }

  formData.append("file", file);

  return (await api.post("/resumes/", formData)).data;
};

export const analyzeResume = async (id) =>
  (await api.post(`/resumes/${id}/analyze/`)).data;

export const getResumeATSScore = async (id) =>
  (await api.post(`/resumes/${id}/ats-score/`)).data;

// Peeks at a cached ATS report without regenerating it.
// Returns null if an ATS report has not been generated yet.
export const peekResumeATSScore = async (id) => {
  try {
    return (await api.get(`/resumes/${id}/ats-score/`)).data;
  } catch {
    return null;
  }
};

// Generate a brand-new resume from user-provided information
// and the selected resume template.
export const generateNewResume = async (payload) =>
  (await api.post("/resumes/generate/", payload)).data;
