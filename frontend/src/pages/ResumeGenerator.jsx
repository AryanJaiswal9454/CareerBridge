import { useState } from "react";
import { Card, ErrorBox, SuccessBox, Spinner } from "../components/Ui";
import { Page } from "./Dashboard";
import { generateNewResume } from "../api/resumes";

const TEMPLATES = [
  {
    key: "aryan_ats",
    name: "Aryan ATS",
    description: "Clean one-column ATS format based on the master resume style.",
  },
  {
    key: "classic_ats",
    name: "Classic ATS",
    description: "Traditional professional single-column layout.",
  },
  {
    key: "modern_professional",
    name: "Modern Professional",
    description: "Modern typography with ATS-readable structure.",
  },
  {
    key: "compact_ats",
    name: "Compact ATS",
    description: "Space-efficient format for concise one-page resumes.",
  },
];

const emptyExperience = () => ({
  title: "",
  organization: "",
  duration: "",
  bullets: [""],
});

const emptyProject = () => ({
  name: "",
  description: "",
  tech_stack: "",
  bullets: [""],
});

const emptyEducation = () => ({
  degree: "",
  institution: "",
  duration: "",
  grade: "",
});

const emptyCertification = () => ({
  name: "",
  issuer: "",
  date: "",
});

const INITIAL = {
  full_name: "",
  headline: "",
  location: "",
  phone: "",
  email: "",
  linkedin: "",
  github: "",
  portfolio: "",
  professional_summary: "",
  key_skills: "",
  work_experience: [emptyExperience()],
  projects: [emptyProject()],
  education: [emptyEducation()],
  certifications: [emptyCertification()],
  template: "aryan_ats",
};

export default function ResumeGenerator() {
  const [form, setForm] = useState(INITIAL);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");
  const [generated, setGenerated] = useState(null);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function updateArray(section, index, field, value) {
    setForm((current) => ({
      ...current,
      [section]: current[section].map((item, i) =>
        i === index ? { ...item, [field]: value } : item
      ),
    }));
  }

  function updateBullet(section, itemIndex, bulletIndex, value) {
    setForm((current) => ({
      ...current,
      [section]: current[section].map((item, i) => {
        if (i !== itemIndex) return item;
        return {
          ...item,
          bullets: item.bullets.map((bullet, j) =>
            j === bulletIndex ? value : bullet
          ),
        };
      }),
    }));
  }

  function addItem(section, factory) {
    setForm((current) => ({
      ...current,
      [section]: [...current[section], factory()],
    }));
  }

  function removeItem(section, index) {
    setForm((current) => ({
      ...current,
      [section]: current[section].filter((_, i) => i !== index),
    }));
  }

  function addBullet(section, itemIndex) {
    setForm((current) => ({
      ...current,
      [section]: current[section].map((item, i) =>
        i === itemIndex
          ? { ...item, bullets: [...item.bullets, ""] }
          : item
      ),
    }));
  }

  function removeBullet(section, itemIndex, bulletIndex) {
    setForm((current) => ({
      ...current,
      [section]: current[section].map((item, i) => {
        if (i !== itemIndex) return item;
        return {
          ...item,
          bullets: item.bullets.filter((_, j) => j !== bulletIndex),
        };
      }),
    }));
  }

  function cleanPayload() {
    return {
      ...form,
      key_skills: form.key_skills
        .split(",")
        .map((x) => x.trim())
        .filter(Boolean),
      work_experience: form.work_experience
        .filter((x) => x.title.trim() || x.organization.trim())
        .map((x) => ({
          ...x,
          bullets: x.bullets.map((b) => b.trim()).filter(Boolean),
        })),
      projects: form.projects
        .filter((x) => x.name.trim())
        .map((x) => ({
          ...x,
          bullets: x.bullets.map((b) => b.trim()).filter(Boolean),
        })),
      education: form.education.filter(
        (x) => x.degree.trim() || x.institution.trim()
      ),
      certifications: form.certifications.filter(
        (x) => x.name.trim()
      ),
    };
  }

  async function submit() {
    setBusy(true);
    setError("");
    setOk("");

    try {
      const payload = cleanPayload();

      if (!payload.full_name.trim()) {
        throw new Error("Full name is required.");
      }

      if (!payload.email.trim() && !payload.phone.trim()) {
        throw new Error("Add at least an email address or phone number.");
      }

      if (!payload.key_skills.length) {
        throw new Error("Add at least one technical skill.");
      }

      if (!payload.education.length) {
        throw new Error("Add at least one education entry.");
      }

      const result = await generateNewResume(payload);
      setGenerated(result);
      setOk("Your new resume was generated and saved to Resume Analyzer.");
    } catch (err) {
      setError(
        err.response?.data?.details ||
          err.response?.data?.error ||
          err.message ||
          "Unable to generate the resume."
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <Page
      title="Generate New Resume"
      subtitle="Enter your real career information once and CareerBridge will create a structured resume using the template you choose."
    >
      <ErrorBox>{error}</ErrorBox>
      <SuccessBox>{ok}</SuccessBox>

      <Card
        title="1. Personal information"
        subtitle="Use the details you want recruiters to see on the resume."
      >
        <div className="form-grid">
          <label>Full name<input value={form.full_name} onChange={(e) => update("full_name", e.target.value)} placeholder="Aryan Jaiswal" /></label>
          <label>Target headline<input value={form.headline} onChange={(e) => update("headline", e.target.value)} placeholder="Python Developer | AI / Data Enthusiast" /></label>
          <label>Location<input value={form.location} onChange={(e) => update("location", e.target.value)} placeholder="Noida, Uttar Pradesh" /></label>
          <label>Phone<input value={form.phone} onChange={(e) => update("phone", e.target.value)} placeholder="+91 6389766905" /></label>
          <label>Email<input value={form.email} onChange={(e) => update("email", e.target.value)} placeholder="you@example.com" /></label>
          <label>LinkedIn<input value={form.linkedin} onChange={(e) => update("linkedin", e.target.value)} placeholder="linkedin.com/in/your-name" /></label>
          <label>GitHub<input value={form.github} onChange={(e) => update("github", e.target.value)} placeholder="github.com/username" /></label>
          <label>Portfolio<input value={form.portfolio} onChange={(e) => update("portfolio", e.target.value)} placeholder="yourportfolio.com" /></label>
        </div>
      </Card>

      <Card title="2. Professional summary" subtitle="2–4 sentences describing your profile, strengths and target direction.">
        <textarea className="paste-box" rows="5" value={form.professional_summary} onChange={(e) => update("professional_summary", e.target.value)} placeholder="Write a concise professional summary based only on your real experience and skills…" />
      </Card>

      <Card title="3. Technical skills" subtitle="Separate skills with commas. Do not add skills you cannot genuinely claim.">
        <input value={form.key_skills} onChange={(e) => update("key_skills", e.target.value)} placeholder="Python, Django, SQL, MySQL, Pandas, NumPy, Git" />
      </Card>

      <Card title="4. Experience" subtitle="Add internships, jobs, training or other relevant professional experience.">
        {form.work_experience.map((item, index) => (
          <div className="generator-entry" key={index}>
            <div className="generator-entry-head"><strong>Experience {index + 1}</strong>{form.work_experience.length > 1 && <button className="button small ghost" onClick={() => removeItem("work_experience", index)}>Remove</button>}</div>
            <div className="form-grid">
              <label>Job title<input value={item.title} onChange={(e) => updateArray("work_experience", index, "title", e.target.value)} placeholder="Python Developer Trainee" /></label>
              <label>Organization<input value={item.organization} onChange={(e) => updateArray("work_experience", index, "organization", e.target.value)} placeholder="Company / Institute" /></label>
              <label>Duration<input value={item.duration} onChange={(e) => updateArray("work_experience", index, "duration", e.target.value)} placeholder="Jan 2026 – Present" /></label>
            </div>
            <BulletEditor section="work_experience" index={index} item={item} updateBullet={updateBullet} addBullet={addBullet} removeBullet={removeBullet} />
          </div>
        ))}
        <button className="button ghost" onClick={() => addItem("work_experience", emptyExperience)}>+ Add experience</button>
      </Card>

      <Card title="5. Projects" subtitle="Add your strongest academic, personal, ML, data or software projects.">
        {form.projects.map((item, index) => (
          <div className="generator-entry" key={index}>
            <div className="generator-entry-head"><strong>Project {index + 1}</strong>{form.projects.length > 1 && <button className="button small ghost" onClick={() => removeItem("projects", index)}>Remove</button>}</div>
            <div className="form-grid">
              <label>Project name<input value={item.name} onChange={(e) => updateArray("projects", index, "name", e.target.value)} placeholder="CareerBridge AI" /></label>
              <label>Technology stack<input value={item.tech_stack} onChange={(e) => updateArray("projects", index, "tech_stack", e.target.value)} placeholder="Python, Django, React, MySQL, Gemini" /></label>
            </div>
            <label className="field-label">Project description<textarea rows="3" value={item.description} onChange={(e) => updateArray("projects", index, "description", e.target.value)} placeholder="What does the project do?" /></label>
            <BulletEditor section="projects" index={index} item={item} updateBullet={updateBullet} addBullet={addBullet} removeBullet={removeBullet} />
          </div>
        ))}
        <button className="button ghost" onClick={() => addItem("projects", emptyProject)}>+ Add project</button>
      </Card>

      <Card title="6. Education" subtitle="Add your degree, institution, dates and grade/CGPA where relevant.">
        {form.education.map((item, index) => (
          <div className="generator-entry" key={index}>
            <div className="generator-entry-head"><strong>Education {index + 1}</strong>{form.education.length > 1 && <button className="button small ghost" onClick={() => removeItem("education", index)}>Remove</button>}</div>
            <div className="form-grid">
              <label>Degree<input value={item.degree} onChange={(e) => updateArray("education", index, "degree", e.target.value)} placeholder="MCA, Computer Applications" /></label>
              <label>Institution<input value={item.institution} onChange={(e) => updateArray("education", index, "institution", e.target.value)} placeholder="RSMT, Varanasi" /></label>
              <label>Duration<input value={item.duration} onChange={(e) => updateArray("education", index, "duration", e.target.value)} placeholder="2024 – 2026" /></label>
              <label>Grade / CGPA<input value={item.grade} onChange={(e) => updateArray("education", index, "grade", e.target.value)} placeholder="CGPA: 8.2" /></label>
            </div>
          </div>
        ))}
        <button className="button ghost" onClick={() => addItem("education", emptyEducation)}>+ Add education</button>
      </Card>

      <Card title="7. Certifications" subtitle="Add certifications, job simulations or relevant courses.">
        {form.certifications.map((item, index) => (
          <div className="generator-entry" key={index}>
            <div className="generator-entry-head"><strong>Certification {index + 1}</strong>{form.certifications.length > 1 && <button className="button small ghost" onClick={() => removeItem("certifications", index)}>Remove</button>}</div>
            <div className="form-grid">
              <label>Certification name<input value={item.name} onChange={(e) => updateArray("certifications", index, "name", e.target.value)} placeholder="Data Analytics Job Simulation" /></label>
              <label>Issuer<input value={item.issuer} onChange={(e) => updateArray("certifications", index, "issuer", e.target.value)} placeholder="Deloitte | Forage" /></label>
              <label>Date<input value={item.date} onChange={(e) => updateArray("certifications", index, "date", e.target.value)} placeholder="2026" /></label>
            </div>
          </div>
        ))}
        <button className="button ghost" onClick={() => addItem("certifications", emptyCertification)}>+ Add certification</button>
      </Card>

      <Card title="8. Choose your template" subtitle="The information stays the same; the template controls the final document layout.">
        <div className="resume-template-grid generator-template-grid">
          {TEMPLATES.map((template) => (
            <button
              type="button"
              key={template.key}
              className={`resume-template-card ${form.template === template.key ? "selected" : ""}`}
              onClick={() => update("template", template.key)}
            >
              <div className={`resume-mini-preview template-${template.key}`}>
                <div className="mini-resume-name">ARYAN JAISWAL</div>
                <div className="mini-resume-contact">Python Developer | Noida, India</div>
                <div className="mini-resume-section">PROFESSIONAL SUMMARY</div>
                <div className="mini-resume-text">Experienced candidate profile, skills and career direction.</div>
                <div className="mini-resume-section">TECHNICAL SKILLS</div>
                <div className="mini-resume-text">Python • Django • SQL • MySQL • Git</div>
                <div className="mini-resume-section">EXPERIENCE</div>
                <div className="mini-resume-bold">Developer / Trainee</div>
                <div className="mini-resume-lines"><span /><span /></div>
                <div className="mini-resume-section">PROJECTS</div>
                <div className="mini-resume-bold">CareerBridge AI</div>
                <div className="mini-resume-lines"><span /><span /></div>
                <div className="mini-resume-section">EDUCATION</div>
                <div className="mini-resume-lines"><span /><span /></div>
              </div>
              <div className="template-card-content">
                <strong>{template.name}</strong>
                <span>{template.description}</span>
                {template.key === "aryan_ats" && <em>Recommended</em>}
              </div>
            </button>
          ))}
        </div>
      </Card>

      <Card title="9. Generate" subtitle="CareerBridge will create the DOCX, save it as a new resume and keep your existing resumes untouched.">
        <button className="button primary" disabled={busy} onClick={submit}>
          {busy ? <><Spinner /> Generating…</> : "Generate New Resume →"}
        </button>

        {generated && (
          <div className="generated-success">
            <strong>{generated.title}</strong>
            <span>Saved to Resume Analyzer as resume #{generated.resume_id}.</span>
            <a className="button ghost small" href="/resume">Open Resume Analyzer</a>
          </div>
        )}
      </Card>
    </Page>
  );
}

function BulletEditor({ section, index, item, updateBullet, addBullet, removeBullet }) {
  return (
    <div className="bullet-editor">
      <span className="field-label">Achievement / contribution bullets</span>
      {item.bullets.map((bullet, bulletIndex) => (
        <div className="bullet-input-row" key={bulletIndex}>
          <input value={bullet} onChange={(e) => updateBullet(section, index, bulletIndex, e.target.value)} placeholder="Describe what you built, improved or accomplished…" />
          {item.bullets.length > 1 && <button className="button small ghost" onClick={() => removeBullet(section, index, bulletIndex)}>×</button>}
        </div>
      ))}
      <button className="button small ghost" onClick={() => addBullet(section, index)}>+ Add bullet</button>
    </div>
  );
}
