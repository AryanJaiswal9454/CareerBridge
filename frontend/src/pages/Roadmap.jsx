import {
  useEffect,
  useMemo,
  useState,
} from "react";

import { useNavigate } from "react-router-dom";

import {
  getRoadmaps,
  generateRoadmap,
  startRoadmapItem,
  saveLearningProgress,
  completeLearning,
  startRoadmapMock,
} from "../api/roadmap";

import { getMatches } from "../api/matching";

import {
  getCommunityResources,
  addCommunityResource,
  upvoteCommunityResource,
} from "../api/resources";

import { Page } from "./Dashboard";

import {
  Card,
  Empty,
  ErrorBox,
  Spinner,
  Bar,
  ResourceLinks,
  AddResourceForm,
} from "../components/Ui";


/*
=========================================================
CHECKLIST HELPERS
=========================================================

The backend stores completed learning steps as indexes:

[
  0,
  1,
  2
]

Older records may contain the actual topic text.

This helper supports both formats.
*/

function normalizeCompletedSteps(
  values,
  checklist
) {

  const result =
    new Set();


  const source =
    Array.isArray(values)
      ? values
      : [];


  source.forEach(
    (value) => {

      /*
       * Current format:
       *
       * 0
       * 1
       * 2
       */
      if (
        Number.isInteger(value)
      ) {

        if (
          value >= 0 &&
          value < checklist.length
        ) {

          result.add(
            value
          );

        }

        return;
      }


      /*
       * Numeric strings such as:
       *
       * "0"
       * "1"
       */
      const numeric =
        Number(value);


      if (
        Number.isInteger(
          numeric
        ) &&
        String(value).trim() !== "" &&
        numeric >= 0 &&
        numeric < checklist.length
      ) {

        result.add(
          numeric
        );

        return;
      }


      /*
       * Legacy format:
       *
       * "Python functions"
       *
       * Convert the topic text into its
       * checklist index.
       */
      const index =
        checklist.findIndex(
          (topic) =>
            String(topic) ===
            String(value)
        );


      if (
        index >= 0
      ) {

        result.add(
          index
        );

      }

    }
  );


  return result;
}


/*
=========================================================
PROGRESS CALCULATOR
=========================================================
*/

function calculateProgress(
  checklist,
  completed
) {

  if (
    !checklist.length
  ) {

    return 0;

  }


  const normalized =
    normalizeCompletedSteps(
      Array.from(
        completed
      ),
      checklist
    );


  return Math.round(
    (
      normalized.size /
      checklist.length
    ) * 100
  );
}


/*
=========================================================
ROADMAP PAGE
=========================================================
*/

export default function Roadmap() {

  const navigate =
    useNavigate();


  const [
    roadmaps,
    setRoadmaps,
  ] = useState([]);


  const [
    matches,
    setMatches,
  ] = useState([]);


  const [
    busy,
    setBusy,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState("");


  const [
    openItemId,
    setOpenItemId,
  ] = useState(null);


  /*
   * Load roadmap and matching data.
   */
  async function load() {

    const [
      roadmapsResult,
      matchesResult,
    ] = await Promise.all([
      getRoadmaps(),
      getMatches(),
    ]);


    setRoadmaps(
      roadmapsResult.roadmaps ||
      []
    );


    setMatches(
      matchesResult ||
      []
    );

  }


  /*
   * Initial load.
   */
  useEffect(
    () => {

      load().catch(
        (err) => {

          setError(
            err.response?.data?.error ||
            "Unable to load your career roadmap."
          );

        }
      );

    },
    []
  );


  const roadmap =
    roadmaps[0];


  const items =
    roadmap?.items ||
    [];


  const doneCount =
    items.filter(
      (item) =>
        item.status ===
        "completed"
    ).length;


  const progress =
    items.length
      ? Math.round(
          (
            doneCount /
            items.length
          ) * 100
        )
      : 0;


  const activeItem =
    items.find(
      (item) =>
        item.status !==
        "completed"
    ) ||
    null;


  /*
   * Generate roadmap from latest match.
   */
  async function generate() {

    if (
      !matches.length
    ) {

      setError(
        "Create a match before generating a roadmap."
      );

      return;
    }


    const matchId =
      matches[0]?.match_id ||
      matches[0]?.id;


    if (!matchId) {

      setError(
        "No valid match was found."
      );

      return;
    }


    setBusy(true);
    setError("");


    try {

      await generateRoadmap(
        matchId
      );


      await load();

    } catch (err) {

      setError(
        err.response?.data?.details ||
        err.response?.data?.error ||
        "Roadmap generation failed."
      );

    } finally {

      setBusy(false);

    }

  }


  /*
   * Start learning.
   */
  async function handleStartLearning(
    item
  ) {

    setBusy(true);
    setError("");


    try {

      await startRoadmapItem(
        item.id
      );


      setOpenItemId(
        item.id
      );


      await load();

    } catch (err) {

      setError(
        err.response?.data?.error ||
        "Unable to start learning."
      );

    } finally {

      setBusy(false);

    }

  }


  /*
   * Checklist change.
   *
   * IMPORTANT:
   *
   * The topic is converted to an INDEX.
   *
   * Example:
   *
   * checklist:
   *
   * [
   *   "Python basics",
   *   "Functions",
   *   "Django"
   * ]
   *
   * "Django" becomes:
   *
   * 2
   */
  async function handleChecklistChange(
    item,
    topic,
    checked
  ) {

    const checklist =
      item.learning_checklist ||
      item.learning_topics ||
      [];


    const topicIndex =
      checklist.findIndex(
        (value) =>
          String(value) ===
          String(topic)
      );


    if (
      topicIndex < 0
    ) {

      setError(
        "Unable to identify this learning topic."
      );

      return;
    }


    const current =
      normalizeCompletedSteps(
        item.completed_learning_steps,
        checklist
      );


    if (
      checked
    ) {

      current.add(
        topicIndex
      );

    } else {

      current.delete(
        topicIndex
      );

    }


    setError("");


    try {

      await saveLearningProgress(
        item.id,
        Array.from(
          current
        ).sort(
          (a, b) =>
            a - b
        )
      );


      /*
       * Reload from Django so the UI always
       * reflects the actual database state.
       */
      await load();

    } catch (err) {

      setError(
        err.response?.data?.error ||
        "Unable to save learning progress."
      );

    }

  }


  /*
   * Complete learning.
   *
   * Backend performs the final validation.
   */
  async function handleCompleteLearning(
    item
  ) {

    setBusy(true);
    setError("");


    try {

      /*
       * Refresh current data first.
       */
      await load();


      await completeLearning(
        item.id
      );


      /*
       * Get the newly unlocked state.
       */
      await load();


      setOpenItemId(
        item.id
      );

    } catch (err) {

      const missing =
        err.response?.data?.missing_topics ||
        [];


      setError(
        missing.length
          ? (
              `Complete these topics first: ${
                missing.join(
                  ", "
                )
              }`
            )
          : (
              err.response?.data?.error ||
              "Unable to complete learning."
            )
      );

    } finally {

      setBusy(false);

    }

  }


  /*
   * Start targeted mock.
   *
   * Before calling the backend, fetch the latest roadmap
   * state so stale React state cannot incorrectly unlock
   * the mock.
   */
  async function handleStartMock(
    item
  ) {

    setBusy(true);
    setError("");


    try {

      const latest =
        await getRoadmaps();


      const latestRoadmap =
        (latest.roadmaps || [])
          .find(
            (value) =>
              value.id ===
              roadmap?.id
          );


      const latestItem =
        latestRoadmap?.items?.find(
          (value) =>
            value.id ===
            item.id
        );


      /*
       * The backend is the source of truth.
       */
      if (
        !latestItem?.learning_completed_at
      ) {

        throw new Error(
          "Complete every learning checklist topic first."
        );

      }


      const result =
        await startRoadmapMock(
          item.id
        );


      const sessionId =
        result?.session?.id;


      if (
        !sessionId
      ) {

        throw new Error(
          "The targeted mock session was not created."
        );

      }


      navigate(
        `/interview?session_id=${sessionId}`
      );

    } catch (err) {

      setError(
        err.response?.data?.details ||
        err.response?.data?.error ||
        err.message ||
        "Unable to start the targeted mock interview."
      );

    } finally {

      setBusy(false);

    }

  }


  /*
=========================================================
RENDER
=========================================================
*/

  return (

    <Page
      title="Personalized Career Roadmap"
      subtitle={
        roadmap
          ? roadmap.title
          : "A practical path from your current gaps to the target role."
      }
    >

      <ErrorBox>
        {error}
      </ErrorBox>


      {!roadmap ? (

        <Card>

          <Empty
            icon="◎"
            title="Your roadmap is waiting"
            text="Run a match first. CareerBridge will convert the exact job requirements and your skill gaps into a topic-by-topic learning journey."
            to="/matching"
            label="Run a match"
          />


          {matches.length > 0 && (

            <button
              className="button primary"
              style={{
                marginTop: 14,
              }}
              disabled={busy}
              onClick={
                generate
              }
            >

              {busy ? (
                <Spinner />
              ) : (
                "Generate roadmap from latest match"
              )}

            </button>

          )}

        </Card>

      ) : (

        <>

          <div
            className="roadmap-head"
          >

            <div>

              <span>
                ROADMAP PROGRESS
              </span>


              <h2>
                {progress}%
                {" "}
                complete
              </h2>


              <p>
                {roadmap.summary}
              </p>

            </div>


            <div className="days">

              <strong>
                {roadmap.total_days}
              </strong>

              <span>
                days
              </span>

            </div>

          </div>


          <Bar
            value={progress}
          />


          {activeItem && (

            <div
              className="ai-recommend-card"
              style={{
                margin:
                  "18px 0",
              }}
            >

              <div
                className="ai-badge"
              >
                AI
              </div>


              <h4>
                NEXT LEARNING PRIORITY
              </h4>


              <p>

                Focus next on{" "}

                <strong>
                  {activeItem.skill}
                </strong>

                {" "}—{" "}

                {activeItem.reason}

              </p>

            </div>

          )}


          {items.length > 0 && (

            <div
              style={{
                margin:
                  "0 0 20px",
                padding:
                  "14px 16px",
                border:
                  "1px solid rgba(44,218,239,.22)",
                borderRadius: 14,
                background:
                  "rgba(7,27,42,.72)",
              }}
            >

              <strong>
                How CareerBridge works
              </strong>


              <div
                style={{
                  marginTop: 8,
                  color: "#9db0c8",
                  fontSize: 14,
                  lineHeight: 1.6,
                }}
              >

                Learn topic by topic →
                complete the checklist →
                unlock the targeted mock →
                pass the mock → complete the
                skill slab → move to the next
                priority.

              </div>

            </div>

          )}


          <div
            className="flow-grid"
            style={{
              marginTop: 6,
            }}
          >

            {items.map(
              (
                item,
                index
              ) => (

                <RoadmapNode
                  key={item.id}
                  item={item}
                  index={index}
                  isActive={
                    item.id ===
                    activeItem?.id
                  }
                  isOpen={
                    openItemId ===
                    item.id
                  }
                  busy={busy}

                  onToggleOpen={() =>
                    setOpenItemId(
                      openItemId ===
                      item.id
                        ? null
                        : item.id
                    )
                  }

                  onStartLearning={() =>
                    handleStartLearning(
                      item
                    )
                  }

                  onChecklistChange={(
                    topic,
                    checked
                  ) =>
                    handleChecklistChange(
                      item,
                      topic,
                      checked
                    )
                  }

                  onCompleteLearning={() =>
                    handleCompleteLearning(
                      item
                    )
                  }

                  onStartMock={() =>
                    handleStartMock(
                      item
                    )
                  }
                />

              )
            )}

          </div>

        </>

      )}

    </Page>

  );

}


/*
=========================================================
ROADMAP NODE
=========================================================
*/

function RoadmapNode({
  item,
  index,
  isActive,
  isOpen,
  busy,
  onToggleOpen,
  onStartLearning,
  onChecklistChange,
  onCompleteLearning,
  onStartMock,
}) {

  const checklist =
    item.learning_checklist ||
    item.learning_topics ||
    [];


  /*
   * THIS IS THE IMPORTANT CRASH FIX.
   *
   * normalizeCompletedSteps is defined globally above,
   * so RoadmapNode can safely use it.
   */
  const completed =
    normalizeCompletedSteps(
      item.completed_learning_steps,
      checklist
    );


  const learningProgress =
    item.learning_progress ??
    calculateProgress(
      checklist,
      completed
    );


  const learningDone =
    Boolean(
      item.learning_completed_at
    );


  const mockDone =
    Boolean(
      item.mock_completed
    );


  const statusClass =
    mockDone
      ? "done"
      : isActive
      ? "active"
      : "";


  const slabProgress =
    mockDone
      ? 100
      : learningProgress;


  const content =
    item.learning_content ||
    {};


  const objectives =
    content.learning_objectives ||
    [];


  const concepts =
    content.concepts ||
    [];


  const examples =
    content.examples ||
    [];


  const practice =
    content.practice_tasks ||
    item.practice_tasks ||
    [];


  return (

    <div
      className={`flow-node ${statusClass}`}
    >

      <div
        className="flow-node-head"
      >

        <div
          className="flow-node-icon"
        >

          {mockDone
            ? "✓"
            : index + 1}

        </div>


        <strong
          style={{
            flex: 1,
            textTransform:
              "capitalize",
          }}
        >

          {item.skill}

        </strong>


        {!learningDone && (

          <button
            className="button primary small"
            disabled={busy}
            onClick={
              onStartLearning
            }
          >

            {item.status ===
            "in_progress"
              ? "Continue Learning"
              : "Start Learning"}

          </button>

        )}


        {learningDone &&
          !mockDone && (

            <button
              className="button primary small"
              disabled={busy}
              onClick={
                onStartMock
              }
            >

              Start Mock

            </button>

          )}


        {mockDone && (

          <button
            className="button ghost small"
            disabled
          >

            Completed

          </button>

        )}

      </div>


      <p>
        {item.reason}
      </p>


      <Bar
        value={
          slabProgress
        }
        tone={
          mockDone
            ? "ok"
            : "default"
        }
      />


      <small>

        {item.estimated_days}
        {" "}days ·{" "}

        {item.category}
        {" "}·{" "}

        {item.priority}
        {" "}priority ·{" "}

        {learningProgress}
        % learning


        {mockDone
          ? " · mock passed"
          : learningDone
          ? " · mock unlocked"
          : ""}

      </small>


      <div
        style={{
          marginTop: 12,
          display: "flex",
          gap: 8,
          flexWrap: "wrap",
        }}
      >

        <button
          className="button ghost small"
          onClick={
            onToggleOpen
          }
        >

          {isOpen
            ? "Hide learning module"
            : "View AI learning module"}

        </button>

      </div>


      {isOpen && (

        <div
          style={{
            marginTop: 16,
          }}
        >

          <LearningChecklist
            checklist={
              checklist
            }
            completed={
              completed
            }
            disabled={
              mockDone
            }
            onChange={
              onChecklistChange
            }
          />


          {!learningDone &&
            checklist.length > 0 && (

              <button
                className="button primary small"
                style={{
                  marginTop: 14,
                }}
                disabled={
                  busy ||
                  learningProgress <
                    100
                }
                onClick={
                  onCompleteLearning
                }
              >

                {learningProgress >=
                100
                  ? "Complete Learning & Unlock Mock"
                  : `Complete all topics (${learningProgress}%)`}

              </button>

            )}


          {learningDone &&
            !mockDone && (

              <div
                style={{
                  marginTop: 14,
                  padding:
                    "12px 14px",
                  borderRadius: 12,
                  border:
                    "1px solid rgba(44,218,239,.25)",
                  background:
                    "rgba(8,35,50,.65)",
                }}
              >

                <strong>
                  Targeted mock unlocked
                </strong>


                <div
                  style={{
                    marginTop: 5,
                    color:
                      "#9db0c8",
                    fontSize: 13,
                  }}
                >

                  The mock will focus on
                  this roadmap skill and
                  its most relevant topic.

                  {" "}

                  Pass score:

                  {" "}

                  {item.mock_pass_score ||
                    70}
                  %.

                </div>


                <button
                  className="button primary small"
                  style={{
                    marginTop: 10,
                  }}
                  disabled={busy}
                  onClick={
                    onStartMock
                  }
                >

                  Start Targeted Mock

                </button>

              </div>

            )}


          {mockDone && (

            <div
              style={{
                marginTop: 14,
                padding:
                  "12px 14px",
                borderRadius: 12,
                background:
                  "rgba(35,170,110,.12)",
                border:
                  "1px solid rgba(35,170,110,.28)",
              }}
            >

              <strong>
                Skill completed
              </strong>


              <div
                style={{
                  marginTop: 5,
                  color:
                    "#9db0c8",
                  fontSize: 13,
                }}
              >

                You completed the learning
                topics and passed the targeted
                mock.

              </div>

            </div>

          )}


          <LearningModule
            content={
              content
            }
            objectives={
              objectives
            }
            concepts={
              concepts
            }
            examples={
              examples
            }
            practice={
              practice
            }
            projectTask={
              item.project_task
            }
          />


          <LiveResourceList
            skill={
              item.skill
            }
            storedResources={
              item.resources
            }
          />

        </div>

      )}

    </div>

  );

}


/*
=========================================================
CHECKLIST
=========================================================
*/

function LearningChecklist({
  checklist,
  completed,
  disabled,
  onChange,
}) {

  return (

    <div
      style={{
        padding: 16,
        borderRadius: 14,
        border:
          "1px solid rgba(255,255,255,.09)",
        background:
          "rgba(4,12,24,.72)",
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          gap: 12,
        }}
      >

        <div>

          <strong>
            Topic-by-topic learning checklist
          </strong>


          <div
            style={{
              color:
                "#8294ac",
              fontSize: 13,
              marginTop: 4,
            }}
          >

            Complete every topic before
            the mock interview unlocks.

          </div>

        </div>


        <span
          className="badge neutral"
        >

          {completed.size}/
          {checklist.length}

        </span>

      </div>


      <div
        style={{
          marginTop: 12,
          display: "grid",
          gap: 8,
        }}
      >

        {checklist.map(
          (
            topic,
            index
          ) => {

            const checked =
              completed.has(
                index
              );


            return (

              <label
                key={
                  `${index}-${topic}`
                }
                style={{
                  display:
                    "flex",
                  alignItems:
                    "flex-start",
                  gap: 10,
                  padding:
                    "10px 12px",
                  borderRadius:
                    10,
                  border:
                    "1px solid rgba(255,255,255,.06)",
                  background:
                    checked
                      ? "rgba(35,170,110,.09)"
                      : "rgba(255,255,255,.025)",
                  cursor:
                    disabled
                      ? "default"
                      : "pointer",
                }}
              >

                <input
                  type="checkbox"
                  checked={
                    checked
                  }
                  disabled={
                    disabled
                  }
                  onChange={
                    (event) =>
                      onChange(
                        topic,
                        event.target.checked
                      )
                  }
                  style={{
                    marginTop: 3,
                  }}
                />


                <span
                  style={{
                    color:
                      checked
                        ? "#d6ffe9"
                        : "#c4d0df",
                  }}
                >

                  <strong
                    style={{
                      color:
                        "#71869f",
                      marginRight: 7,
                    }}
                  >

                    #
                    {index + 1}

                  </strong>

                  {topic}

                </span>

              </label>

            );

          }
        )}

      </div>

    </div>

  );

}


/*
=========================================================
LEARNING MODULE
=========================================================
*/

function LearningModule({
  content,
  objectives,
  concepts,
  examples,
  practice,
  projectTask,
}) {

  const sections =
    useMemo(
      () =>
        [
          [
            "Why this matters",
            content.why_it_matters,
          ],
          [
            "Overview",
            content.overview,
          ],
        ].filter(
          ([, value]) =>
            value
        ),
      [content]
    );


  return (

    <div
      style={{
        marginTop: 16,
        display: "grid",
        gap: 10,
      }}
    >

      {sections.map(
        (
          [
            title,
            text,
          ]
        ) => (

          <div
            key={title}
          >

            <strong>
              {title}
            </strong>


            <p
              style={{
                marginTop: 5,
              }}
            >

              {text}

            </p>

          </div>

        )
      )}


      <ModuleList
        title="Learning objectives"
        items={
          objectives
        }
      />


      <ModuleList
        title="Core concepts"
        items={
          concepts
        }
      />


      <ModuleList
        title="Practical examples"
        items={
          examples
        }
      />


      <ModuleList
        title="Practice tasks"
        items={
          practice
        }
      />


      {projectTask && (

        <div
          style={{
            padding: 14,
            borderRadius: 12,
            background:
              "rgba(114,76,220,.11)",
            border:
              "1px solid rgba(130,95,235,.22)",
          }}
        >

          <strong>
            Project task
          </strong>


          <p
            style={{
              marginTop: 6,
            }}
          >

            {projectTask}

          </p>

        </div>

      )}

    </div>

  );

}


/*
=========================================================
MODULE LIST
=========================================================
*/

function ModuleList({
  title,
  items,
}) {

  if (
    !items?.length
  ) {

    return null;

  }


  return (

    <div>

      <strong>
        {title}
      </strong>


      <ul
        style={{
          marginTop: 6,
          paddingLeft: 20,
        }}
      >

        {items.map(
          (
            item,
            index
          ) => (

            <li
              key={
                `${title}-${index}-${item}`
              }
              style={{
                marginBottom: 5,
              }}
            >

              {item}

            </li>

          )
        )}

      </ul>

    </div>

  );

}


/*
=========================================================
COMMUNITY + CURATED RESOURCES
=========================================================
*/

function LiveResourceList({
  skill,
  storedResources,
}) {

  const [
    community,
    setCommunity,
  ] = useState([]);


  useEffect(
    () => {

      getCommunityResources(
        skill
      )

        .then(
          (result) =>
            setCommunity(
              result.resources ||
              []
            )
        )

        .catch(
          () =>
            setCommunity([])
        );

    },
    [skill]
  );


  async function handleAdd(
    data
  ) {

    const result =
      await addCommunityResource(
        data
      );


    setCommunity(
      (prev) => [
        result.resource,
        ...prev,
      ]
    );

  }


  async function handleUpvote(
    id
  ) {

    const updated =
      await upvoteCommunityResource(
        id
      );


    setCommunity(
      (prev) =>
        prev.map(
          (resource) =>
            resource.id === id
              ? updated
              : resource
        )
    );

  }


  const curatedOnly =
    (
      storedResources ||
      []
    ).filter(
      (resource) =>
        !resource.community
    );


  const communityAsResources =
    community.map(
      (resource) => ({
        id:
          `community-${resource.id}`,

        title:
          resource.title,

        provider:
          `Shared by ${resource.submitted_by_username}`,

        url:
          resource.url,

        type:
          resource.resource_type,

        community:
          true,

        upvotes:
          resource.upvotes,

        _rawId:
          resource.id,
      })
    );


  return (

    <div
      style={{
        marginTop: 16,
      }}
    >

      <ResourceLinks
        resources={[
          ...curatedOnly,
          ...communityAsResources,
        ]}

        onUpvote={
          (id) => {

            const raw =
              communityAsResources.find(
                (resource) =>
                  resource.id ===
                  id
              )?._rawId;


            if (raw) {

              handleUpvote(
                raw
              );

            }

          }
        }
      />


      <AddResourceForm
        skill={skill}
        onSubmit={
          handleAdd
        }
      />

    </div>

  );

}