
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  getInterviews,
  createInterview,
  submitInterviewAnswer,
  getInterviewAnalysis,
  getQuestionBankCategories,
  getQuestionBank,
} from "../api/interviews";
import { getMatches } from "../api/matching";
import { Page } from "./Dashboard";
import { Card, Empty, ErrorBox, Spinner, Pill } from "../components/Ui";

const SESSION_TYPES = [
  {
    id: "mcq",
    label: "MCQ Round",
    desc: "Quick multiple-choice questions.",
  },
  {
    id: "technical",
    label: "Technical Round",
    desc: "Coding + MCQ questions.",
  },
  {
    id: "behavioral",
    label: "Behavioral",
    desc: "Open-ended, story-style questions.",
  },
  {
    id: "mixed",
    label: "Mixed",
    desc: "A blend of all three.",
  },
];

export default function Interview() {
  const [searchParams] = useSearchParams();

  // "mock" -> the existing job-match-driven mock interview flow
  // "bank" -> the standalone category+difficulty question bank
  //
  // Roadmap targeted mocks arrive here through:
  // /interview?session_id=<id>
  const [mode, setMode] = useState(
    searchParams.get("mode") === "bank" ? "bank" : "mock"
  );

  const presetCategory = searchParams.get("category");
  const presetDifficulty = searchParams.get("difficulty");

  // IMPORTANT:
  // Roadmap uses this parameter to tell Interview.jsx which
  // already-created targeted mock session to open.
  const requestedSessionId = searchParams.get("session_id");

  const [sessions, setSessions] = useState([]);
  const [matches, setMatches] = useState([]);

  const [sessionType, setSessionType] = useState("mixed");
  const [activeSession, setActiveSession] = useState(null);

  const [selectedOption, setSelectedOption] = useState("");
  const [code, setCode] = useState("");
  const [answer, setAnswer] = useState("");
  const [reveal, setReveal] = useState(null);

  const [analysis, setAnalysis] = useState(null);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [practiceLinks, setPracticeLinks] = useState([]);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  /*
  =========================================================
  LOAD INTERVIEW DATA
  =========================================================

  This function now does two jobs:

  1. Loads the normal interview list.
  2. If Roadmap supplied ?session_id=..., it opens that
     exact targeted session automatically.
  */
  async function load() {
    const [interviewsResult, matchesResult] = await Promise.all([
      getInterviews(),
      getMatches(),
    ]);

    const loadedSessions =
      interviewsResult.sessions || [];

    setSessions(loadedSessions);
    setMatches(matchesResult);

    /*
    ---------------------------------------------------------
    TARGETED ROADMAP MOCK
    ---------------------------------------------------------

    Roadmap creates a targeted interview session first and
    then navigates to:

        /interview?session_id=123

    Previously this value was ignored, which caused the
    Interview page to show the generic "Start interview"
    screen.

    Now we locate the exact session and make it active.
    ---------------------------------------------------------
    */
    if (requestedSessionId) {
      const requestedSession =
        loadedSessions.find(
          (session) =>
            String(session.id) ===
            String(requestedSessionId)
        );

      if (requestedSession) {
        setActiveSession(requestedSession);

        setSessionType(
          requestedSession.session_type ||
            "mixed"
        );

        setReveal(null);
        setShowAnalysis(false);

        /*
        The targeted roadmap session may already contain
        useful practice links in the backend response.
        Normal session history remains fully functional.
        */
        setPracticeLinks(
          requestedSession.practice_links ||
            []
        );
      } else {
        setError(
          "The targeted mock session could not be found."
        );
      }
    }
  }

  /*
  Initial load.

  requestedSessionId is included because the Interview page
  can be opened directly with a different session_id.
  */
  useEffect(() => {
    load().catch((err) => {
      setError(
        err.response?.data?.error ||
          "Unable to load interview sessions."
      );
    });
  }, [requestedSessionId]);

  /*
  =========================================================
  NORMAL MOCK INTERVIEW
  =========================================================
  */

  async function startSession() {
    if (!matches[0]) return;

    setBusy(true);
    setError("");
    setReveal(null);
    setShowAnalysis(false);

    try {
      const questionCount =
        sessionType === "mcq"
          ? 5
          : 6;

      const result =
        await createInterview(
          matches[0].match_id,
          sessionType,
          questionCount
        );

      setActiveSession(
        result.session
      );

      setPracticeLinks(
        result.practice_links || []
      );
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to start interview."
      );
    } finally {
      setBusy(false);
    }
  }

  /*
  =========================================================
  CURRENT QUESTION
  =========================================================
  */

  const currentQuestion =
    activeSession?.questions?.find(
      (question) =>
        !question.answered_at
    );

  /*
  =========================================================
  ANSWER PAYLOAD
  =========================================================
  */

  function buildAnswerPayload(
    question
  ) {
    if (
      question.question_type ===
      "mcq"
    ) {
      return selectedOption
        ? {
            selected_option:
              selectedOption,
          }
        : null;
    }

    if (
      question.question_type ===
      "coding"
    ) {
      return code.trim()
        ? {
            answer: code,
          }
        : null;
    }

    return answer.trim()
      ? {
          answer,
        }
      : null;
  }

  /*
  =========================================================
  SUBMIT ANSWER
  =========================================================
  */

  async function submitAnswer() {
    if (!currentQuestion) {
      return;
    }

    const payload =
      buildAnswerPayload(
        currentQuestion
      );

    if (!payload) {
      return;
    }

    setBusy(true);
    setError("");

    try {
      const result =
        await submitInterviewAnswer(
          currentQuestion.id,
          payload
        );

      setReveal(result);

      const refreshed =
        await getInterviews();

      const refreshedSession =
        refreshed.sessions?.find(
          (session) =>
            session.id ===
            activeSession.id
        );

      setActiveSession(
        refreshedSession ||
          activeSession
      );

      setSessions(
        refreshed.sessions || []
      );

      setSelectedOption("");
      setCode("");
      setAnswer("");
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Answer submission failed."
      );
    } finally {
      setBusy(false);
    }
  }

  /*
  =========================================================
  NEXT QUESTION
  =========================================================
  */

  function goToNextQuestion() {
    setReveal(null);
  }

  /*
  =========================================================
  ANALYSIS
  =========================================================
  */

  async function viewAnalysis(
    sessionId
  ) {
    setBusy(true);
    setError("");

    try {
      const result =
        await getInterviewAnalysis(
          sessionId
        );

      setAnalysis(result);
      setShowAnalysis(true);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to load analysis."
      );
    } finally {
      setBusy(false);
    }
  }

  /*
  =========================================================
  PAGE
  =========================================================
  */

  return (
    <Page
      title="Interview Coach"
      subtitle="Practice MCQs and coding challenges against the same target that produced your skill gaps and roadmap."
    >
      <div
        className="segmented"
        style={{
          justifyContent:
            "flex-start",
          marginBottom: 16,
        }}
      >
        <button
          className={
            mode === "mock"
              ? "selected"
              : ""
          }
          onClick={() =>
            setMode("mock")
          }
        >
          Mock Interview
        </button>

        <button
          className={
            mode === "bank"
              ? "selected"
              : ""
          }
          onClick={() =>
            setMode("bank")
          }
        >
          Question Bank
        </button>
      </div>

      {mode === "bank" ? (
        <QuestionBankTab
          presetCategory={
            presetCategory
          }
          presetDifficulty={
            presetDifficulty
          }
        />
      ) : (
        <>
          <ErrorBox>
            {error}
          </ErrorBox>

          {showAnalysis &&
          analysis ? (
            <AnalysisView
              analysis={analysis}
              onBack={() =>
                setShowAnalysis(
                  false
                )
              }
            />
          ) : !activeSession ? (
            <StartScreen
              sessionType={
                sessionType
              }
              setSessionType={
                setSessionType
              }
              onStart={
                startSession
              }
              busy={busy}
              hasMatch={
                !!matches.length
              }
            />
          ) : (
            <ActiveSessionCard
              session={
                activeSession
              }
              question={
                currentQuestion
              }
              selectedOption={
                selectedOption
              }
              setSelectedOption={
                setSelectedOption
              }
              code={code}
              setCode={setCode}
              answer={answer}
              setAnswer={setAnswer}
              reveal={reveal}
              busy={busy}
              onSubmit={
                submitAnswer
              }
              onNextQuestion={
                goToNextQuestion
              }
              onViewAnalysis={() =>
                viewAnalysis(
                  activeSession.id
                )
              }
              onStartAnother={() => {
                setActiveSession(
                  null
                );
                setReveal(null);
              }}
            />
          )}

          {!showAnalysis &&
            activeSession &&
            practiceLinks.length >
              0 && (
              <Card
                className="section-card"
                title="Take a full mock elsewhere too"
                subtitle="Free topic-wise practice on well-known external platforms."
              >
                <div className="practice-links">
                  {practiceLinks.map(
                    (
                      link,
                      index
                    ) => (
                      <a
                        key={index}
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="practice-link-chip"
                      >
                        <strong>
                          {
                            link.provider
                          }
                        </strong>
                        <span>
                          {
                            link.skill
                          }
                        </span>
                      </a>
                    )
                  )}
                </div>
              </Card>
            )}

          {!showAnalysis &&
            sessions.length >
              0 && (
              <Card
                className="section-card"
                title="Previous sessions"
              >
                <div className="item-list">
                  {sessions.map(
                    (
                      session
                    ) => (
                      <div
                        className="item-row"
                        key={
                          session.id
                        }
                      >
                        <div>
                          <strong>
                            {
                              session.session_type
                            }{" "}
                            interview
                          </strong>

                          <span>
                            {
                              session.questions_answered
                            }
                            /
                            {
                              session.total_questions
                            }{" "}
                            answered
                          </span>
                        </div>

                        <div className="row-actions">
                          <span className="badge neutral">
                            {
                              session.overall_score
                            }
                            %
                          </span>

                          {session.status ===
                            "completed" && (
                            <button
                              className="button ghost small"
                              onClick={() =>
                                viewAnalysis(
                                  session.id
                                )
                              }
                            >
                              Analysis
                            </button>
                          )}
                        </div>
                      </div>
                    )
                  )}
                </div>
              </Card>
            )}
        </>
      )}
    </Page>
  );
}


/*
=========================================================
START SCREEN
=========================================================
*/

function StartScreen({
  sessionType,
  setSessionType,
  onStart,
  busy,
  hasMatch,
}) {
  return (
    <Card
      title="Start a mock interview"
      subtitle="Questions come from your latest job match."
    >
      <div className="interview-start">
        <div className="start-icon">
          ◌
        </div>

        <h3>
          Ready to practice?
        </h3>

        <p>
          Select a round type.
          MCQ and Technical rounds
          include multiple-choice
          and coding questions with
          answers revealed after you
          submit.
        </p>

        <div className="segmented">
          {SESSION_TYPES.map(
            (type) => (
              <button
                key={type.id}
                className={
                  sessionType ===
                  type.id
                    ? "selected"
                    : ""
                }
                onClick={() =>
                  setSessionType(
                    type.id
                  )
                }
                title={type.desc}
              >
                {type.label}
              </button>
            )
          )}
        </div>

        <button
          className="button primary"
          disabled={
            !hasMatch || busy
          }
          onClick={onStart}
        >
          {busy ? (
            <Spinner />
          ) : (
            "Start interview"
          )}
        </button>

        {!hasMatch && (
          <span className="hint">
            Run a match before
            starting an interview.
          </span>
        )}
      </div>
    </Card>
  );
}


/*
=========================================================
ACTIVE SESSION
=========================================================
*/

function ActiveSessionCard({
  session,
  question,
  selectedOption,
  setSelectedOption,
  code,
  setCode,
  answer,
  setAnswer,
  reveal,
  busy,
  onSubmit,
  onNextQuestion,
  onViewAnalysis,
  onStartAnother,
}) {
  return (
    <Card
      title={`Interview · ${session.session_type}`}
      subtitle={`${session.questions_answered}/${session.total_questions} answered · ${session.overall_score}% so far`}
    >
      <div className="question-card">
        {question ? (
          <QuestionView
            session={session}
            question={question}
            selectedOption={
              selectedOption
            }
            setSelectedOption={
              setSelectedOption
            }
            code={code}
            setCode={setCode}
            answer={answer}
            setAnswer={setAnswer}
            reveal={reveal}
            busy={busy}
            onSubmit={onSubmit}
            onNextQuestion={
              onNextQuestion
            }
          />
        ) : (
          <div className="completed">
            <strong>
              Interview complete
            </strong>

            <span>
              {
                session.overall_score
              }
              % overall score
            </span>

            <button
              className="button ghost"
              onClick={
                onViewAnalysis
              }
            >
              View analysis →
            </button>

            <button
              className="button secondary"
              onClick={
                onStartAnother
              }
            >
              Start another
            </button>
          </div>
        )}
      </div>
    </Card>
  );
}


/*
=========================================================
QUESTION VIEW
=========================================================
*/

function QuestionView({
  session,
  question,
  selectedOption,
  setSelectedOption,
  code,
  setCode,
  answer,
  setAnswer,
  reveal,
  busy,
  onSubmit,
  onNextQuestion,
}) {
  const questionNumber =
    session.questions.findIndex(
      (q) =>
        q.id === question.id
    ) + 1;

  return (
    <>
      <span className="question-label">
        QUESTION{" "}
        {questionNumber} ·{" "}
        {question.question_type.toUpperCase()}
        {question.related_skill
          ? ` · ${question.related_skill}`
          : ""}
      </span>

      <h2>
        {question.question}
      </h2>

      {!reveal &&
        question.question_type ===
          "mcq" && (
          <div className="mcq-options">
            {(question.options ||
              []).map(
              (
                option,
                index
              ) => {
                const letter =
                  String.fromCharCode(
                    65 + index
                  );

                return (
                  <div
                    key={letter}
                    className={`mcq-option${
                      selectedOption ===
                      letter
                        ? " selected"
                        : ""
                    }`}
                    onClick={() =>
                      setSelectedOption(
                        letter
                      )
                    }
                  >
                    <span className="mcq-option-letter">
                      {letter}
                    </span>

                    <span>
                      {option}
                    </span>
                  </div>
                );
              }
            )}
          </div>
        )}

      {!reveal &&
        question.question_type ===
          "coding" && (
          <textarea
            className="code-editor"
            rows="9"
            value={
              code ||
              question.starter_code ||
              ""
            }
            onChange={(e) =>
              setCode(
                e.target.value
              )
            }
            placeholder="Write your code here…"
          />
        )}

      {!reveal &&
        question.question_type ===
          "open" && (
          <textarea
            rows="8"
            value={answer}
            onChange={(e) =>
              setAnswer(
                e.target.value
              )
            }
            placeholder="Structure your answer with an explanation, example and connection to the role…"
          />
        )}

      {!reveal && (
        <button
          className="button primary"
          disabled={busy}
          onClick={onSubmit}
        >
          {busy ? (
            <Spinner />
          ) : (
            "Submit answer"
          )}
        </button>
      )}

      {reveal && (
        <RevealPanel
          result={reveal}
          questionType={
            question.question_type
          }
          onNext={
            onNextQuestion
          }
        />
      )}
    </>
  );
}


/*
=========================================================
REVEAL PANEL
=========================================================
*/

function RevealPanel({
  result,
  questionType,
  onNext,
}) {
  const isCorrect =
    result.is_correct;

  return (
    <div
      className={`reveal-panel ${
        isCorrect
          ? "correct"
          : "incorrect"
      }`}
    >
      <h4>
        {isCorrect
          ? "✓ Correct"
          : "✗ Not quite"}{" "}
        · Score: {result.score}%
      </h4>

      <p>
        {result.feedback}
      </p>

      {questionType ===
        "mcq" && (
        <p>
          <strong>
            Correct answer:
          </strong>{" "}
          Option{" "}
          {result.correct_option} —{" "}
          {result.explanation}
        </p>
      )}

      {questionType ===
        "coding" && (
        <>
          <p>
            <strong>
              Explanation:
            </strong>{" "}
            {result.explanation}
          </p>

          {result.sample_solution && (
            <pre>
              {result.sample_solution}
            </pre>
          )}
        </>
      )}

      {(
        result.improvement_tips ||
        []
      ).length > 0 && (
        <>
          <p
            style={{
              marginBottom: 4,
            }}
          >
            <strong>
              What to improve:
            </strong>
          </p>

          <ul>
            {result.improvement_tips.map(
              (
                tip,
                index
              ) => (
                <li key={index}>
                  {tip}
                </li>
              )
            )}
          </ul>
        </>
      )}

      <button
        className="button primary small"
        style={{
          marginTop: 10,
        }}
        onClick={onNext}
      >
        Next question →
      </button>
    </div>
  );
}


/*
=========================================================
ANALYSIS VIEW
=========================================================
*/

function AnalysisView({
  analysis,
  onBack,
}) {
  return (
    <Card
      title="Interview Analysis"
      subtitle={`${analysis.session_type} round · ${analysis.questions_answered}/${analysis.total_questions} answered`}
    >
      <div className="summary-banner">
        {analysis.summary}
      </div>

      <div className="analysis-grid">
        <div className="analysis-stat">
          <strong>
            {analysis.overall_score}%
          </strong>

          <span>
            Overall score
          </span>
        </div>

        <div className="analysis-stat">
          <strong>
            {analysis.by_type.mcq.count}
          </strong>

          <span>
            MCQs ·{" "}
            {
              analysis.by_type.mcq
                .correct
            }{" "}
            correct
          </span>
        </div>

        <div className="analysis-stat">
          <strong>
            {
              analysis.by_type
                .coding.count
            }
          </strong>

          <span>
            Coding · avg{" "}
            {
              analysis.by_type
                .coding
                .average_score ??
              "—"
            }
            %
          </span>
        </div>
      </div>

      {analysis.skill_breakdown
        .length > 0 && (
        <div
          style={{
            marginBottom: 16,
          }}
        >
          <h4
            style={{
              fontSize: 10,
              letterSpacing: 0.5,
              textTransform:
                "uppercase",
              color: "#8B96AD",
              margin:
                "0 0 8px",
            }}
          >
            Skill performance
          </h4>

          {analysis.skill_breakdown.map(
            (
              skill,
              index
            ) => (
              <div
                className="skill-perf-row"
                key={index}
              >
                <span>
                  {skill.skill}
                </span>

                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{
                      width: `${skill.average_score}%`,
                    }}
                  />
                </div>

                <b>
                  {
                    skill.average_score
                  }
                  %
                </b>
              </div>
            )
          )}
        </div>
      )}

      <div
        style={{
          display: "flex",
          gap: 8,
          flexWrap: "wrap",
          marginBottom: 14,
        }}
      >
        {analysis.strong_skills.map(
          (skill) => (
            <Pill
              tone="ok"
              key={skill}
            >
              Strong: {skill}
            </Pill>
          )
        )}

        {analysis.weak_skills.map(
          (skill) => (
            <Pill
              tone="bad"
              key={skill}
            >
              Focus: {skill}
            </Pill>
          )
        )}
      </div>

      <button
        className="button ghost"
        onClick={onBack}
      >
        ← Back
      </button>
    </Card>
  );
}


const DIFFICULTIES = [
  {
    id: "easy",
    label: "Easy",
  },
  {
    id: "medium",
    label: "Medium",
  },
  {
    id: "hard",
    label: "Hard",
  },
];


/*
=========================================================
QUESTION BANK
=========================================================

The standalone category/difficulty
practice library is independent of
the job-match-driven mock.
*/

function QuestionBankTab({
  presetCategory,
  presetDifficulty,
}) {
  const [categories, setCategories] =
    useState([]);

  const [category, setCategory] =
    useState(
      presetCategory || null
    );

  const [difficulty, setDifficulty] =
    useState(
      [
        "easy",
        "medium",
        "hard",
      ].includes(
        presetDifficulty
      )
        ? presetDifficulty
        : "medium"
    );

  const [questions, setQuestions] =
    useState(null);

  const [revealedIds, setRevealedIds] =
    useState({});

  const [busy, setBusy] =
    useState(false);

  const [error, setError] =
    useState("");

  /*
  Load categories.
  */
  useEffect(() => {
    getQuestionBankCategories()
      .then((result) =>
        setCategories(
          result.categories ||
            []
        )
      )
      .catch(() =>
        setError(
          "Unable to load categories."
        )
      );
  }, []);

  /*
  Arrived through a deep link?
  Generate the set automatically.
  */
  useEffect(() => {
    if (presetCategory) {
      generateSet();
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function generateSet() {
    if (!category) {
      return;
    }

    setBusy(true);
    setError("");
    setQuestions(null);
    setRevealedIds({});

    try {
      const result =
        await getQuestionBank(
          category,
          difficulty,
          20
        );

      setQuestions(
        result.questions
      );
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to generate questions."
      );
    } finally {
      setBusy(false);
    }
  }

  function toggleReveal(id) {
    setRevealedIds(
      (prev) => ({
        ...prev,
        [id]: !prev[id],
      })
    );
  }

  return (
    <>
      <ErrorBox>
        {error}
      </ErrorBox>

      <Card
        title="Build a practice set"
        subtitle="Pick a topic and difficulty — 20 questions, answers included, mix of MCQ, coding and conceptual."
      >
        <div className="category-grid">
          {categories.map(
            (c) => (
              <button
                key={c.id}
                className={`category-card${
                  category === c.id
                    ? " selected"
                    : ""
                }`}
                onClick={() =>
                  setCategory(
                    c.id
                  )
                }
              >
                {c.label}
              </button>
            )
          )}
        </div>

        <div
          className="segmented"
          style={{
            margin:
              "16px 0",
          }}
        >
          {DIFFICULTIES.map(
            (d) => (
              <button
                key={d.id}
                className={
                  difficulty ===
                  d.id
                    ? "selected"
                    : ""
                }
                onClick={() =>
                  setDifficulty(
                    d.id
                  )
                }
              >
                {d.label}
              </button>
            )
          )}
        </div>

        <button
          className="button primary"
          disabled={
            !category || busy
          }
          onClick={
            generateSet
          }
        >
          {busy ? (
            <Spinner />
          ) : (
            "Generate 20 questions"
          )}
        </button>
      </Card>

      {questions && (
        <Card
          className="section-card"
          title={`${category} · ${difficulty}`}
          subtitle={`${questions.length} questions`}
        >
          <div className="qbank-list">
            {questions.map(
              (
                q,
                index
              ) => (
                <QuestionBankItem
                  key={
                    q.id ||
                    index
                  }
                  index={
                    index + 1
                  }
                  question={q}
                  revealed={
                    !!revealedIds[
                      q.id ||
                        index
                    ]
                  }
                  onToggle={() =>
                    toggleReveal(
                      q.id ||
                        index
                    )
                  }
                />
              )
            )}
          </div>
        </Card>
      )}
    </>
  );
}


/*
=========================================================
QUESTION BANK ITEM
=========================================================
*/

function QuestionBankItem({
  index,
  question,
  revealed,
  onToggle,
}) {
  return (
    <div className="qbank-item">
      <div className="qbank-item-head">
        <span className="qbank-number">
          {index}
        </span>

        <Pill tone="neutral">
          {
            question.question_type
          }
        </Pill>

        <Pill
          tone={
            question.difficulty ===
            "hard"
              ? "bad"
              : question.difficulty ===
                "easy"
              ? "ok"
              : "warn"
          }
        >
          {question.difficulty}
        </Pill>
      </div>

      <p className="qbank-question">
        {question.question}
      </p>

      {question.question_type ===
        "mcq" && (
        <ul className="qbank-options">
          {(question.options ||
            []).map(
            (
              option,
              i
            ) => {
              const letter =
                String.fromCharCode(
                  65 + i
                );

              const isCorrect =
                revealed &&
                letter ===
                  question.correct_option;

              return (
                <li
                  key={letter}
                  className={
                    isCorrect
                      ? "correct"
                      : ""
                  }
                >
                  <strong>
                    {letter}.
                  </strong>{" "}
                  {option}
                </li>
              );
            }
          )}
        </ul>
      )}

      {question.question_type ===
        "coding" &&
        question.starter_code && (
          <pre className="qbank-code">
            {
              question.starter_code
            }
          </pre>
        )}

      <button
        className="button ghost small"
        onClick={onToggle}
      >
        {revealed
          ? "Hide answer"
          : "Show answer"}
      </button>

      {revealed && (
        <div className="qbank-answer">
          {question.question_type ===
            "mcq" && (
            <p>
              <strong>
                Correct answer:
              </strong>{" "}
              Option{" "}
              {
                question.correct_option
              } —{" "}
              {
                question.explanation
              }
            </p>
          )}

          {question.question_type ===
            "coding" && (
            <>
              <p>
                <strong>
                  Explanation:
                </strong>{" "}
                {
                  question.explanation
                }
              </p>

              {question.sample_solution && (
                <pre>
                  {
                    question.sample_solution
                  }
                </pre>
              )}
            </>
          )}

          {question.question_type ===
            "conceptual" && (
            <>
              <p>
                <strong>
                  Model answer:
                </strong>{" "}
                {
                  question.model_answer
                }
              </p>

              {(
                question.key_points ||
                []
              ).length > 0 && (
                <ul>
                  {question.key_points.map(
                    (
                      point,
                      i
                    ) => (
                      <li key={i}>
                        {point}
                      </li>
                    )
                  )}
                </ul>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

