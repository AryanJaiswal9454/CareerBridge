
import api from "./axios";

export const matchResumeToJob = async (resumeId, jobId) =>
  (await api.post("/matching/match/", {
    resume_id: resumeId,
    job_id: jobId,
  })).data;


export const getMatches = async () =>
  (await api.get("/matching/")).data;


export const getMatchResults = getMatches;


export const getResumeOptimization = async (
  matchId,
  forceRefresh = false
) => {
  if (forceRefresh) {
    return (
      await api.post(`/matching/${matchId}/optimize/`)
    ).data;
  }

  return (
    await api.get(`/matching/${matchId}/optimize/`)
  ).data;
};


export const getTailoredResume = async (
  matchId,
  forceRefresh = false
) => {
  if (forceRefresh) {
    return (
      await api.post(
        `/matching/${matchId}/tailored-resume/`
      )
    ).data;
  }

  return (
    await api.get(
      `/matching/${matchId}/tailored-resume/`
    )
  ).data;
};


export const getResumeTemplates = async () =>
  (await api.get("/matching/templates/")).data;


export async function downloadTailoredResume(
  matchId,
  filenameHint = "tailored_resume.docx",
  version = null,
  template = "aryan_ats"
) {
  const response = await api.get(
    `/matching/${matchId}/tailored-resume/download/`,
    {
      params: {
        ...(version ? { version } : {}),
        template,
      },
      responseType: "blob",
    }
  );

  const url = window.URL.createObjectURL(
    new Blob([response.data])
  );

  const link = document.createElement("a");

  link.href = url;
  link.download = filenameHint;

  document.body.appendChild(link);

  link.click();

  link.remove();

  window.URL.revokeObjectURL(url);
}

