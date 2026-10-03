import { useEffect, useRef, useState } from "react";
import { getResumes, uploadResume, analyzeResume, getResumeATSScore } from "../api/resumes";
import { Card, ErrorBox, SuccessBox, Spinner, Empty, Gauge, Pill } from "../components/Ui";
import { Page } from "./Dashboard";

const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"];

export default function Resume() {
  const [items, setItems] = useState([]);
  const [title, setTitle] = useState("");
  const [paste, setPaste] = useState("");
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");
  const fileInput = useRef();
  const loadVersion = useRef(0);

  const [atsReports, setAtsReports] = useState({});
  const [atsOpenId, setAtsOpenId] = useState(null);
  const [atsBusy, setAtsBusy] = useState(null);

  async function load() {
    const version = ++loadVersion.current;
    const data = await getResumes();
    if (version === loadVersion.current) {
      setItems(Array.isArray(data) ? data : []);
    }
    return data;
  }

  useEffect(() => {
    load();
  }, []);

  function chooseFile(candidate) {
    const isAllowed = candidate && ALLOWED_EXTENSIONS.some((ext) =>
      candidate.name.toLowerCase().endsWith(ext)
    );
    if (isAllowed) {
      setFile(candidate);
    } else {
      setError("Please choose a PDF, DOCX or TXT resume.");
    }
  }

  async function save() {
    setBusy(true);
    setError("");
    setOk("");
    try {
      let fileToUpload = file;
      if (!fileToUpload && paste.trim()) {
        fileToUpload = new File([paste], "pasted_resume.txt", { type: "text/plain" });
      }
      if (!fileToUpload) {
        throw new Error("Paste your resume or select a file first.");
      }

      await uploadResume(title, fileToUpload);
      setOk("Resume uploaded successfully.");
      setPaste("");
      setFile(null);
      setTitle("");
      await load();
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Upload failed.");
    } finally {
      setBusy(false);
    }
  }

  async function analyze(id) {
    setError("");
    try {
      const result = await analyzeResume(id);
      // Update the existing row immediately. Do not race an older GET against
      // the POST response; that was causing analyzed resumes to disappear.
      setItems((current) => current.map((resume) =>
        String(resume.id) === String(id)
          ? { ...resume, has_ai_analysis: true, ai_analysis: result.analysis || resume.ai_analysis }
          : resume
      ));
      setOk("Resume analysis completed.");
    } catch (err) {
      setError(err.response?.data?.details || err.response?.data?.error || "Analysis failed.");
    }
  }

  async function checkATS(id) {
    setError("");
    setAtsBusy(id);
    try {
      const result = await getResumeATSScore(id);
      setAtsReports((prev) => ({ ...prev, [id]: result.report }));
      setAtsOpenId(id);
    } catch (err) {
      setError(err.response?.data?.details || err.response?.data?.error || "ATS check failed.");
    } finally {
      setAtsBusy(null);
    }
  }

  return (
    <Page
      title="Resume Analyzer"
      subtitle="Upload your resume or paste its text. CareerBridge extracts the evidence before matching it to a real job."
    >
      <Card className="section-card" title="Your resumes" subtitle="Analyze a resume before using it in Job Matching.">
        {!items.length ? (
          <Empty
            icon="▤"
            title="No resume yet"
            text="Add your first resume above to start the CareerBridge pipeline."
          />
        ) : (
          <div className="item-list">
            {items.map((resume) => (
              <div key={resume.id}>
                <div className="item-row">
                  <div>
                    <strong>{resume.title}</strong>
                    <span>
                      {resume.has_ai_analysis ? "AI analysis ready" : "Awaiting analysis"} ·{" "}
                      {new Date(resume.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="row-actions">
                    {resume.has_ai_analysis ? (
                      <span className="badge success">Analyzed</span>
                    ) : (
                      <button className="button small primary" onClick={() => analyze(resume.id)}>
                        Analyze resume
                      </button>
                    )}
                    <button
                      className="button small ghost"
                      disabled={atsBusy === resume.id}
                      onClick={() =>
                        atsReports[resume.id]
                          ? setAtsOpenId(atsOpenId === resume.id ? null : resume.id)
                          : checkATS(resume.id)
                      }
                    >
                      {atsBusy === resume.id ? <Spinner /> : atsReports[resume.id] ? "View ATS score" : "Check ATS score"}
                    </button>
                  </div>
                </div>

                {atsOpenId === resume.id && atsReports[resume.id] && (
                  <ATSReportPanel report={atsReports[resume.id]} />
                )}
              </div>
            ))}
          </div>
        )}
      </Card><br /><br />
      <div className="two-column">
        <Card title="Add your resume" subtitle="PDF, DOCX or TXT — or paste the full text.">
          <ErrorBox>{error}</ErrorBox>
          <SuccessBox>{ok}</SuccessBox>

          <label className="field-label">
            Resume title
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Aryan Jaiswal — Software / Data"
            />
          </label>

          <div
            className="upload-zone"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              chooseFile(e.dataTransfer.files[0]);
            }}
            onClick={() => fileInput.current.click()}
          >
            <input
              ref={fileInput}
              type="file"
              hidden
              accept=".pdf,.docx,.txt"
              onChange={(e) => chooseFile(e.target.files[0])}
            />
            <div className="upload-icon">↑</div>
            <strong>{file ? file.name : "Drop your resume here"}</strong>
            <span>{file ? `${(file.size / 1024).toFixed(0)} KB selected` : "or click to browse files"}</span>
            <small>PDF · DOCX · TXT</small>
          </div>

          <div className="or">
            <span>OR PASTE TEXT</span>
          </div>

          <textarea
            className="paste-box"
            rows="10"
            value={paste}
            onChange={(e) => {
              setPaste(e.target.value);
              setFile(null);
            }}
            placeholder="Paste the complete resume text here…"
          />

          <button className="button primary full" disabled={busy} onClick={save}>
            {busy ? <><Spinner /> Processing…</> : "Save resume"}
          </button>
        </Card>

        <Card title="What happens next" subtitle="A connected pipeline, not a static upload.">
          <div className="feature-stack">
            <Feature n="01" t="Extract" p="We read the text from your resume file or pasted content." />
            <Feature n="02" t="Analyze" p="AI identifies skills, education, experience, projects and certifications." />
            <Feature n="03" t="Match" p="Your evidence is compared with the exact target JD." />
            <Feature n="04" t="Improve" p="Skill gaps become roadmap and interview actions." />
          </div>
        </Card>
      </div>

      
    </Page>
  );
}

function ATSReportPanel({ report }) {
  return (
    <div className="ats-panel">
      <div className="ats-panel-head">
        <Gauge value={report.ats_score} size={90} stroke={9} label="ATS Score" />
        <div>
          <p>{report.improved_summary}</p>
          {report.strengths?.length > 0 && (
            <div className="ats-strengths">
              {report.strengths.map((strength, i) => (
                <Pill tone="ok" key={i}>{strength}</Pill>
              ))}
            </div>
          )}
        </div>
      </div>

      {report.issues?.length > 0 && (
        <div className="ats-issues">
          {report.issues.map((issue, i) => (
            <div className="ats-issue-row" key={i}>
              <strong>⚠ {issue.issue}</strong>
              <p>{issue.why_it_matters}</p>
              <span>Fix: {issue.fix}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Feature({ n, t, p }) {
  return (
    <div className="feature-row">
      <b>{n}</b>
      <div>
        <strong>{t}</strong>
        <p>{p}</p>
      </div>
    </div>
  );
}
