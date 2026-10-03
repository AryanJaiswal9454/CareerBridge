import { useEffect, useRef, useState } from "react";
import { getJobDescriptions, uploadJobDescription, analyzeJobDescription } from "../api/careers";
import { Card, ErrorBox, SuccessBox, Empty, Spinner } from "../components/Ui";
import { Page } from "./Dashboard";

const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"];

export default function JobDescription() {
  const [jobs, setJobs] = useState([]);
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [paste, setPaste] = useState("");
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");
  const fileInput = useRef();
  const loadVersion = useRef(0);

  async function load() {
    const version = ++loadVersion.current;
    const data = await getJobDescriptions();
    if (version === loadVersion.current) {
      setJobs(Array.isArray(data) ? data : []);
    }
    return data;
  }

  useEffect(() => {
    load();
  }, []);

  function chooseFile(candidate) {
    if (!candidate) return;
    const isAllowed = ALLOWED_EXTENSIONS.some((ext) =>
      candidate.name.toLowerCase().endsWith(ext)
    );
    if (isAllowed) {
      setFile(candidate);
    } else {
      setError("Only PDF, DOCX and TXT JD files are supported.");
    }
  }

  async function save() {
    setBusy(true);
    setError("");
    setOk("");
    try {
      if (!company.trim() || !role.trim()) {
        throw new Error("Company name and job title are required.");
      }
      if (!file && !paste.trim()) {
        throw new Error("Paste the exact JD or upload a file.");
      }

      const formData = new FormData();
      formData.append("company_name", company.trim());
      formData.append("job_title", role.trim());
      if (file) {
        formData.append("file", file);
      } else {
        formData.append("description", paste.trim());
      }

      await uploadJobDescription(formData);
      setOk("Exact job description saved successfully.");
      setCompany("");
      setRole("");
      setPaste("");
      setFile(null);
      await load();
    } catch (err) {
      setError(err.response?.data?.error || err.message || "JD save failed.");
    } finally {
      setBusy(false);
    }
  }

  async function analyze(id) {
    setError("");
    try {
      const result = await analyzeJobDescription(id);
      setJobs((current) => current.map((job) =>
        String(job.id) === String(id)
          ? { ...job, ai_analysis: result.analysis || job.ai_analysis }
          : job
      ));
      setOk("JD analysis completed.");
    } catch (err) {
      setError(err.response?.data?.details || err.response?.data?.error || "JD analysis failed.");
    }
  }

  return (
    <Page
      title="Job Description"
      subtitle="Target the exact company role. Paste the JD or drag and drop the original PDF, DOCX or TXT file."
    >
      <div className="target-banner">
        <div>
          <span>WHY EXACT JD?</span>
          <h3>Generic role templates are not enough.</h3>
          <p>
            CareerBridge uses the company-provided description as the source of
            truth for matching, gaps, roadmap and interview preparation.
          </p>
        </div>
        <div className="target-badge">
          SOURCE
          <br />
          <b>EXACT JD</b>
        </div>
      </div>

      <Card title="Add target job" subtitle="Company and role identify the target; the description is the evidence.">
        <ErrorBox>{error}</ErrorBox>
        <SuccessBox>{ok}</SuccessBox>

        <div className="form-grid">
          <label>
            Company name
            <input value={company} onChange={(e) => setCompany(e.target.value)} placeholder="e.g. TCS" />
          </label>
          <label>
            Job title
            <input value={role} onChange={(e) => setRole(e.target.value)} placeholder="e.g. Data Analyst" />
          </label>
        </div>

        <div
          className="upload-zone large"
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
          <div className="upload-icon">⇧</div>
          <strong>{file ? file.name : "Drag & drop the company JD"}</strong>
          <span>{file ? "Ready to upload" : "or click to select a PDF, DOCX or TXT file"}</span>
          <small>FILE UPLOAD</small>
        </div>

        <div className="or">
          <span>OR PASTE THE EXACT JD</span>
        </div>

        <textarea
          className="paste-box"
          rows="12"
          value={paste}
          onChange={(e) => {
            setPaste(e.target.value);
            setFile(null);
          }}
          placeholder="Paste the exact job description copied from the company's careers page or job posting…"
        />

        <button className="button primary" disabled={busy} onClick={save}>
          {busy ? <><Spinner /> Saving…</> : "Save target job"}
        </button>
      </Card>

      <Card className="section-card" title="Saved target jobs" subtitle="Analyze a saved JD before running a match.">
        {!jobs.length ? (
          <Empty
            icon="▣"
            title="No target job yet"
            text="Add the company JD above. It becomes the source of truth for the rest of your journey."
          />
        ) : (
          <div className="item-list">
            {jobs.map((job) => (
              <div className="item-row" key={job.id}>
                <div>
                  <strong>{job.company_name} · {job.job_title}</strong>
                  <span>
                    {job.source_type === "file" ? "Uploaded file" : "Pasted text"} ·{" "}
                    {job.ai_analysis ? "Analysis ready" : "Awaiting analysis"}
                  </span>
                </div>
                <div className="row-actions">
                  {job.ai_analysis ? (
                    <span className="badge success">Analyzed</span>
                  ) : (
                    <button className="button small primary" onClick={() => analyze(job.id)}>
                      Analyze JD
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </Page>
  );
}
