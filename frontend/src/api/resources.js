import api from "./axios";

export const getCommunityResources = async (skill) =>
  (await api.get("/resources/", { params: { skill } })).data;

export const addCommunityResource = async (data) =>
  (await api.post("/resources/", data)).data;

export const upvoteCommunityResource = async (id) =>
  (await api.post(`/resources/${id}/upvote/`)).data;
