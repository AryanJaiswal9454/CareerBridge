import json
import os
import re

from pydantic import BaseModel

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None


# Gemini model used by every AI generation helper.
# You can override this in backend/.env with:
# GEMINI_MODEL=your-model-name
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Fallback models used when the primary model is temporarily unavailable,
# rate-limited, or not available for the current project.
# You can override these in backend/.env with a comma-separated list:
# GEMINI_FALLBACK_MODELS=gemini-3.7-flash,gemini-3.6-flash,gemini-3.5-flash-lite,gemini-3.1-flash-lite
DEFAULT_FALLBACK_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

_configured_fallbacks = os.getenv("GEMINI_FALLBACK_MODELS", "")
if _configured_fallbacks.strip():
    FALLBACK_MODELS = [
        model.strip()
        for model in _configured_fallbacks.split(",")
        if model.strip()
    ]
else:
    FALLBACK_MODELS = DEFAULT_FALLBACK_MODELS

# Keep the primary model first and remove duplicates while preserving order.
GEMINI_MODELS = list(dict.fromkeys([PRIMARY_MODEL] + FALLBACK_MODELS))


SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "django",
    "flask",
    "fastapi",
    "node.js",
    "express",
    "rest api",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "gcp",
    "power bi",
    "tableau",
    "excel",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "data analysis",
    "data analytics",
    "tensorflow",
    "pytorch",
    "communication",
    "problem solving",
    "leadership",
    "figma",
    "linux",
    "api",
    "agile",
    "scrum",
]


class ResumeAnalysis(BaseModel):
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]
    certifications: list[str]


class JobAnalysis(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    experience_required: str
    education_required: str


class MCQItem(BaseModel):
    question: str
    options: list[str]
    correct_option: str
    explanation: str


class CodingItem(BaseModel):
    question: str
    starter_code: str
    sample_solution: str
    explanation: str


class ConceptualItem(BaseModel):
    question: str
    model_answer: str
    key_points: list[str]


class CourseRecommendation(BaseModel):
    title: str
    provider: str
    search_query: str
    reason: str


class CourseRecommendationList(BaseModel):
    recommendations: list[CourseRecommendation]


class CodingEvaluation(BaseModel):
    score: int
    is_correct: bool
    feedback: str
    missing_points: list[str]


class BulletSuggestion(BaseModel):
    original_bullet: str
    improved_bullet: str
    reason: str


class ResumeOptimizationResult(BaseModel):
    ats_keyword_score: int
    missing_keywords: list[str]
    strong_points: list[str]
    summary: str
    bullet_suggestions: list[BulletSuggestion]


def _skills(text):
    low = text.lower()
    found = []

    for skill in SKILLS:
        if re.search(
            r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])",
            low,
        ):
            found.append(
                skill.title()
                if skill not in {"c++", "sql", "html", "css", "gcp", "aws", "api"}
                else skill.upper()
            )

    return found


def _lines(text, words):
    out = []

    for line in text.splitlines():
        s = line.strip()

        if s and any(w in s.lower() for w in words):
            out.append(s[:220])

    return out[:10]


def fallback_resume(text):
    return {
        "skills": _skills(text),
        "education": _lines(
            text,
            [
                "education",
                "bca",
                "mca",
                "b.tech",
                "bachelor",
                "master",
                "university",
                "college",
                "degree",
            ],
        ),
        "experience": _lines(
            text,
            [
                "experience",
                "intern",
                "developer",
                "analyst",
                "engineer",
                "worked",
                "employment",
            ],
        ),
        "projects": _lines(
            text,
            [
                "project",
                "developed",
                "built",
                "application",
                "system",
            ],
        ),
        "certifications": _lines(
            text,
            [
                "certification",
                "certificate",
                "certified",
                "course",
            ],
        ),
    }


def fallback_job(text):
    low = text.lower()
    lines = text.splitlines()
    required = []
    preferred = []

    for skill in _skills(text):
        # Crude but transparent: preferred wording on nearby line
        # moves the skill to preferred.
        idx = next(
            (
                i
                for i, l in enumerate(lines)
                if skill.lower() in l.lower()
            ),
            -1,
        )

        context = (
            " ".join(lines[max(0, idx - 1) : idx + 2]).lower()
            if idx >= 0
            else low
        )

        if any(
            w in context
            for w in [
                "preferred",
                "nice to have",
                "desired",
                "advantage",
                "plus",
            ]
        ):
            preferred.append(skill)
        else:
            required.append(skill)

    exp = ""

    m = re.search(
        r"(\d+\+?\s*(?:years?|yrs?).{0,35}(?:experience|exp))",
        text,
        re.I,
    )

    if m:
        exp = m.group(1)

    edu = ""

    for line in lines:
        if any(
            w in line.lower()
            for w in [
                "bachelor",
                "master",
                "b.tech",
                "mca",
                "bca",
                "degree",
            ]
        ):
            edu = line.strip()[:220]
            break

    return {
        "required_skills": list(dict.fromkeys(required)),
        "preferred_skills": list(dict.fromkeys(preferred)),
        "experience_required": exp,
        "education_required": edu,
    }


def _gemini_error_code(exc):
    """Best-effort extraction of an HTTP/API status code from a Gemini error."""
    for attr in ("status_code", "code", "http_status"):
        value = getattr(exc, attr, None)
        if isinstance(value, int):
            return value

    text = str(exc).lower()
    for code in (429, 500, 502, 503, 504, 404):
        if str(code) in text:
            return code

    return None


def _should_try_next_model(exc):
    """Return True for errors where another Gemini model may succeed."""
    code = _gemini_error_code(exc)
    if code in {429, 500, 502, 503, 504, 404}:
        return True

    text = str(exc).lower()
    transient_terms = (
        "unavailable",
        "high demand",
        "resource_exhausted",
        "rate limit",
        "quota",
        "overloaded",
        "not found",
    )
    return any(term in text for term in transient_terms)


def _gemini_json(prompt, schema):
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        print("GEMINI ERROR: GEMINI_API_KEY is missing.")
        return None

    if genai is None:
        print(
            "GEMINI ERROR: google-genai package could not be imported."
        )
        return None

    print("GEMINI: model fallback chain =", " -> ".join(GEMINI_MODELS))

    client = genai.Client(api_key=key)
    last_error = None

    for index, model_name in enumerate(GEMINI_MODELS):
        print(f"GEMINI: attempting model = {model_name}")

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0,
                ),
            )

            if not response:
                print(
                    f"GEMINI ERROR [{model_name}]: Empty response object."
                )
                last_error = "empty response"
                continue

            if not response.text:
                print(
                    f"GEMINI ERROR [{model_name}]: Gemini returned no text."
                )
                print("Gemini response:", response)
                last_error = "empty response text"
                continue

            try:
                result = json.loads(response.text)
                print(
                    f"GEMINI: model {model_name} succeeded "
                    f"({index + 1}/{len(GEMINI_MODELS)})."
                )
                return result

            except json.JSONDecodeError as exc:
                print(
                    f"GEMINI ERROR [{model_name}]: "
                    "Response was not valid JSON."
                )
                print("JSON error:", exc)
                print("Raw Gemini response:", response.text)
                last_error = exc

                # A malformed structured response is normally a model/API
                # response problem, so let the next model try as well.
                continue

        except Exception as exc:
            last_error = exc
            code = _gemini_error_code(exc)

            print("=" * 80)
            print("GEMINI API ERROR")
            print("=" * 80)
            print("Model:", model_name)
            print("Error type:", type(exc).__name__)
            print("Status/code:", code)
            print("Error:", str(exc))
            print("=" * 80)

            if _should_try_next_model(exc) and index < len(GEMINI_MODELS) - 1:
                print(
                    "GEMINI: current model is unavailable/rate-limited; "
                    "trying the next fallback model."
                )
                continue

            # Authentication, permission, malformed-request, and other
            # non-fallback errors should not cause a long chain of requests.
            break

    print("GEMINI ERROR: all configured models failed.")
    if last_error is not None:
        print("Last Gemini error:", str(last_error))
    return None

def analyze_resume(resume_text):
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    result = _gemini_json(
        f"""
Extract only explicit resume information.

Return:
- skills
- education
- experience
- projects
- certifications

Do not invent information.

RESUME:
{resume_text}
""",
        ResumeAnalysis,
    )

    return result or fallback_resume(resume_text)


def analyze_job_description(job_text):
    if not job_text or not job_text.strip():
        raise ValueError("Job description text is empty.")

    result = _gemini_json(
        f"""
Extract only explicit job requirements.

Return:
- required_skills
- preferred_skills
- experience_required
- education_required

Do not invent information.

JOB DESCRIPTION:
{job_text}
""",
        JobAnalysis,
    )

    return result or fallback_job(job_text)


def generate_mcq_question(skill, difficulty="intermediate"):
    """Ask Gemini for one MCQ about `skill`."""

    prompt = (
        f"Create ONE multiple-choice interview question about "
        f"'{skill}' at {difficulty} level for a job candidate. "
        "Provide exactly 4 answer options (plain text, do not prefix "
        "them with A/B/C/D yourself), the correct_option as the letter "
        "A, B, C or D corresponding to its position in the options list, "
        "and a short explanation (1-2 sentences) of why that answer is "
        "correct."
    )

    return _gemini_json(prompt, MCQItem)


def generate_coding_question(skill, difficulty="intermediate"):
    """Ask Gemini for one short coding question about `skill`."""

    prompt = (
        f"Create ONE short, self-contained coding interview question "
        f"about '{skill}' for a job candidate ({difficulty} level). "
        "Include: question (1-3 sentences describing the task), "
        "starter_code (a short code skeleton the candidate would "
        "complete), sample_solution (a concise worked solution), "
        "and explanation (1-2 sentences on the approach / key idea)."
    )

    return _gemini_json(prompt, CodingItem)


def generate_conceptual_question(topic, difficulty="intermediate"):
    """
    Ask Gemini for one open-ended interview question about `topic`.
    """

    prompt = (
        f"Create ONE open-ended interview question about '{topic}' "
        f"at {difficulty} level for a job candidate. "
        "This could be a conceptual technical question or, if the "
        "topic is HR/behavioral, a standard behavioral interview "
        "question. Provide: question, model_answer (a strong example "
        "answer, 3-5 sentences), and key_points (a short list of "
        "2-4 things a strong answer should hit, for quick self-review)."
    )

    return _gemini_json(prompt, ConceptualItem)


def generate_course_recommendations(skill, count=2):
    """
    Ask Gemini for course/video recommendations for `skill`.
    """

    prompt = (
        f"Recommend {count} well-known, currently popular, high "
        f"quality YouTube tutorials or course playlists for learning "
        f"'{skill}' as a job-seeker preparing for interviews. "
        "For each, give: title (a realistic, specific video/course "
        "title), provider (the channel or platform name), "
        "search_query (a short YouTube search string likely to "
        "surface this or an equivalent video), reason (one sentence "
        "on why it's a good pick)."
    )

    result = _gemini_json(
        prompt,
        CourseRecommendationList,
    )

    if result:
        return result.get("recommendations")

    return None


def evaluate_coding_answer(
    question,
    sample_solution,
    candidate_answer,
):
    """
    Ask Gemini to grade a candidate's coding answer.
    """

    prompt = (
        "You are grading a candidate's answer to a coding interview "
        "question.\n"
        f"QUESTION:\n{question}\n\n"
        "REFERENCE SOLUTION "
        "(for grading only, do not reveal verbatim):\n"
        f"{sample_solution}\n\n"
        f"CANDIDATE ANSWER:\n{candidate_answer}\n\n"
        "Grade the candidate answer from 0-100 (score), whether it is "
        "essentially correct (is_correct), short constructive feedback "
        "(feedback), and a short list of concrete things missing or "
        "wrong (missing_points, empty list if none)."
    )

    return _gemini_json(
        prompt,
        CodingEvaluation,
    )


def _fallback_resume_optimization(
    resume_text,
    job_text,
    missing_skills,
    matched_skills,
):
    """
    Rule-based resume optimization used when Gemini is unavailable.
    Transparent and deterministic.
    """

    resume_words = set(
        re.findall(
            r"[a-zA-Z][a-zA-Z0-9+.#]{1,}",
            (resume_text or "").lower(),
        )
    )

    job_keywords = _skills(job_text or "")

    missing_keywords = [
        k
        for k in job_keywords
        if k.lower() not in resume_words
    ][:10] or list(missing_skills)[:10]

    # Find resume bullet-like lines lacking a number/metric.
    candidate_lines = [
        line.strip()
        for line in (resume_text or "").splitlines()
        if len(line.strip()) > 25
        and not re.search(r"\d", line)
    ][:3]

    bullet_suggestions = []

    for line in candidate_lines:
        bullet_suggestions.append(
            {
                "original_bullet": line[:200],
                "improved_bullet": (
                    f"{line[:160].rstrip('.')} — add a measurable "
                    "result (e.g. 'reducing X by Y%' or "
                    "'for Z users/records')."
                ),
                "reason": (
                    "Quantified bullets (with a number, %, or scale) "
                    "are more likely to pass ATS ranking and catch "
                    "a recruiter's eye."
                ),
            }
        )

    if not bullet_suggestions:
        bullet_suggestions.append(
            {
                "original_bullet": "(no clear bullet points detected)",
                "improved_bullet": (
                    "Structure achievements as: Accomplished [X] "
                    "as measured by [Y], by doing [Z]."
                ),
                "reason": (
                    "Use the X-Y-Z formula so every bullet shows "
                    "a concrete, measurable outcome."
                ),
            }
        )

    total_keywords = max(len(job_keywords), 1)
    matched_count = total_keywords - len(missing_keywords)

    ats_score = round(
        (matched_count / total_keywords) * 100
    )

    return {
        "ats_keyword_score": max(0, min(100, ats_score)),
        "missing_keywords": missing_keywords,
        "strong_points": list(matched_skills)[:6],
        "summary": (
            f"Your resume already reflects {len(matched_skills)} "
            "of the role's key skills. Adding the missing keywords "
            "below — and quantifying your bullet points — is the "
            "fastest way to raise your ATS match score."
        ),
        "bullet_suggestions": bullet_suggestions,
    }


class ATSIssue(BaseModel):
    issue: str
    why_it_matters: str
    fix: str


class ATSReport(BaseModel):
    ats_score: int
    strengths: list[str]
    issues: list[ATSIssue]
    improved_summary: str


def _fallback_ats_report(resume_text):
    """
    Rule-based, generic ATS friendliness check.
    """

    text = resume_text or ""
    lower = text.lower()
    word_count = len(text.split())

    issues = []
    strengths = []
    score = 100

    expected_sections = [
        "experience",
        "education",
        "skills",
    ]

    missing_sections = [
        s for s in expected_sections if s not in lower
    ]

    if missing_sections:
        score -= 15 * len(missing_sections)

        issues.append(
            {
                "issue": (
                    "Missing standard section header(s): "
                    f"{', '.join(missing_sections)}"
                ),
                "why_it_matters": (
                    "ATS software looks for standard section headers "
                    "to categorize your experience correctly."
                ),
                "fix": (
                    "Add a clearly labeled section for: "
                    f"{', '.join(missing_sections)}."
                ),
            }
        )
    else:
        strengths.append(
            "Has standard Experience / Education / Skills sections."
        )

    bullet_markers = (
        text.count("•")
        + text.count("- ")
        + text.count("* ")
    )

    if bullet_markers < 3:
        score -= 15

        issues.append(
            {
                "issue": "Very few bullet points detected.",
                "why_it_matters": (
                    "ATS and recruiters both scan bullet points "
                    "far more easily than dense paragraphs."
                ),
                "fix": (
                    "Convert your experience descriptions into "
                    "concise bullet points, one achievement per line."
                ),
            }
        )
    else:
        strengths.append(
            "Uses bullet points for readability."
        )

    if not re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text,
    ):
        score -= 15

        issues.append(
            {
                "issue": "No email address detected.",
                "why_it_matters": (
                    "ATS systems extract contact details automatically; "
                    "a missing email can drop your application."
                ),
                "fix": (
                    "Add a professional email address near the top "
                    "of your resume."
                ),
            }
        )
    else:
        strengths.append(
            "Email address is present and detectable."
        )

    if word_count < 150:
        score -= 15

        issues.append(
            {
                "issue": "Resume looks quite short.",
                "why_it_matters": (
                    "Very short resumes often lack the keywords "
                    "ATS systems rank against."
                ),
                "fix": (
                    "Expand on your experience with specific "
                    "responsibilities and measurable outcomes."
                ),
            }
        )

    elif word_count > 1200:
        score -= 10

        issues.append(
            {
                "issue": "Resume looks very long.",
                "why_it_matters": (
                    "Overly long resumes dilute keyword density and "
                    "are harder for recruiters to scan quickly."
                ),
                "fix": (
                    "Aim for a focused one-to-two page resume; "
                    "trim older or less relevant experience."
                ),
            }
        )

    else:
        strengths.append(
            "Resume length is in a reasonable range."
        )

    if re.search(
        r"\t{2,}|\|{2,}",
        text,
    ):
        score -= 10

        issues.append(
            {
                "issue": (
                    "Possible table or multi-column layout detected "
                    "in the extracted text."
                ),
                "why_it_matters": (
                    "Tables, columns and text boxes often get "
                    "scrambled or dropped by ATS parsers."
                ),
                "fix": (
                    "Use a single-column layout with plain text "
                    "instead of tables or graphic design elements."
                ),
            }
        )

    score = max(
        0,
        min(100, score),
    )

    return {
        "ats_score": score,
        "strengths": (
            strengths
            or [
                "Resume was readable as plain text, "
                "which is ATS-friendly."
            ]
        ),
        "issues": issues,
        "improved_summary": (
            "This is a rule-based check (structure, sections, "
            "bullets, contact info, length) rather than a full "
            "AI review. Address the issues above, then re-run "
            "this check to confirm your score improved."
        ),
    }


def generate_ats_report(resume_text):
    """
    Generic job-independent ATS-friendliness check.
    """

    prompt = (
        "You are an ATS (Applicant Tracking System) resume "
        "screening simulator. Evaluate ONLY how well this resume "
        "would survive an automated ATS parse and keyword scan — "
        "not fit for any specific job.\n\n"
        f"RESUME:\n{(resume_text or '')[:6000]}\n\n"
        "Return: ats_score (0-100), strengths (what already works "
        "well for ATS), issues (a list of concrete problems, each "
        "with issue, why_it_matters, and fix), and improved_summary "
        "(2-3 sentences of overall guidance on making this resume "
        "more ATS-friendly)."
    )

    result = _gemini_json(
        prompt,
        ATSReport,
    )

    if result:
        return result

    return _fallback_ats_report(resume_text)


def generate_resume_optimization(
    resume_text,
    job_text,
    missing_skills,
    matched_skills,
):
    """
    Compare a resume against a job description and suggest
    concrete improvements.
    """

    prompt = (
        "You are an ATS resume optimization assistant. Compare "
        "the RESUME against the JOB DESCRIPTION.\n\n"
        f"RESUME:\n{(resume_text or '')[:6000]}\n\n"
        f"JOB DESCRIPTION:\n{(job_text or '')[:4000]}\n\n"
        f"Skills already matched: "
        f"{', '.join(matched_skills) or 'none'}\n"
        f"Skills currently missing: "
        f"{', '.join(missing_skills) or 'none'}\n\n"
        "Return: ats_keyword_score (0-100, how well the resume's "
        "wording covers the job's key terms), missing_keywords "
        "(important terms/skills from the job description that "
        "are absent or weak in the resume), strong_points "
        "(what the resume already does well for this role), "
        "summary (2-3 sentences of overall guidance), and "
        "bullet_suggestions: for up to 4 resume lines that could "
        "be strengthened, give original_bullet (quoted or closely "
        "paraphrased from the resume), improved_bullet (a rewritten "
        "version using the X-Y-Z formula: accomplished X, measured "
        "by Y, by doing Z, using only facts implied by the original "
        "— do not invent numbers that aren't grounded in the text), "
        "and reason (why the change helps)."
    )

    result = _gemini_json(
        prompt,
        ResumeOptimizationResult,
    )

    if result:
        return result

    return _fallback_resume_optimization(
        resume_text,
        job_text,
        missing_skills,
        matched_skills,
    )


class TailoredWorkExperience(BaseModel):
    title: str
    organization: str
    duration: str
    bullets: list[str]


class TailoredProject(BaseModel):
    name: str
    description: str
    tech_stack: str
    bullets: list[str]


class TailoredResume(BaseModel):
    full_name: str
    contact_line: str
    professional_summary: str
    key_skills: list[str]
    work_experience: list[TailoredWorkExperience]
    projects: list[TailoredProject]
    education: list[str]
    certifications: list[str]
    keywords_incorporated: list[str]
    tailoring_notes: str


def _fallback_tailored_resume(
    resume_text,
    job_title,
    company_name,
):
    """
    Rule-based fallback when Gemini is unavailable.

    This reformats the master resume's own extracted sections
    rather than pretending to perform AI tailoring.
    """

    lines = [
        l.strip()
        for l in (resume_text or "").splitlines()
        if l.strip()
    ]

    name_guess = (
        lines[0]
        if lines
        else "Your Name"
    )

    contact_line = next(
        (
            l
            for l in lines
            if "@" in l
            or re.search(r"\d{3,}", l)
        ),
        "",
    )

    return {
        "full_name": name_guess[:100],
        "contact_line": contact_line[:200],
        "professional_summary": (
            "(AI unavailable — showing your original resume "
            "content reformatted, not truly tailored to "
            f"{job_title or 'the target role'} at "
            f"{company_name or 'the target company'}. "
            "Re-run this once Gemini is reachable for an actual "
            "tailored rewrite.)"
        ),
        "key_skills": [],
        "work_experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
        "keywords_incorporated": [],
        "tailoring_notes": (
            "This is your original resume text, unmodified — "
            "AI tailoring was unavailable when this was generated."
        ),
    }


def generate_tailored_resume(
    resume_text,
    job_text,
    job_title,
    company_name,
    missing_skills,
    matched_skills,
):
    """
    Rewrite the person's own master resume into a version
    tailored to one specific job posting.

    The master resume remains the source of truth.
    """

    prompt = (
        "You are a professional resume writer. Rewrite the "
        "candidate's MASTER RESUME into a version tailored "
        f"specifically for this role: "
        f"{job_title or 'the target role'} at "
        f"{company_name or 'the target company'}.\n\n"

        "MASTER RESUME (the ONLY source of truth for facts — "
        "do not invent employers, titles, dates, metrics, or "
        "achievements not grounded in this text):\n"
        f"{(resume_text or '')[:6000]}\n\n"

        "TARGET JOB DESCRIPTION:\n"
        f"{(job_text or '')[:4000]}\n\n"

        "Skills the candidate already has: "
        f"{', '.join(matched_skills) or 'none identified'}\n"

        "Skills the role wants that are weak/missing: "
        f"{', '.join(missing_skills) or 'none'}\n\n"

        "Rules: the MASTER RESUME is the ONLY source of truth for "
        "candidate facts. Reorder and re-emphasize the candidate's "
        "REAL experience so the most relevant parts lead; tighten "
        "bullets using the X-Y-Z formula (accomplished X, measured "
        "by Y, by doing Z) using only numbers/facts implied by the "
        "original text — never fabricate metrics, achievements, "
        "employers, titles, dates, technologies, responsibilities, "
        "users, revenue, percentages, or outcomes. Keep every employer, "
        "job title, and date exactly as in the original.\n\n"

        "Preserve relevant projects from the MASTER RESUME. Do not "
        "remove a relevant project simply because the job description "
        "does not explicitly mention it. Reorder projects by relevance "
        "when appropriate. Never invent a project, technology, metric, "
        "result, or achievement.\n\n"

        "Naturally work in missing keywords ONLY where the candidate's "
        "real background genuinely supports them. If a requested skill "
        "is unsupported, do not add it to the resume and do not claim "
        "the candidate has it.\n\n"

        "Return: full_name, contact_line, professional_summary "
        "(3-4 sentences targeted at this role), key_skills "
        "(ordered by relevance to this job), work_experience "
        "(list of {title, organization, duration, bullets}), projects "
        "(list of {name, description, tech_stack, bullets}), education "
        "(list of strings), certifications (list of strings, empty if "
        "none), keywords_incorporated (only missing keywords you were "
        "able to truthfully work in), and tailoring_notes (1-2 sentences "
        "on what changed and why)."
    )

    result = _gemini_json(
        prompt,
        TailoredResume,
    )

    if result:
        return result

    return _fallback_tailored_resume(
        resume_text,
        job_title,
        company_name,
    )