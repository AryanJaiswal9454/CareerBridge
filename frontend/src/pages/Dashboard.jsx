import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  ResponsiveContainer, LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip,
} from "recharts";
import { getProfile, getSkills } from "../api/profile";
import { getResumes } from "../api/resumes";
import { getJobDescriptions } from "../api/careers";
import { getMatches } from "../api/matching";
import { getRoadmaps } from "../api/roadmap";
import { getInterviews } from "../api/interviews";
import { Card, Empty, Spinner, Gauge, Bar as ProgressBar, Pill } from "../components/Ui";

// Rough proficiency -> percentage mapping, used to draw the skill bars
// until we have a more precise per-skill score from the backend.
const PROFICIENCY_PERCENT = {
  beginner: 40,
  intermediate: 70,
  advanced: 92,
};

export default function Dashboard() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      getProfile(),
      getSkills(),
      getResumes(),
      getJobDescriptions(),
      getMatches(),
      getRoadmaps(),
      getInterviews(),
    ])
      .then((results) => {
        const value = (index) => (results[index].status === "fulfilled" ? results[index].value : null);
        setData({
          profile: value(0),
          skills: value(1) || [],
          resumes: value(2) || [],
          jobs: value(3) || [],
          matches: value(4) || [],
          roadmaps: value(5)?.roadmaps || [],
          interviews: value(6)?.sessions || [],
        });
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <Page title="Good morning" subtitle="Preparing your career workspace…">
        <div className="loading">
          <Spinner />
        </div>
      </Page>
    );
  }

  const profile = data.profile || {};
  const matches = data.matches || [];
  const interviews = data.interviews || [];
  const latestMatch = matches[0];
  const roadmap = data.roadmaps?.[0];
  const resume = data.resumes?.[0];

  const roadmapItems = roadmap?.items || [];
  const roadmapDoneCount = roadmapItems.filter((item) => item.status === "completed").length;
  const roadmapProgress = roadmapItems.length
    ? Math.round((roadmapDoneCount / roadmapItems.length) * 100)
    : 0;

  const insights = buildInsights({ matches, interviews });
  const quote = pickQuote(insights.averageMatchScore);
  const weakSpotLink = buildWeakSpotLink(insights.recurringGaps);
  const nextStep = getNextStep({ profile, data, latestMatch, roadmapProgress });

  const welcomeName = profile.full_name || localStorage.getItem("username") || "Student";
  const subtitle = profile.career_goal
    ? `Target Career: ${profile.career_goal}`
    : "CareerBridge turns your current profile into a clear, evidence-based job-readiness journey.";

  return (
    <Page title={`Welcome back, ${welcomeName}.`} subtitle={subtitle}>
      {/* Hero: readiness gauge + a quote that reacts to how things are actually going */}
      <div className="dash-hero">
        <div className="dash-hero-gauge">
          <Gauge value={latestMatch ? latestMatch.match_score : 0} label="Readiness" />
        </div>
        <div className="dash-hero-quote">
          <span className="eyebrow">TODAY'S TAKEAWAY</span>
          <h2>{quote}</h2>
          <p>
            Based on {matches.length} match{matches.length === 1 ? "" : "es"} and{" "}
            {interviews.length} interview session{interviews.length === 1 ? "" : "s"} on record.
          </p>
        </div>
      </div>

      {/* KPI row: the headline numbers across everything the user has done so far */}
      <div className="kpi-row">
        <KpiCard label="Matches run" value={matches.length} icon="⇄" />
        <KpiCard label="Avg. match score" value={insights.averageMatchScore !== null ? `${insights.averageMatchScore}%` : "—"} icon="◎" />
        <KpiCard label="Roadmap complete" value={`${roadmapProgress}%`} icon="✓" />
        <KpiCard label="Interview avg." value={insights.averageInterviewScore !== null ? `${insights.averageInterviewScore}%` : "—"} icon="◌" />
      </div>

      {/* Trend charts: is the person actually improving over time */}
      <div className="chart-row">
        <Card title="Match score over time" subtitle="Every resume-to-JD comparison you've run.">
          {matches.length > 1 ? (
            <ResponsiveContainer width="100%" height={180}>
              <LineChart data={insights.matchTrend}>
                <CartesianGrid stroke="#1E2536" vertical={false} />
                <XAxis dataKey="label" stroke="#8B96AD" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="#8B96AD" fontSize={11} tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip contentStyle={{ background: "#0D1220", border: "1px solid #1E2536", borderRadius: 10, fontSize: 12 }} />
                <Line type="monotone" dataKey="score" stroke="#22D3EE" strokeWidth={2.5} dot={{ r: 4, fill: "#22D3EE" }} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <Empty icon="⇄" title="Not enough data yet" text="Run a couple more matches to see your trend." to="/matching" label="Run a match" />
          )}
        </Card>

        <Card title="Interview score over time" subtitle="Every mock interview session you've completed.">
          {interviews.filter((s) => s.status === "completed").length > 1 ? (
            <ResponsiveContainer width="100%" height={180}>
              <LineChart data={insights.interviewTrend}>
                <CartesianGrid stroke="#1E2536" vertical={false} />
                <XAxis dataKey="label" stroke="#8B96AD" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="#8B96AD" fontSize={11} tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip contentStyle={{ background: "#0D1220", border: "1px solid #1E2536", borderRadius: 10, fontSize: 12 }} />
                <Line type="monotone" dataKey="score" stroke="#8B5CF6" strokeWidth={2.5} dot={{ r: 4, fill: "#8B5CF6" }} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <Empty icon="◌" title="Not enough data yet" text="Complete a couple more interview sessions to see your trend." to="/interview" label="Start an interview" />
          )}
        </Card>
      </div>

      {/* The single most useful insight: what keeps showing up as a gap, across every match run */}
      <Card
        className="section-card"
        title="Your recurring gaps"
        subtitle="Skills that show up as missing or needing work across all your matches — fix these first."
      >
        {insights.recurringGaps.length ? (
          <ResponsiveContainer width="100%" height={Math.max(120, insights.recurringGaps.length * 34)}>
            <BarChart data={insights.recurringGaps} layout="vertical" margin={{ left: 10 }}>
              <CartesianGrid stroke="#1E2536" horizontal={false} />
              <XAxis type="number" stroke="#8B96AD" fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
              <YAxis type="category" dataKey="skill" stroke="#8B96AD" fontSize={12} tickLine={false} axisLine={false} width={110} />
              <Tooltip contentStyle={{ background: "#0D1220", border: "1px solid #1E2536", borderRadius: 10, fontSize: 12 }} />
              <Bar dataKey="count" fill="#F87171" radius={[0, 6, 6, 0]} barSize={16} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="muted">No recurring gaps yet — run a match to start building this picture.</p>
        )}
      </Card>

      <div className="dash-grid" style={{ gridTemplateColumns: "minmax(0,1fr) minmax(0,1fr) minmax(0,1.4fr)" }}>
        <div className="dash-card">
          <h4>Resume Status</h4>
          {resume ? (
            <div className="status-row">
              <strong>{resume.title}</strong>
              <Pill tone={resume.has_ai_analysis ? "ok" : "warn"}>
                {resume.has_ai_analysis ? "Complete" : "Refine"}
              </Pill>
            </div>
          ) : (
            <Empty icon="▤" title="No resume" text="Upload your resume to get started." to="/resume" label="Upload resume" />
          )}
        </div>

        <div className="dash-card">
          <h4>Interview Preparation Status</h4>
          <div className="status-row">
            <span>Sessions completed</span>
            <strong>{interviews.filter((s) => s.status === "completed").length}</strong>
          </div>
          <div className="status-row">
            <span>Weakest round type</span>
            <span className="muted">{insights.weakestRoundType || "—"}</span>
          </div>
          {weakSpotLink ? (
            <Link className="button primary small" to={weakSpotLink} style={{ marginTop: 10 }}>
              🎯 Practice my weak spot
            </Link>
          ) : (
            <Link className="button ghost small" to="/interview" style={{ marginTop: 10 }}>
              Open Interview Coach
            </Link>
          )}
        </div>

        <div className="next-step-card">
          <div>
            <h4>Recommended Next Step</h4>
            <h3>{nextStep.title}</h3>
            <p style={{ fontSize: 12, color: "#eef1ff", margin: "-8px 0 12px" }}>{nextStep.description}</p>
          </div>
          <Link className="button" to={nextStep.to}>
            Continue →
          </Link>
        </div>
      </div>

      <Card className="section-card" title="CareerBridge flow" subtitle="Everything stays connected.">
        <div className="flow-list">
          {FLOW_STEPS.map((step) => (
            <Link to={step.to} className="flow-item" key={step.number}>
              <b>{step.number}</b>
              <div>
                <strong>{step.title}</strong>
                <span>{step.description}</span>
              </div>
              <em>→</em>
            </Link>
          ))}
        </div>
      </Card>
    </Page>
  );
}

function KpiCard({ label, value, icon }) {
  return (
    <div className="kpi-card">
      <span className="kpi-icon">{icon}</span>
      <strong>{value}</strong>
      <span className="kpi-label">{label}</span>
    </div>
  );
}

// Crunches every match and interview session on record into the handful
// of numbers/charts that actually help someone see their mistakes at a
// glance, instead of re-displaying the same single-match data as every
// other page.
function buildInsights({ matches, interviews }) {
  const averageMatchScore = matches.length
    ? Math.round(matches.reduce((sum, m) => sum + m.match_score, 0) / matches.length)
    : null;

  const matchTrend = [...matches]
    .reverse()
    .map((m, index) => ({ label: `#${index + 1}`, score: Math.round(m.match_score) }));

  const completedInterviews = interviews.filter((s) => s.status === "completed");
  const averageInterviewScore = completedInterviews.length
    ? Math.round(completedInterviews.reduce((sum, s) => sum + (s.overall_score || 0), 0) / completedInterviews.length)
    : null;

  const interviewTrend = [...completedInterviews]
    .reverse()
    .map((s, index) => ({ label: `#${index + 1}`, score: Math.round(s.overall_score || 0) }));

  const gapCounts = {};
  matches.forEach((match) => {
    [...(match.missing_skills || []), ...(match.skills_to_improve || [])].forEach((skill) => {
      gapCounts[skill] = (gapCounts[skill] || 0) + 1;
    });
  });
  const recurringGaps = Object.entries(gapCounts)
    .map(([skill, count]) => ({ skill, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 6);

  const roundScores = {};
  completedInterviews.forEach((session) => {
    if (!roundScores[session.session_type]) roundScores[session.session_type] = [];
    roundScores[session.session_type].push(session.overall_score || 0);
  });
  let weakestRoundType = null;
  let weakestAverage = Infinity;
  Object.entries(roundScores).forEach(([type, scores]) => {
    const average = scores.reduce((sum, s) => sum + s, 0) / scores.length;
    if (average < weakestAverage) {
      weakestAverage = average;
      weakestRoundType = type;
    }
  });

  return { averageMatchScore, matchTrend, averageInterviewScore, interviewTrend, recurringGaps, weakestRoundType };
}

const QUOTES_BY_BAND = {
  high: [
    "You're in strong shape — this is a great time to start applying.",
    "Consistency got you here. Keep the roadmap moving and stay interview-ready.",
  ],
  medium: [
    "Good foundation. A focused week on your top gap will move the needle fast.",
    "You're closer than it feels — close the top 2 gaps and re-run a match.",
  ],
  low: [
    "Every strong profile starts here. Pick one skill from your roadmap and start today.",
    "Small, consistent steps beat cramming. Start with your single biggest gap.",
  ],
  none: [
    "Upload a resume and a real job description to see where you actually stand.",
  ],
};

function pickQuote(averageMatchScore) {
  const band = averageMatchScore === null ? "none" : averageMatchScore >= 75 ? "high" : averageMatchScore >= 50 ? "medium" : "low";
  const options = QUOTES_BY_BAND[band];
  return options[Math.floor(Math.random() * options.length)];
}


// Matches the person's most common skill gap to a real Question Bank
// category (mirrors backend QUESTION_BANK_CATEGORIES), so the "Practice my
// weak spot" shortcut always lands on a category that actually exists —
// falling back to the broad "Data Analytics" blend if nothing matches.
const KNOWN_QUESTION_BANK_CATEGORIES = [
  "python", "sql", "excel", "power bi", "statistics", "javascript", "react",
  "django", "html", "css", "git", "streamlit", "python libraries",
];

function buildWeakSpotLink(recurringGaps) {
  if (!recurringGaps?.length) return null;

  const topGap = recurringGaps[0].skill.trim().toLowerCase();
  const matchedCategory = KNOWN_QUESTION_BANK_CATEGORIES.find(
    (cat) => cat === topGap || topGap.includes(cat) || cat.includes(topGap)
  );
  const category = matchedCategory || "data analytics";

  return `/interview?mode=bank&category=${encodeURIComponent(category)}&difficulty=hard`;
}

const FLOW_STEPS = [
  { number: "01", title: "Profile", description: "Tell us where you are", to: "/profile" },
  { number: "02", title: "Resume", description: "Understand your evidence", to: "/resume" },
  { number: "03", title: "Job Description", description: "Use the exact target", to: "/job-description" },
  { number: "04", title: "Match → Roadmap", description: "Close the gaps", to: "/matching" },
  { number: "05", title: "Interview Coach", description: "Practice and reveal gaps", to: "/interview" },
];

// Works out the single most useful thing the person should do next,
// by walking the CareerBridge pipeline in order and stopping at the
// first step that isn't done yet.
function getNextStep({ profile, data, latestMatch, roadmapProgress }) {
  if (!profile.career_goal) {
    return { title: "Complete your profile", description: "Add your target role, education and background.", to: "/profile" };
  }
  if (!data.resumes?.length) {
    return { title: "Upload your resume", description: "Your resume powers analysis and matching.", to: "/resume" };
  }
  if (!data.jobs?.length) {
    return { title: "Add a target JD", description: "Use the exact company job description you want to pursue.", to: "/job-description" };
  }
  if (!latestMatch) {
    return { title: "Run your first match", description: "Compare your resume with your target job.", to: "/matching" };
  }
  if (!data.roadmaps?.length) {
    return { title: "Build your roadmap", description: "Turn your skill gaps into a practical plan.", to: "/roadmap" };
  }
  if (roadmapProgress < 100) {
    return { title: "Continue your roadmap", description: `${roadmapProgress}% complete — keep the momentum going.`, to: "/roadmap" };
  }
  return { title: "Practice your interview", description: "Use the target role to rehearse interview questions.", to: "/interview" };
}

// Shared page header used by every screen: an eyebrow label, a title,
// a one-line subtitle, and whatever page content is passed as children.
export function Page({ title, subtitle, children, eyebrow = "CAREERBRIDGE AI" }) {
  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">{eyebrow}</span>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </div>
      {children}
    </div>
  );
}
