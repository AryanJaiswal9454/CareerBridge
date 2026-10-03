import api from "./axios";


/*
=========================================================
GET ROADMAPS
=========================================================
*/

export const getRoadmaps = async () =>
  (
    await api.get(
      "/roadmap/"
    )
  ).data;


/*
=========================================================
GENERATE ROADMAP
=========================================================
*/

export const generateRoadmap =
  async (matchId) =>
    (
      await api.post(
        "/roadmap/generate/",
        {
          match_id: matchId,
        }
      )
    ).data;


/*
=========================================================
START LEARNING ITEM
=========================================================
*/

export const startRoadmapItem =
  async (id) =>
    (
      await api.post(
        `/roadmap/items/${id}/start/`
      )
    ).data;


/*
=========================================================
SAVE LEARNING CHECKLIST PROGRESS
=========================================================

IMPORTANT:

Django backend expects:

PATCH
/roadmap/items/<id>/progress/

{
    "completed_steps": [0, 1, 2]
}

It stores checklist indexes, NOT the topic text.
*/

export const saveLearningProgress =
  async (
    id,
    completedLearningSteps
  ) =>
    (
      await api.patch(
        `/roadmap/items/${id}/progress/`,
        {
          completed_steps:
            completedLearningSteps,
        }
      )
    ).data;


/*
=========================================================
COMPLETE LEARNING
=========================================================

The backend verifies that every checklist item
has been completed before setting:

learning_completed_at

This is what unlocks the targeted mock.
*/

export const completeLearning =
  async (id) =>
    (
      await api.post(
        `/roadmap/items/${id}/learning-complete/`
      )
    ).data;


/*
=========================================================
START TARGETED MOCK
=========================================================
*/

export const startRoadmapMock =
  async (id) =>
    (
      await api.post(
        `/roadmap/items/${id}/mock/start/`
      )
    ).data;


/*
=========================================================
OPTIONAL ROADMAP STATUS UPDATE
=========================================================
*/

export const updateRoadmapItem =
  async (
    id,
    status
  ) =>
    (
      await api.patch(
        `/roadmap/items/${id}/`,
        {
          status,
        }
      )
    ).data;