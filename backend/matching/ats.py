
import re


STANDARD_SECTIONS = {
    "professional summary": [
        "professional summary",
        "summary",
        "career objective",
        "objective",
    ],
    "technical skills": [
        "technical skills",
        "skills",
        "technical skill",
    ],
    "professional experience": [
        "professional experience",
        "work experience",
        "experience",
        "internship experience",
    ],
    "projects": [
        "projects",
        "project experience",
        "academic projects",
    ],
    "education": [
        "education",
        "academic background",
    ],
    "certifications": [
        "certifications",
        "certificates",
    ],
}


def _clean(value):
    return str(value or "").strip()


def _normalise(value):
    return re.sub(r"\s+", " ", _clean(value).lower())


def _contains_keyword(text, keyword):
    """
    Conservative keyword matching.

    Uses word boundaries so that, for example,
    'sql' does not accidentally match unrelated words.
    """
    text = _normalise(text)
    keyword = _normalise(keyword)

    if not keyword:
        return False

    pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
    return bool(re.search(pattern, text))


def _resume_to_text(resume):
    """
    Converts our structured tailored-resume JSON into
    searchable plain text.
    """
    if not resume:
        return ""

    parts = []

    for key in (
        "full_name",
        "contact_line",
        "professional_summary",
    ):
        value = resume.get(key)
        if value:
            parts.append(str(value))

    for key in ("key_skills", "education", "certifications"):
        values = resume.get(key) or []
        if isinstance(values, list):
            parts.extend(str(item) for item in values)

    for job in resume.get("work_experience") or []:
        if not isinstance(job, dict):
            continue

        parts.extend(
            [
                job.get("title", ""),
                job.get("organization", ""),
                job.get("duration", ""),
            ]
        )
        parts.extend(job.get("bullets") or [])

    for project in resume.get("projects") or []:
        if isinstance(project, dict):
            parts.extend(
                [
                    project.get("name", ""),
                    project.get("title", ""),
                    project.get("description", ""),
                    project.get("tech_stack", ""),
                ]
            )
            parts.extend(project.get("bullets") or [])
        else:
            parts.append(str(project))

    return "\n".join(str(x) for x in parts if x)


def _extract_original_sections(text):
    """
    Checks whether common ATS-readable headings exist in
    the original resume text.
    """
    normalised = _normalise(text)

    found = []

    for canonical, aliases in STANDARD_SECTIONS.items():
        if any(alias in normalised for alias in aliases):
            found.append(canonical)

    return found


def _keyword_report(resume_text, job_analysis):
    required = job_analysis.get("required_skills") or []
    preferred = job_analysis.get("preferred_skills") or []

    required = [_clean(x) for x in required if _clean(x)]
    preferred = [_clean(x) for x in preferred if _clean(x)]

    matched_required = [
        skill for skill in required
        if _contains_keyword(resume_text, skill)
    ]

    matched_preferred = [
        skill for skill in preferred
        if _contains_keyword(resume_text, skill)
    ]

    missing_required = [
        skill for skill in required
        if skill not in matched_required
    ]

    missing_preferred = [
        skill for skill in preferred
        if skill not in matched_preferred
    ]

    required_score = (
        (len(matched_required) / len(required)) * 100
        if required else 100
    )

    preferred_score = (
        (len(matched_preferred) / len(preferred)) * 100
        if preferred else 100
    )

    return {
        "required_keywords": required,
        "matched_required_keywords": matched_required,
        "missing_required_keywords": missing_required,
        "preferred_keywords": preferred,
        "matched_preferred_keywords": matched_preferred,
        "missing_preferred_keywords": missing_preferred,
        "required_keyword_score": round(required_score, 2),
        "preferred_keyword_score": round(preferred_score, 2),
    }


def calculate_ats_score(resume_text, job_analysis=None):
    """
    Produces a transparent ATS score.

    This is deliberately deterministic.
    No AI call is made here.
    """
    resume_text = _clean(resume_text)
    job_analysis = job_analysis or {}

    if not resume_text:
        return {
            "score": 0,
            "grade": "Needs work",
            "keyword_score": 0,
            "structure_score": 0,
            "readability_score": 0,
            "content_score": 0,
            "checks": [],
            "missing_required_keywords": [],
            "matched_required_keywords": [],
        }

    checks = []

    # --------------------------------------------------
    # 1. Structure — 25 points
    # --------------------------------------------------

    sections = _extract_original_sections(resume_text)

    structure_points = 0

    if len(sections) >= 4:
        structure_points += 10
        checks.append({
            "name": "Standard resume sections",
            "status": "pass",
            "message": "Multiple standard resume sections were detected.",
        })
    else:
        checks.append({
            "name": "Standard resume sections",
            "status": "warning",
            "message": "Some standard resume sections may be missing.",
        })

    if re.search(r"\b(education|degree|bca|mca|b\.?tech|m\.?tech)\b", resume_text, re.I):
        structure_points += 5
        checks.append({
            "name": "Education section",
            "status": "pass",
            "message": "Education information was detected.",
        })
    else:
        checks.append({
            "name": "Education section",
            "status": "warning",
            "message": "Education information was not clearly detected.",
        })

    if re.search(r"@", resume_text):
        structure_points += 5
        checks.append({
            "name": "Email/contact information",
            "status": "pass",
            "message": "An email address was detected.",
        })
    else:
        checks.append({
            "name": "Email/contact information",
            "status": "warning",
            "message": "An email address was not detected.",
        })

    if re.search(r"\b\d{10}\b", resume_text):
        structure_points += 5
        checks.append({
            "name": "Phone number",
            "status": "pass",
            "message": "A phone number was detected.",
        })

    # --------------------------------------------------
    # 2. Readability — 20 points
    # --------------------------------------------------

    readability_points = 20

    if len(resume_text) < 500:
        readability_points -= 8
        checks.append({
            "name": "Content density",
            "status": "warning",
            "message": "The resume appears to contain very little text.",
        })

    elif len(resume_text) > 12000:
        readability_points -= 5
        checks.append({
            "name": "Content density",
            "status": "warning",
            "message": "The resume may be unnecessarily long.",
        })
    else:
        checks.append({
            "name": "Content density",
            "status": "pass",
            "message": "Resume content is within a reasonable text range.",
        })

    if resume_text.count("|") > 40:
        readability_points -= 5
        checks.append({
            "name": "Excessive separators",
            "status": "warning",
            "message": "There may be excessive visual separators.",
        })

    # --------------------------------------------------
    # 3. Content completeness — 25 points
    # --------------------------------------------------

    content_points = 0

    content_checks = [
        (
            "Professional summary",
            r"\b(summary|objective|profile)\b",
            5,
        ),
        (
            "Skills",
            r"\b(skills|technical skills)\b",
            5,
        ),
        (
            "Experience",
            r"\b(experience|internship|employment)\b",
            5,
        ),
        (
            "Projects",
            r"\b(projects|project experience)\b",
            5,
        ),
        (
            "Education",
            r"\b(education|degree|mca|bca)\b",
            5,
        ),
    ]

    for name, pattern, points in content_checks:
        if re.search(pattern, resume_text, re.I):
            content_points += points
            checks.append({
                "name": name,
                "status": "pass",
                "message": f"{name} information was detected.",
            })
        else:
            checks.append({
                "name": name,
                "status": "warning",
                "message": f"{name} information was not clearly detected.",
            })

    # --------------------------------------------------
    # 4. Job keyword relevance — 30 points
    # --------------------------------------------------

    keyword = _keyword_report(resume_text, job_analysis)

    keyword_score = (
        keyword["required_keyword_score"] * 0.75
        + keyword["preferred_keyword_score"] * 0.25
    )

    final_score = (
        structure_points
        + readability_points
        + content_points
        + (keyword_score * 0.30)
    )

    final_score = round(min(max(final_score, 0), 100), 2)

    if final_score >= 85:
        grade = "Excellent"
    elif final_score >= 70:
        grade = "Strong"
    elif final_score >= 55:
        grade = "Needs improvement"
    else:
        grade = "Needs work"

    return {
        "score": final_score,
        "grade": grade,
        "keyword_score": round(keyword_score, 2),
        "structure_score": structure_points * 4,
        "readability_score": readability_points * 5,
        "content_score": content_points * 4,
        "checks": checks,
        **keyword,
    }


def compare_ats_scores(before, after):
    before_score = float((before or {}).get("score", 0))
    after_score = float((after or {}).get("score", 0))

    return {
        "before": round(before_score, 2),
        "after": round(after_score, 2),
        "improvement": round(after_score - before_score, 2),
    }

