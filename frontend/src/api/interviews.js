import api from "./axios";

export const getInterviews = async () =>
  (await api.get("/interviews/")).data;

export const createInterview = async (
  matchId,
  sessionType = "mixed",
  questionCount = 5,
  options = {}
) =>
  (
    await api.post("/interviews/create/", {
      match_id: matchId,
      roadmap_item_id: options.roadmapItemId || undefined,
      session_type: sessionType,
      question_count: questionCount,
      role_id: options.roleId || undefined,
      skill: options.skill || undefined,
      topic: options.topic || undefined,
      difficulty: options.difficulty || undefined,
    })
  ).data;

export const submitInterviewAnswer = async (questionId, payload) =>
  (await api.post(`/interviews/questions/${questionId}/answer/`, payload)).data;

export const getInterviewAnalysis = async (sessionId) =>
  (await api.get(`/interviews/${sessionId}/analysis/`)).data;

export const getQuestionBankCatalog = async () =>
  (await api.get("/interviews/question-bank/catalog/")).data;

export const getQuestionBankCategories = async () =>
  (await api.get("/interviews/question-bank/categories/")).data;

export const getQuestionBank = async ({
  roleId,
  skill,
  topic,
  difficulty = "medium",
  count = 12,
  questionType = "mixed",
}) =>
  (
    await api.get("/interviews/question-bank/", {
      params: {
        role_id: roleId,
        skill,
        topic,
        difficulty,
        count,
        question_type: questionType,
      },
    })
  ).data;
