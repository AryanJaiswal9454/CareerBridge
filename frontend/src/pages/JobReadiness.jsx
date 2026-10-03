import { useEffect, useState } from "react";
import { getProfile } from "../api/profile";
import { getResumes } from "../api/resumes";
import { getJobDescriptions } from "../api/careers";
import { getMatches } from "../api/matching";
import { getRoadmaps } from "../api/roadmap";
import { getInterviews } from "../api/interviews";
import { Page } from "./Dashboard";
import { Card } from "../components/Ui";

const DATA_SOURCES = ["profile", "resumes", "jobs", "matches", "roadmaps", "interviews"];

export default function JobReadiness() {
  const [data, setData] = useState({});

  useEffect(() => {
    Promise.allSettled([
      getProfile(),
      getResumes(),
      getJobDescriptions(),
      getMatches(),
      getRoadmaps(),
      getInterviews(),
    ]).then((results) => {
      const merged = {};
      DATA_SOURCES.forEach((key, index) => {
        merged[key] = results[index].status === "fulfilled" ? results[index].value : null;
      });
      setData(merged);
    });
  }, []);

  const latestMatch = data.matches?.[0];

  const checks = [
    ["Profile", !!data.profile?.career_goal, "Define your target role", "/profile"],
    ["Resume", !!data.resumes?.some((r) => r.has_ai_analysis), "Resume analyzed", "/resume"],
    ["Exact JD", !!data.jobs?.some((j) => j.ai_analysis), "Target JD analyzed", "/job-description"],
    ["Match", !!latestMatch, "Match score created", "/matching"],
    ["Roadmap", !!data.roadmaps?.length, "Preparation plan created", "/roadmap"],
    ["Interview", !!data.interviews?.length, "Practice started", "/interview"],
  ];

  const completedCount = checks.filter(([, done]) => done).length;
  const readinessPercent = Math.round((completedCount / checks.length) * 100);

  return (
    <Page title="Job Readiness" subtitle="A simple final checklist across the entire CareerBridge journey.">
      <div className="readiness-hero">
        <div>
          <span>READINESS</span>
          <strong>{readinessPercent}%</strong>
          <p>{completedCount} of {checks.length} milestones complete</p>
        </div>
        <div className="readiness-bar">
          <i style={{ width: `${readinessPercent}%` }} />
        </div>
      </div>

      <div className="check-grid">
        {checks.map(([title, done, description, to], index) => (
          <Card key={title} className={done ? "complete-card" : ""}>
            <div className="check-card">
              <div className="big-check">{done ? "✓" : `0${index + 1}`}</div>
              <div>
                <span>{title}</span>
                <h3>{description}</h3>
                <p>{done ? "Completed — keep going." : "This step is still needed."}</p>
              </div>
              <a className="button ghost small" href={to}>
                Open
              </a>
            </div>
          </Card>
        ))}
      </div>

      {latestMatch && (
        <Card className="section-card" title="Current readiness signal">
          <div className="readiness-summary">
            <strong>{Math.round(latestMatch.match_score)}%</strong>
            <p>
              Latest resume-to-JD match for <b>{latestMatch.company_name} · {latestMatch.job_title}</b>.
              Use Skill Gap and Roadmap to raise this signal.
            </p>
          </div>
        </Card>
      )}
    </Page>
  );
}
