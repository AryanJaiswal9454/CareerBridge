import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getMatches } from "../api/matching";
import { generateRoadmap } from "../api/roadmap";
import { getCommunityResources, addCommunityResource, upvoteCommunityResource } from "../api/resources";
import { Card, ErrorBox, Empty, Spinner, Gauge, Bar, ResourceLinks, AddResourceForm } from "../components/Ui";
import { Page } from "./Dashboard";

// Indicative readiness percentage per skill category — a simple, honest
// proxy derived from the match engine's categorical rating, not a precise
// measurement.
const LEVEL_PERCENT = { ready: 90, improve: 55, missing: 12 };

export default function SkillGap() {
  const [matches, setMatches] = useState([]);
  const [matchId, setMatchId] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getMatches()
      .then((matchList) => {
        setMatches(matchList || []);
        if (matchList?.length) {
          setMatchId(String(matchList[0].id));
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const match = matches.find((m) => String(m.id) === String(matchId));

  async function buildRoadmap() {
    if (!match) return;
    setBusy(true);
    setError("");
    try {
      await generateRoadmap(match.id);
      navigate("/roadmap");
    } catch (err) {
      setError(err.response?.data?.error || "Unable to generate roadmap.");
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return (
      <Page title="Your Skill Gap Analysis" subtitle="Loading your latest match…">
        <div className="loading">
          <Spinner />
        </div>
      </Page>
    );
  }

  if (!matches.length) {
    return (
      <Page title="Your Skill Gap Analysis" subtitle="Run a match first to see where you stand.">
        <Card>
          <Empty
            icon="△"
            title="No match yet"
            text="Match a resume against a target job description to see your skill gaps here."
            to="/matching"
            label="Run a match"
          />
        </Card>
      </Page>
    );
  }

  const readySkills = match?.matched_skills || [];
  const improveSkills = match?.skills_to_improve || [];
  const missingSkills = [...(match?.missing_skills || []), ...(match?.preferred_skills_missing || [])];
  const readiness = match?.match_score || 0;

  return (
    <Page
      title="Your Skill Gap Analysis"
      subtitle={`Overall Readiness Indicator for ${match?.job_title || "your target role"}.`}
    >
      {matches.length > 1 && (
        <label className="field-label" style={{ maxWidth: 340, marginBottom: 16 }}>
          Comparing against
          <select value={matchId} onChange={(e) => setMatchId(e.target.value)}>
            {matches.map((m) => (
              <option key={m.id} value={m.id}>
                {m.company_name} · {m.job_title}
              </option>
            ))}
          </select>
        </label>
      )}

      <div className="gap-score">
        <Gauge value={readiness} size={100} stroke={10} />
        <div>
          <span>OVERALL READINESS INDICATOR</span>
          <strong style={{ fontSize: 16, display: "block", margin: "6px 0 4px", color: "#fff" }}>
            Ready for {match?.job_title}: {Math.round(readiness)}%
          </strong>
          <p>{readinessSummary(readiness)}</p>
        </div>
      </div>

      <ErrorBox>{error}</ErrorBox>

      <div className="gap-columns">
        <div className="gap-col ok">
          <h4>✓ READY</h4>
          {readySkills.length ? (
            readySkills.map((skill, i) => <SkillRow key={i} skill={skill} level="ready" />)
          ) : (
            <p className="muted">Nothing confirmed yet.</p>
          )}
        </div>

        <div className="gap-col warn">
          <h4>◐ IMPROVE</h4>
          {improveSkills.length ? (
            improveSkills.map((skill, i) => <SkillRow key={i} skill={skill} level="improve" />)
          ) : (
            <p className="muted">Nothing to improve — good sign.</p>
          )}
        </div>

        <div className="gap-col bad">
          <h4>⚠ MISSING</h4>
          {missingSkills.length ? (
            missingSkills.map((skill, i) => <SkillRow key={i} skill={skill} level="missing" />)
          ) : (
            <p className="muted">No missing skills found.</p>
          )}
        </div>
      </div>

      <div className="two-column">
        <div className="explain-panel">
          <h4>◆ AI EXPLANATION PANEL</h4>
          <p>{buildExplanation(improveSkills, missingSkills, match?.job_title)}</p>
        </div>

        <Card title="Learn the gaps" subtitle="Videos, docs and community picks for your top priority skills.">
          {[...missingSkills, ...improveSkills].slice(0, 3).map((skill, i) => (
            <SkillResourceBlock key={i} skill={skill} />
          ))}
          {!missingSkills.length && !improveSkills.length && (
            <p className="muted">No gaps to learn right now — nice work.</p>
          )}
        </Card>
      </div>

      <button className="button primary full" style={{ marginTop: 18 }} disabled={busy} onClick={buildRoadmap}>
        {busy ? <Spinner /> : "Generate My Roadmap →"}
      </button>
    </Page>
  );
}

function readinessSummary(readiness) {
  if (readiness >= 70) return "Strong foundation — a few targeted gaps remain.";
  if (readiness >= 45) return "Good foundation, but key skill gaps remain.";
  return "Early stage — focus on core required skills first.";
}

function SkillRow({ skill, level }) {
  const pct = LEVEL_PERCENT[level];
  const tone = level === "ready" ? "ok" : level === "improve" ? "warn" : "bad";
  const statusLabel = level === "ready" ? "Confident" : level === "improve" ? "Needs practice" : "Start learning";

  return (
    <div className="gap-skill-row">
      <div className="gap-skill-head">
        <strong>{skill}</strong>
        <span>{statusLabel}</span>
      </div>
      <Bar value={pct} tone={tone} />
    </div>
  );
}

function buildExplanation(improveSkills, missingSkills, jobTitle) {
  const priority = [...missingSkills, ...improveSkills].slice(0, 2);

  if (!priority.length) {
    return `Your profile is well aligned with the ${jobTitle || "target"} role. Keep sharpening your strongest skills and start interview practice.`;
  }

  return (
    `Focus on ${priority.join(" and ")} first — they carry the most weight for a ${jobTitle || "this"} role. ` +
    "Your existing strengths are a real advantage, but closing these specific gaps will move your readiness score the most."
  );
}

// Fallback resource links shown before a roadmap exists (the roadmap itself
// carries richer, backend-generated resources once it's been created).
function buildFallbackResources(skill) {
  const courseQuery = encodeURIComponent(`${skill} full course tutorial for beginners`);
  const docQuery = encodeURIComponent(`${skill} official documentation`);
  const normalizedSkill = skill.trim().toLowerCase();

  return [
    {
      title: `${skill} — Full Course / Playlist`,
      provider: "YouTube",
      url: `https://www.youtube.com/results?search_query=${courseQuery}`,
      type: "video",
      ai_recommended: false,
    },
    {
      title: `${skill} — Official Documentation`,
      provider: "Official Docs",
      url: OFFICIAL_DOCS[normalizedSkill] || `https://www.google.com/search?q=${docQuery}`,
      type: "doc",
      ai_recommended: false,
    },
  ];
}

const OFFICIAL_DOCS = {
  python: "https://docs.python.org/3/",
  sql: "https://dev.mysql.com/doc/",
  excel: "https://support.microsoft.com/en-us/excel",
  "power bi": "https://learn.microsoft.com/en-us/power-bi/",
  tableau: "https://help.tableau.com/current/guides/get-started-tutorial/en-us/",
  javascript: "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
  react: "https://react.dev/",
  django: "https://docs.djangoproject.com/",
  html: "https://developer.mozilla.org/en-US/docs/Web/HTML",
  css: "https://developer.mozilla.org/en-US/docs/Web/CSS",
  "machine learning": "https://scikit-learn.org/stable/documentation.html",
  statistics: "https://www.khanacademy.org/math/statistics-probability",
};

// One skill's resource list: curated video + official docs, merged with
// whatever the community has shared for that skill, plus a form to add more.
function SkillResourceBlock({ skill }) {
  const [community, setCommunity] = useState([]);

  useEffect(() => {
    getCommunityResources(skill)
      .then((result) => setCommunity(result.resources || []))
      .catch(() => setCommunity([]));
  }, [skill]);

  async function handleAdd(data) {
    const result = await addCommunityResource(data);
    setCommunity((prev) => [result.resource, ...prev]);
  }

  async function handleUpvote(id) {
    const updated = await upvoteCommunityResource(id);
    setCommunity((prev) => prev.map((r) => (r.id === id ? updated : r)));
  }

  const communityAsResources = community.map((r) => ({
    id: `community-${r.id}`,
    title: r.title,
    provider: `Shared by ${r.submitted_by_username}`,
    url: r.url,
    type: r.resource_type,
    community: true,
    upvotes: r.upvotes,
    _rawId: r.id,
  }));

  return (
    <div style={{ marginBottom: 18 }}>
      <strong style={{ fontSize: 12, display: "block", marginBottom: 6, textTransform: "capitalize" }}>
        {skill}
      </strong>
      <ResourceLinks
        resources={[...buildFallbackResources(skill), ...communityAsResources]}
        onUpvote={(id) => {
          const raw = communityAsResources.find((r) => r.id === id)?._rawId;
          if (raw) handleUpvote(raw);
        }}
      />
      <AddResourceForm skill={skill} onSubmit={handleAdd} />
    </div>
  );
}
