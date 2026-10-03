import api from "./axios";

export const getJobDescriptions = async () =>
  (await api.get("/careers/")).data;

export const createJobDescription = async (data) =>
  (await api.post("/careers/", data)).data;

export const uploadJobDescription = async (formData) =>
  (await api.post("/careers/", formData)).data;

export const analyzeJobDescription = async (id) =>
  (await api.post(`/careers/${id}/analyze/`)).data;
