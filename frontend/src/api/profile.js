
import api from "./axios";

export const getProfile = async () =>
  (await api.get("/profiles/")).data;

export const updateProfile = async (data) =>
  (await api.put("/profiles/", data)).data;

export const getSkills = async () =>
  (await api.get("/profiles/skills/")).data;

export const addSkill = async (data) =>
  (await api.post("/profiles/skills/", data)).data;

export const deleteSkill = async (skillId) =>
  (
    await api.delete(
      `/profiles/skills/${skillId}/`
    )
  ).data;

export const changePassword = async (
  currentPassword,
  newPassword
) =>
  (
    await api.post(
      "/auth/password/change/",
      {
        current_password:
          currentPassword,
        new_password:
          newPassword,
      }
    )
  ).data;

