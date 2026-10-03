import { useEffect, useState } from "react";
import { getResumes } from "../api/resumes";
import { getJobDescriptions } from "../api/careers";
import { getMatches, matchResumeToJob, getResumeOptimization, getTailoredResume, downloadTailoredResume } from "../api/matching";
import { Card, ErrorBox, SuccessBox, Empty, Spinner, Gauge, Pill } from "../components/Ui";
import { Page } from "./Dashboard";

export default function Matching() {
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [matches, setMatches] = useState([]);

  const [resumeId, setResumeId] = useState("");
  const [jobId, setJobId] = useState("");

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  const [tab, setTab] = useState("overview");
  const [optimization, setOptimization] = useState(null);
  const [optimizationLoading, setOptimizationLoading] = useState(false);
  const [optimizationError, setOptimizationError] = useState("");

  const [tailoredResume, setTailoredResume] = useState(null);
  const [tailoredHistory, setTailoredHistory] = useState([]);
  const [selectedTailoredVersion, setSelectedTailoredVersion] = useState(null);
  const [tailoredResumeLoading, setTailoredResumeLoading] = useState(false);
  const [tailoredResumeError, setTailoredResumeError] = useState("");
  const [downloading, setDownloading] = useState(false);

  async function load() {
    const [resumesResult, jobsResult, matchesResult] = await Promise.allSettled([
      getResumes(),
      getJobDescriptions(),
      getMatches(),
    ]);
    setResumes(resumesResult.status === "fulfilled" ? resumesResult.value : []);
    setJobs(jobsResult.status === "fulfilled" ? jobsResult.value : []);
    setMatches(matchesResult.status === "fulfilled" ? matchesResult.value : []);
  }

  useEffect(() => {
    load();
  }, []);

  async function runMatch() {
    setBusy(true);
    setError("");
    setOk("");
    try {
      const result = await matchResumeToJob(resumeId, jobId);
      setOk(`Match created: ${Math.round(result.match_score)}%`);
      setTab("overview");
      setOptimization(null);
      await load();
    } catch (err) {
      setError(
        err.response?.data?.message ||
        err.response?.data?.error ||
        "Matching failed. Analyze both documents first."
      );
    } finally {
      setBusy(false);
    }
  }

  const latestMatch = matches[0];
  const recommendation = latestMatch ? buildRecommendation(latestMatch) : null;

  async function openOptimizationTab() {
    setTab("optimization");
    if (optimization || !latestMatch) return;

    setOptimizationLoading(true);
    setOptimizationError("");
    try {
      const result = await getResumeOptimization(latestMatch.id);
      setOptimization(result);
    } catch (err) {
      setOptimizationError(err.response?.data?.error || "Unable to generate optimization suggestions.");
    } finally {
      setOptimizationLoading(false);
    }
  }

  async function regenerateOptimization() {
    if (!latestMatch) return;

    setOptimizationLoading(true);
    setOptimizationError("");
    try {
      const result = await getResumeOptimization(latestMatch.id, true);
      setOptimization(result);
    } catch (err) {
      setOptimizationError(err.response?.data?.error || "Unable to regenerate suggestions.");
    } finally {
      setOptimizationLoading(false);
    }
  }

  async function openTailoredResumeTab() {
    setTab("tailored");
    if (tailoredResume || !latestMatch) return;

    setTailoredResumeLoading(true);
    setTailoredResumeError("");
    try {
      const result = await getTailoredResume(latestMatch.id);
      setTailoredResume(result);
      setTailoredHistory(result.history || []);
      setSelectedTailoredVersion((result.history || []).length ? result.history[result.history.length - 1].version : null);
    } catch (err) {
      setTailoredResumeError(err.response?.data?.error || "Unable to generate a tailored resume.");
    } finally {
      setTailoredResumeLoading(false);
    }
  }

  async function regenerateTailoredResume() {
    if (!latestMatch) return;

    setTailoredResumeLoading(true);
    setTailoredResumeError("");
    try {
      const result = await getTailoredResume(latestMatch.id, true);
      setTailoredResume(result);
      setTailoredHistory(result.history || []);
      setSelectedTailoredVersion((result.history || []).length ? result.history[result.history.length - 1].version : null);
    } catch (err) {
      setTailoredResumeError(err.response?.data?.error || "Unable to regenerate the tailored resume.");
    } finally {
      setTailoredResumeLoading(false);
    }
  }

  function selectPreviousTailoredResume(version) {
    if (!version?.data) return;
    setTailoredResume(version.data);
    setSelectedTailoredVersion(version.version);
    setTailoredResumeError("");
  }

  async function handleDownload() {
    if (!latestMatch) return;
    setDownloading(true);
    try {
      const filename = `Tailored_Resume_${latestMatch.company_name}_${latestMatch.job_title}.docx`.replace(/\s+/g, "_");
      await downloadTailoredResume(latestMatch.id, filename, selectedTailoredVersion);
    } catch (err) {
      setTailoredResumeError("Download failed. Generate the tailored resume first.");
    } finally {
      setDownloading(false);
    }
  }

  return (
    <Page title="Job Matching" subtitle="Put your resume against the exact target JD and see what actually lines up.">
      <div className="match-controls">
        <div>
          <span>01</span>
          <strong>Select evidence</strong>
          <p>Choose an analyzed resume and analyzed target job.</p>
        </div>

        <label>
          Resume
          <select value={resumeId} onChange={(e) => setResumeId(e.target.value)}>
            <option value="">Choose resume</option>
            {resumes.map((resume) => (
              <option key={resume.id} value={resume.id}>
                {resume.title}{resume.has_ai_analysis ? " · ready" : " · analyze first"}
              </option>
            ))}
          </select>
        </label>

        <div className="connector">×</div>

        <label>
          Target JD
          <select value={jobId} onChange={(e) => setJobId(e.target.value)}>
            <option value="">Choose target</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.company_name} · {job.job_title}{job.ai_analysis ? " · ready" : " · analyze first"}
              </option>
            ))}
          </select>
        </label>

        <button className="button primary" disabled={!resumeId || !jobId || busy} onClick={runMatch}>
          {busy ? <Spinner /> : "Run match →"}
        </button>
      </div>

      <ErrorBox>{error}</ErrorBox>
      <SuccessBox>{ok}</SuccessBox>

      {!latestMatch ? (
        <Card>
          <Empty
            icon="⇄"
            title="No match yet"
            text="Analyze a resume and exact JD, then run your first comparison."
            to="/resume"
            label="Start with resume"
          />
        </Card>
      ) : (
        <>
          <div className="segmented" style={{ justifyContent: "flex-start", marginBottom: 16 }}>
            <button className={tab === "overview" ? "selected" : ""} onClick={() => setTab("overview")}>
              Match Overview
            </button>
            <button className={tab === "optimization" ? "selected" : ""} onClick={openOptimizationTab}>
              Resume Optimization
            </button>
            <button className={tab === "tailored" ? "selected" : ""} onClick={openTailoredResumeTab}>
              Tailored Resume
            </button>
          </div>

          {tab === "overview" ? (
            <MatchOverviewTab latestMatch={latestMatch} matches={matches} recommendation={recommendation} />
          ) : tab === "optimization" ? (
            <ResumeOptimizationTab
              optimization={optimization}
              loading={optimizationLoading}
              error={optimizationError}
              onRegenerate={regenerateOptimization}
              jobTitle={latestMatch.job_title}
            />
          ) : (
            <TailoredResumeTab
              tailoredResume={tailoredResume}
              tailoredHistory={tailoredHistory}
              selectedVersion={selectedTailoredVersion}
              onSelectPrevious={selectPreviousTailoredResume}
              onDownloadVersion={async (version, filename) => {
                try {
                  await downloadTailoredResume(latestMatch.id, filename, version);
                } catch {
                  setTailoredResumeError("Download failed for this saved version.");
                }
              }}
              loading={tailoredResumeLoading}
              error={tailoredResumeError}
              onRegenerate={regenerateTailoredResume}
              onDownload={handleDownload}
              downloading={downloading}
              jobTitle={latestMatch.job_title}
              companyName={latestMatch.company_name}
            />
          )}
        </>
      )}
    </Page>
  );
}

function MatchOverviewTab({ latestMatch, matches, recommendation }) {
  return (
    <>
      <div className="match-hero">
        <Gauge value={latestMatch.match_score} label="Match" size={170} />
        <div className="match-hero-text">
          <span className="eyebrow">TARGET ROLE: {latestMatch.job_title?.toUpperCase()}</span>
          <h2>{scoreHeadline(latestMatch.match_score)}</h2>
          <p>
            Your profile shows {latestMatch.match_score >= 70 ? "a strong foundation" : "room to grow"} for{" "}
            {latestMatch.company_name} · {latestMatch.job_title}.{" "}
            {latestMatch.missing_skills?.length
              ? `Focus on ${latestMatch.missing_skills.slice(0, 2).join(" and ")} to close the biggest gaps.`
              : "Keep reinforcing what you already have."}
          </p>
        </div>
      </div>

      <div className="match-columns">
        <SkillColumn tone="ok" heading="✓ Strong Skills" items={latestMatch.matched_skills} emptyText="No strong matches yet" />
        <SkillColumn tone="warn" heading="⚠ Needs Improvement" items={latestMatch.skills_to_improve} emptyText="Nothing here — good signal" />
        <SkillColumn tone="bad" heading="⛒ Skill Gaps" items={latestMatch.missing_skills} emptyText="No missing required skills" />
      </div>

      <div className="two-column">
        <Card title="Match history" subtitle="Each comparison stays tied to its resume and target job.">
          {matches.length <= 1 ? (
            <p className="muted">This is your only match so far.</p>
          ) : (
            <div className="item-list">
              {matches.map((match) => (
                <div className="item-row" key={match.id}>
                  <div>
                    <strong>{match.company_name} · {match.job_title}</strong>
                    <span>{match.resume_title} · {new Date(match.created_at).toLocaleDateString()}</span>
                  </div>
                  <strong className="score-inline">{Math.round(match.match_score)}%</strong>
                </div>
              ))}
            </div>
          )}
        </Card>

        <div className="ai-recommend-card">
          <div className="ai-badge">AI</div>
          <h4>AI RECOMMENDATION CARD</h4>
          <p>{recommendation}</p>
        </div>
      </div>
    </>
  );
}

function SkillColumn({ tone, heading, items, emptyText }) {
  return (
    <div className={`match-col ${tone}`}>
      <h4>{heading}</h4>
      <ul>
        {items?.length ? items.map((item, index) => <li key={index}>{item}</li>) : <li>{emptyText}</li>}
      </ul>
    </div>
  );
}

function ResumeOptimizationTab({ optimization, loading, error, onRegenerate, jobTitle }) {
  if (loading) {
    return (
      <Card>
        <div className="loading">
          <Spinner />
        </div>
      </Card>
    );
  }

  return (
    <>
      <ErrorBox>{error}</ErrorBox>

      {!optimization ? (
        <Card>
          <p className="muted">Preparing your resume optimization report…</p>
        </Card>
      ) : (
        <>
          <div className="gap-score">
            <Gauge value={optimization.ats_keyword_score} size={100} stroke={10} />
            <div>
              <span>ATS KEYWORD MATCH SCORE</span>
              <strong style={{ fontSize: 16, display: "block", margin: "6px 0 4px", color: "#fff" }}>
                For {jobTitle}
              </strong>
              <p>{optimization.summary}</p>
            </div>
          </div>

          <div className="match-columns" style={{ gridTemplateColumns: "1fr 1fr" }}>
            <SkillColumn
              tone="bad"
              heading="⚠ Missing Keywords"
              items={optimization.missing_keywords}
              emptyText="None found — good coverage"
            />
            <SkillColumn
              tone="ok"
              heading="✓ Already Strong"
              items={optimization.strong_points}
              emptyText="Add more detail to build strengths"
            />
          </div>

          <Card
            title="Suggested resume rewrites"
            subtitle="Grounded in your resume — quantify these with real numbers where you can."
          >
            <div className="item-list">
              {(optimization.bullet_suggestions || []).map((bullet, index) => (
                <div key={index} style={{ padding: "14px 2px", borderBottom: "1px solid var(--line)" }}>
                  <div style={{ fontSize: 9, color: "#8B96AD", textTransform: "uppercase", letterSpacing: .5, marginBottom: 4 }}>
                    Original
                  </div>
                  <p style={{ margin: "0 0 8px", fontSize: 11, color: "#8B96AD" }}>{bullet.original_bullet}</p>

                  <div style={{ fontSize: 9, color: "#22D3EE", textTransform: "uppercase", letterSpacing: .5, marginBottom: 4 }}>
                    Improved
                  </div>
                  <p style={{ margin: "0 0 8px", fontSize: 11.5, color: "#F1F5FB", fontWeight: 600 }}>
                    {bullet.improved_bullet}
                  </p>

                  <Pill tone="ok">{bullet.reason}</Pill>
                </div>
              ))}
            </div>
          </Card>

          <button className="button ghost" style={{ marginTop: 14 }} onClick={onRegenerate}>
            ↻ Regenerate suggestions
          </button>
        </>
      )}
    </>
  );
}

function scoreHeadline(score) {
  if (score >= 80) return "An excellent match — you're ready to apply.";
  if (score >= 60) return "A strong match with identified areas for development.";
  if (score >= 40) return "A moderate match. A few focused improvements will help.";
  return "An early-stage match. Building core skills will help most.";
}

function buildRecommendation(latestMatch) {
  const gaps = [...(latestMatch.missing_skills || []), ...(latestMatch.skills_to_improve || [])];

  if (!gaps.length) {
    return "Based on your current profile, you're well aligned with this role. Keep practicing interview questions to stay sharp.";
  }

  const topGaps = gaps.slice(0, 2);
  return (
    `Based on your current gaps, we recommend a targeted ${topGaps.join(" and ")} learning plan. ` +
    `These are essential for a strong ${latestMatch.job_title} application — check Skill Gaps for a full breakdown and course links.`
  );
}

function TailoredResumeTab({ tailoredResume, tailoredHistory, selectedVersion, onSelectPrevious, onDownloadVersion, loading, error, onRegenerate, onDownload, downloading, jobTitle, companyName }) {
  if (loading) {
    return (
      <Card>
        <div className="loading"><Spinner /></div>
      </Card>
    );
  }

  return (
    <>
      <ErrorBox>{error}</ErrorBox>

      {!tailoredResume ? (
        <Card>
          <p className="muted">Preparing your tailored resume…</p>
        </Card>
      ) : (
        <>
          <div className="target-banner">
            <div>
              <span>MASTER RESUME → TAILORED FOR</span>
              <h3>{jobTitle} at {companyName}</h3>
              <p>{tailoredResume.tailoring_notes}</p>
            </div>
            <button className="button primary" disabled={downloading} onClick={onDownload}>
              {downloading ? <Spinner /> : "⬇ Download as Word"}
            </button>
          </div>

          <Card title={tailoredResume.full_name} subtitle={tailoredResume.contact_line}>
            {tailoredResume.professional_summary && (
              <div style={{ marginBottom: 18 }}>
                <h4 className="tr-heading">Professional Summary</h4>
                <p className="tr-body">{tailoredResume.professional_summary}</p>
              </div>
            )}

            {tailoredResume.key_skills?.length > 0 && (
              <div style={{ marginBottom: 18 }}>
                <h4 className="tr-heading">Key Skills</h4>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {tailoredResume.key_skills.map((skill, i) => <Pill tone="ok" key={i}>{skill}</Pill>)}
                </div>
              </div>
            )}

            {tailoredResume.work_experience?.length > 0 && (
              <div style={{ marginBottom: 18 }}>
                <h4 className="tr-heading">Experience</h4>
                {tailoredResume.work_experience.map((job, i) => (
                  <div key={i} style={{ marginBottom: 14 }}>
                    <strong className="tr-body" style={{ display: "block" }}>
                      {job.title} — {job.organization} <span className="muted">({job.duration})</span>
                    </strong>
                    <ul style={{ margin: "6px 0 0", paddingLeft: 18 }}>
                      {(job.bullets || []).map((bullet, j) => (
                        <li key={j} className="tr-body">{bullet}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}

            {tailoredResume.education?.length > 0 && (
              <div style={{ marginBottom: 18 }}>
                <h4 className="tr-heading">Education</h4>
                <ul style={{ margin: 0, paddingLeft: 18 }}>
                  {tailoredResume.education.map((line, i) => <li key={i} className="tr-body">{line}</li>)}
                </ul>
              </div>
            )}

            {tailoredResume.keywords_incorporated?.length > 0 && (
              <div>
                <h4 className="tr-heading">Keywords worked in for this role</h4>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {tailoredResume.keywords_incorporated.map((k, i) => <Pill tone="neutral" key={i}>{k}</Pill>)}
                </div>
              </div>
            )}
          </Card>

          <button className="button ghost" style={{ marginTop: 14 }} onClick={onRegenerate}>
            ↻ Regenerate tailored resume
          </button>

          <Card title="Previously Generated" subtitle="Saved tailored versions for this job match. Your master resume is never replaced.">
            {tailoredHistory?.length ? (
              <div className="tailored-history-list">
                {[...tailoredHistory].reverse().map((item) => (
                  <div className={`tailored-history-item ${selectedVersion === item.version ? "current" : ""}`} key={item.version}>
                    <div className="tailored-history-info">
                      <strong>Version {item.version}</strong>
                      <span>{item.company_name} · {item.job_title}</span>
                      <small>{item.generated_at ? new Date(item.generated_at).toLocaleString() : "Previously generated"}</small>
                    </div>
                    <div className="tailored-history-actions">
                      <button className="button ghost small" onClick={() => onSelectPrevious(item)}>
                        {selectedVersion === item.version ? "Viewing" : "View"}
                      </button>
                      <button
                        className="button ghost small"
                        onClick={() => {
                          const filename = `Tailored_Resume_${item.company_name || "target"}_${item.job_title || "role"}_v${item.version}.docx`.replace(/\s+/g, "_");
                          onDownloadVersion(item.version, filename);
                        }}
                      >
                        Download
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="muted">No previous versions yet. Regenerate this resume to create another saved version.</p>
            )}
          </Card>
        </>
      )}
    </>
  );
}
