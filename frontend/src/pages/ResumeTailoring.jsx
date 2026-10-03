import { useEffect, useState } from "react";
import { getResumes } from "../api/resumes";
import { getJobDescriptions } from "../api/careers";
import {
  getMatches,
  matchResumeToJob,
  getTailoredResume,
  getResumeTemplates,
  downloadTailoredResume,
} from "../api/matching";
import {
  Card,
  ErrorBox,
  SuccessBox,
  Empty,
  Spinner,
  Pill,
} from "../components/Ui";
import { Page } from "./Dashboard";


const DEFAULT_TEMPLATES = [
  {
    key: "aryan_ats",
    name: "Aryan ATS",
    description:
      "Based on the uploaded one-column ATS-friendly resume format.",
    recommended: true,
  },
  {
    key: "classic_ats",
    name: "Classic ATS",
    description:
      "Traditional professional single-column format.",
    recommended: false,
  },
  {
    key: "modern_professional",
    name: "Modern Professional",
    description:
      "Clean modern layout while remaining ATS readable.",
    recommended: false,
  },
  {
    key: "compact_ats",
    name: "Compact ATS",
    description:
      "Space-efficient format for concise one-page resumes.",
    recommended: false,
  },
];


const TEMPLATE_PREVIEWS = {
  aryan_ats: {
    name: "ARYAN JAISWAL",
    contact: "Noida, Uttar Pradesh  |  +91 6389766905",
    summary:
      "Entry-level Software Developer with hands-on experience in Python, Django, AI/ML and data-focused applications.",
    skills: "Python • Django • SQL • MySQL • AI/ML",
    experience: "Python Full-Stack Developer Trainee",
    project: "CareerBridge AI",
  },

  classic_ats: {
    name: "ARYAN JAISWAL",
    contact: "Noida, Uttar Pradesh  |  +91 6389766905",
    summary:
      "Software developer focused on Python, Django, databases and practical AI applications.",
    skills: "Python • Django • SQL • JavaScript",
    experience: "Professional Experience",
    project: "UPI Fraud Detection",
  },

  modern_professional: {
    name: "Aryan Jaiswal",
    contact: "Python Developer  |  Noida, India",
    summary:
      "Building practical full-stack and AI-powered applications using Python and modern development tools.",
    skills: "Python  Django  SQL  AI/ML",
    experience: "Experience",
    project: "CareerBridge AI",
  },

  compact_ats: {
    name: "ARYAN JAISWAL",
    contact: "Noida, India  |  +91 6389766905",
    summary:
      "Python developer with experience in Django, SQL, AI/ML and application development.",
    skills: "Python • Django • SQL • MySQL • Git",
    experience: "Experience",
    project: "UPI Fraud Detection",
  },
};


export default function ResumeTailoring() {
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [matches, setMatches] = useState([]);
  const [templates, setTemplates] = useState(DEFAULT_TEMPLATES);

  const [resumeId, setResumeId] = useState("");
  const [jobId, setJobId] = useState("");
  const [selectedTemplate, setSelectedTemplate] =
    useState("aryan_ats");

  const [tailored, setTailored] = useState(null);
  const [selectedVersion, setSelectedVersion] = useState(null);

  const [busy, setBusy] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const [error, setError] = useState("");
  const [ok, setOk] = useState("");


  async function load() {
    try {
      const [r, j, m, t] = await Promise.all([
        getResumes(),
        getJobDescriptions(),
        getMatches(),
        getResumeTemplates().catch(() => DEFAULT_TEMPLATES),
      ]);

      const rr = Array.isArray(r) ? r : [];
      const jj = Array.isArray(j) ? j : [];
      const mm = Array.isArray(m) ? m : [];
      const tt = Array.isArray(t) && t.length
        ? t
        : DEFAULT_TEMPLATES;

      setResumes(rr);
      setJobs(jj);
      setMatches(mm);
      setTemplates(tt);

      if (!resumeId) {
        const ready = rr.find((x) => x.has_ai_analysis);

        if (ready) {
          setResumeId(String(ready.id));
        }
      }

      if (!jobId) {
        const ready = jj.find((x) => !!x.ai_analysis);

        if (ready) {
          setJobId(String(ready.id));
        }
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to load your resumes and target jobs."
      );
    }
  }


  useEffect(() => {
    load();
  }, []);


  const selectedResume = resumes.find(
    (r) => String(r.id) === String(resumeId)
  );

  const selectedJob = jobs.find(
    (j) => String(j.id) === String(jobId)
  );


  const currentMatch = matches.find(
    (m) =>
      String(m.resume_id) === String(resumeId) &&
      String(m.job_id) === String(jobId)
  );


  const history = Array.isArray(tailored?.history)
    ? [...tailored.history].reverse()
    : [];


  async function getOrCreateMatch() {
    let match = matches.find(
      (m) =>
        String(m.resume_id) === String(resumeId) &&
        String(m.job_id) === String(jobId)
    );

    if (!match) {
      const result = await matchResumeToJob(
        resumeId,
        jobId
      );

      match = {
        ...result,
        id: result.match_id,
      };

      setMatches((current) => [match, ...current]);
    }

    return match;
  }


  async function loadSavedVersion(matchId) {
    setError("");
    setOk("");
    setBusy(true);

    try {
      const result = await getTailoredResume(
        matchId,
        false
      );

      setTailored(result);

      setSelectedVersion(
        result.current_version ||
          result.history?.at(-1)?.version ||
          1
      );

      if (result.selected_template) {
        setSelectedTemplate(result.selected_template);
      }

      setOk(
        "Saved job-specific resume loaded from your CareerBridge history."
      );
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to load the saved tailored resume."
      );
    } finally {
      setBusy(false);
    }
  }


  async function generate(forceRefresh = true) {
    setError("");
    setOk("");
    setBusy(true);

    try {
      if (!selectedResume || !selectedJob) {
        throw new Error(
          "Choose a resume and target JD first."
        );
      }

      if (!selectedResume.has_ai_analysis) {
        throw new Error(
          "Analyze the selected resume first."
        );
      }

      if (!selectedJob.ai_analysis) {
        throw new Error(
          "Analyze the selected job description first."
        );
      }

      const match = await getOrCreateMatch();

      const result = await getTailoredResume(
        match.id,
        forceRefresh
      );

      setTailored({
        ...result,
        selected_template: selectedTemplate,
      });

      setSelectedVersion(
        result.current_version ||
          result.history?.at(-1)?.version ||
          1
      );

      setOk(
        forceRefresh
          ? "New job-specific resume version generated and saved."
          : "Saved job-specific resume loaded."
      );
    } catch (err) {
      setError(
        err.response?.data?.details ||
          err.response?.data?.error ||
          err.message ||
          "Unable to generate the job-specific resume."
      );
    } finally {
      setBusy(false);
    }
  }


  function selectedData() {
    if (!tailored) {
      return null;
    }

    const found = tailored.history?.find(
      (item) =>
        Number(item.version) === Number(selectedVersion)
    );

    return found?.data || tailored;
  }


  async function download(version = null) {
    const match = matches.find(
      (m) =>
        String(m.resume_id) === String(resumeId) &&
        String(m.job_id) === String(jobId)
    );

    if (!match) {
      return;
    }

    setDownloading(true);
    setError("");

    try {
      const versionSuffix = version
        ? `_v${version}`
        : "";

      const safeCompany = (
        selectedJob?.company_name || "target"
      ).replace(/\s+/g, "_");

      const safeRole = (
        selectedJob?.job_title || "role"
      ).replace(/\s+/g, "_");

      await downloadTailoredResume(
        match.id,
        `Tailored_Resume_${safeCompany}_${safeRole}${versionSuffix}.docx`,
        version,
        selectedTemplate
      );
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Download failed."
      );
    } finally {
      setDownloading(false);
    }
  }


  function changeResume(value) {
    setResumeId(value);
    setTailored(null);
    setSelectedVersion(null);
    setOk("");
  }


  function changeJob(value) {
    setJobId(value);
    setTailored(null);
    setSelectedVersion(null);
    setOk("");
  }


  const selected = selectedData();

  const atsReport =
    selected?.ats_report ||
    tailored?.ats_report ||
    null;

  const beforeScore = Number(
    atsReport?.comparison?.before ??
      atsReport?.before?.score ??
      0
  );

  const afterScore = Number(
    atsReport?.comparison?.after ??
      atsReport?.after?.score ??
      0
  );

  const improvement = Number(
    atsReport?.comparison?.improvement ??
      afterScore - beforeScore
  );

  const hasAts =
    Boolean(atsReport) &&
    (
      atsReport.comparison ||
      atsReport.before ||
      atsReport.after
    );


  return (
    <Page
      title="Job-Specific Resume"
      subtitle="Keep one master resume and create a truthful, ATS-friendly version for every exact target role."
    >

      {/* =====================================================
          STEP 1
      ====================================================== */}

      <Card
        title="1. Choose your master resume and target job"
        subtitle="Your master resume is never overwritten. Every generated job-specific version is saved separately."
      >

        <ErrorBox>{error}</ErrorBox>
        <SuccessBox>{ok}</SuccessBox>

        <div className="form-grid">

          <label>
            Master Resume

            <select
              value={resumeId}
              onChange={(e) =>
                changeResume(e.target.value)
              }
            >
              <option value="">
                Choose analyzed resume
              </option>

              {resumes.map((r) => (
                <option
                  key={r.id}
                  value={r.id}
                >
                  {r.title}
                  {r.has_ai_analysis
                    ? " · analyzed"
                    : " · analyze first"}
                </option>
              ))}
            </select>
          </label>


          <label>
            Exact Company JD

            <select
              value={jobId}
              onChange={(e) =>
                changeJob(e.target.value)
              }
            >
              <option value="">
                Choose analyzed JD
              </option>

              {jobs.map((j) => (
                <option
                  key={j.id}
                  value={j.id}
                >
                  {j.company_name} · {j.job_title}
                  {j.ai_analysis
                    ? " · analyzed"
                    : " · analyze first"}
                </option>
              ))}
            </select>
          </label>

        </div>

      </Card>


      {/* =====================================================
          STEP 2 — TEMPLATE SELECTION
      ====================================================== */}

      <Card
        className="section-card"
        title="2. Choose your resume template"
        subtitle="The content stays the same; the selected template controls the final document layout."
      >

        <div className="resume-template-grid">

          {templates.map((template) => {
            const preview =
              TEMPLATE_PREVIEWS[template.key] ||
              TEMPLATE_PREVIEWS.aryan_ats;

            const isSelected =
              selectedTemplate === template.key;

            return (
              <button
                type="button"
                key={template.key}
                className={`resume-template-card ${
                  isSelected ? "selected" : ""
                }`}
                onClick={() =>
                  setSelectedTemplate(template.key)
                }
              >

                <div
                  className={`resume-mini-preview template-${template.key}`}
                >

                  <div className="mini-resume-name">
                    {preview.name}
                  </div>

                  <div className="mini-resume-contact">
                    {preview.contact}
                  </div>

                  <div className="mini-resume-section">
                    PROFESSIONAL SUMMARY
                  </div>

                  <div className="mini-resume-text">
                    {preview.summary}
                  </div>

                  <div className="mini-resume-section">
                    TECHNICAL SKILLS
                  </div>

                  <div className="mini-resume-text">
                    {preview.skills}
                  </div>

                  <div className="mini-resume-section">
                    EXPERIENCE
                  </div>

                  <div className="mini-resume-bold">
                    {preview.experience}
                  </div>

                  <div className="mini-resume-lines">
                    <span />
                    <span />
                  </div>

                  <div className="mini-resume-section">
                    PROJECTS
                  </div>

                  <div className="mini-resume-bold">
                    {preview.project}
                  </div>

                  <div className="mini-resume-lines">
                    <span />
                    <span />
                  </div>

                  <div className="mini-resume-section">
                    EDUCATION
                  </div>

                  <div className="mini-resume-lines">
                    <span />
                    <span />
                  </div>

                </div>


                <div className="template-card-content">

                  <strong>
                    {template.name}
                  </strong>

                  <span>
                    {template.description}
                  </span>

                  {template.recommended && (
                    <em>
                      Recommended
                    </em>
                  )}

                </div>

              </button>
            );
          })}

        </div>

      </Card>


      {/* =====================================================
          STEP 3 — GENERATE
      ====================================================== */}

      <Card
        className="section-card"
        title="3. Generate"
        subtitle="CareerBridge will tailor the content and then re-check its ATS compatibility."
      >

        <div className="generate-row">

          <button
            className="button primary"
            disabled={
              busy ||
              !resumeId ||
              !jobId
            }
            onClick={() =>
              generate(true)
            }
          >
            {busy ? (
              <>
                <Spinner />
                Working…
              </>
            ) : (
              "Generate tailored resume →"
            )}
          </button>


          {currentMatch?.has_tailored_resume && (
            <button
              className="button ghost"
              disabled={busy}
              onClick={() =>
                loadSavedVersion(
                  currentMatch.id
                )
              }
            >
              Load previously generated
            </button>
          )}

        </div>

      </Card>


      {/* =====================================================
          ATS SCORE
      ====================================================== */}

      {hasAts && (
        <Card
          className="section-card ats-improvement-card"
          title="ATS improvement"
          subtitle="Deterministic checks compare the source resume with the generated version."
        >

          <div className="ats-score-grid">

            <div className="ats-score-card">
              <span>Before</span>

              <strong className="ats-score-value">
                {beforeScore}
              </strong>

              <small>
                ATS score
              </small>
            </div>


            <div className="ats-score-arrow">
              →
            </div>


            <div className="ats-score-card">
              <span>After</span>

              <strong className="ats-score-value">
                {afterScore}
              </strong>

              <small>
                ATS score
              </small>
            </div>


            <div
              className={`ats-score-card improvement ${
                improvement < 0
                  ? "negative"
                  : improvement > 0
                  ? "positive"
                  : "neutral"
              }`}
            >

              <span>
                {improvement > 0
                  ? "Improvement"
                  : improvement < 0
                  ? "Change"
                  : "No change"}
              </span>

              <strong className="ats-score-value">
                {improvement > 0
                  ? `+${improvement}`
                  : improvement}
              </strong>

              <small>
                points
              </small>

            </div>

          </div>


          {improvement < 0 && (
            <div className="ats-warning">
              The generated version currently scores lower than
              the source resume. Review the missing keywords and
              resume content before downloading it.
            </div>
          )}

        </Card>
      )}


      {/* =====================================================
          HISTORY
      ====================================================== */}

      {tailored && (
        <Card
          className="section-card"
          title="Previously Generated"
          subtitle="Every tailored version is stored against this exact resume + company JD combination."
        >

          {history.length ? (
            <div className="item-list">

              {history.map((item) => (
                <div
                  className="item-row"
                  key={item.version}
                >

                  <div>
                    <strong>
                      Version {item.version} ·{" "}
                      {item.company_name} ·{" "}
                      {item.job_title}
                    </strong>

                    <span>
                      {new Date(
                        item.generated_at
                      ).toLocaleString()}{" "}
                      · {item.resume_title}
                    </span>
                  </div>


                  <div
                    style={{
                      display: "flex",
                      gap: 8,
                    }}
                  >

                    <button
                      className="button ghost small"
                      onClick={() =>
                        setSelectedVersion(
                          item.version
                        )
                      }
                    >
                      View
                    </button>

                    <button
                      className="button ghost small"
                      disabled={downloading}
                      onClick={() =>
                        download(item.version)
                      }
                    >
                      Download
                    </button>

                  </div>

                </div>
              ))}

            </div>
          ) : (
            <p className="muted">
              No previous versions are stored yet.
            </p>
          )}

        </Card>
      )}


      {/* =====================================================
          RESUME PREVIEW
      ====================================================== */}

      {selected && (
        <Card
          className="section-card"
          title="4. Resume preview"
          subtitle="Review the tailored content before downloading the final Word document."
        >

          <div className="target-banner">

            <div>

              <span>
                MASTER RESUME → TARGET ROLE
              </span>

              <h3>
                {selectedJob?.job_title} at{" "}
                {selectedJob?.company_name}
              </h3>

              <p>
                {selected.tailoring_notes}
              </p>

              <Pill tone="ok">
                Version {selectedVersion}
              </Pill>

            </div>


            <button
              className="button primary"
              disabled={downloading}
              onClick={() =>
                download(
                  Number(selectedVersion)
                )
              }
            >
              {downloading ? (
                <Spinner />
              ) : (
                "⬇ Download ATS Word"
              )}
            </button>

          </div>


          {selected.professional_summary && (
            <ResumeSection title="Professional Summary">
              <p className="tr-body">
                {selected.professional_summary}
              </p>
            </ResumeSection>
          )}


          {selected.key_skills?.length > 0 && (
            <ResumeSection title="Technical Skills">

              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 6,
                }}
              >
                {selected.key_skills.map(
                  (skill, index) => (
                    <Pill
                      tone="ok"
                      key={index}
                    >
                      {skill}
                    </Pill>
                  )
                )}
              </div>

            </ResumeSection>
          )}


          {selected.work_experience?.length > 0 && (
            <ResumeSection title="Professional Experience">

              {selected.work_experience.map(
                (job, index) => (
                  <div
                    key={index}
                    style={{
                      marginBottom: 14,
                    }}
                  >

                    <strong className="tr-body">
                      {job.title} —{" "}
                      {job.organization}{" "}

                      <span className="muted">
                        {job.duration
                          ? `(${job.duration})`
                          : ""}
                      </span>
                    </strong>

                    <ul>
                      {(job.bullets || []).map(
                        (bullet, bulletIndex) => (
                          <li
                            className="tr-body"
                            key={bulletIndex}
                          >
                            {bullet}
                          </li>
                        )
                      )}
                    </ul>

                  </div>
                )
              )}

            </ResumeSection>
          )}


          {selected.projects?.length > 0 && (
            <ResumeSection title="Projects">

              {selected.projects.map(
                (project, index) => (
                  <div
                    key={index}
                    style={{
                      marginBottom: 14,
                    }}
                  >

                    <strong className="tr-body">
                      {project.name}
                    </strong>

                    {project.description && (
                      <p className="tr-body">
                        {project.description}
                      </p>
                    )}

                    {project.tech_stack && (
                      <p className="muted">
                        <strong>
                          Technologies:
                        </strong>{" "}
                        {project.tech_stack}
                      </p>
                    )}

                    {project.bullets?.length > 0 && (
                      <ul>
                        {project.bullets.map(
                          (bullet, bulletIndex) => (
                            <li
                              className="tr-body"
                              key={bulletIndex}
                            >
                              {bullet}
                            </li>
                          )
                        )}
                      </ul>
                    )}

                  </div>
                )
              )}

            </ResumeSection>
          )}


          {selected.education?.length > 0 && (
            <ResumeSection title="Education">

              <ul>
                {selected.education.map(
                  (item, index) => (
                    <li
                      className="tr-body"
                      key={index}
                    >
                      {item}
                    </li>
                  )
                )}
              </ul>

            </ResumeSection>
          )}


          {selected.certifications?.length > 0 && (
            <ResumeSection title="Certifications">

              <ul>
                {selected.certifications.map(
                  (item, index) => (
                    <li
                      className="tr-body"
                      key={index}
                    >
                      {item}
                    </li>
                  )
                )}
              </ul>

            </ResumeSection>
          )}


          {selected.keywords_incorporated?.length > 0 && (
            <ResumeSection title="Truthfully Incorporated JD Keywords">

              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 6,
                }}
              >

                {selected.keywords_incorporated.map(
                  (keyword, index) => (
                    <Pill
                      tone="neutral"
                      key={index}
                    >
                      {keyword}
                    </Pill>
                  )
                )}

              </div>

            </ResumeSection>
          )}

        </Card>
      )}


      {!resumes.length || !jobs.length ? (
        <Card>
          <Empty
            icon="✦"
            title="Add both sides first"
            text="Upload/analyze your master resume and exact company JD, then return here to create a job-specific version."
          />
        </Card>
      ) : null}

    </Page>
  );
}


function ResumeSection({
  title,
  children,
}) {
  return (
    <div
      style={{
        marginTop: 18,
      }}
    >
      <h4 className="tr-heading">
        {title}
      </h4>

      {children}
    </div>
  );
}