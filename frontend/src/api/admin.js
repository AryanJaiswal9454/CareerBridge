import api from "./axios";

export const getAdminUsers = async () =>
  (await api.get("/auth/admin/users/")).data;

export const toggleUserActive = async (userId) =>
  (await api.post(`/auth/admin/users/${userId}/toggle-active/`)).data;
