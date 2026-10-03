ALIASES = {
    "python": "python",
    "python programming": "python",
    "sql": "sql",
    "mysql": "sql",
    "postgresql": "sql",
    "excel": "excel",
    "microsoft excel": "excel",
    "power bi": "power bi",
    "powerbi": "power bi",
    "tableau": "tableau",
    "statistics": "statistics",
    "data analysis": "data analysis",
    "data analytics": "data analysis",
    "machine learning": "machine learning",
    "ml": "machine learning",
    "javascript": "javascript",
    "react": "react",
    "django": "django",
    "html": "html",
    "css": "css",
}


def normalize_skill(skill):
    if not skill:
        return ""

    value = skill.strip().lower()

    return ALIASES.get(value, value)


def normalize_skills(skills):
    if not skills:
        return []

    normalized = []

    for skill in skills:
        value = normalize_skill(skill)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


def get_skill_proficiency(profile_skills, skill):
    normalized_target = normalize_skill(skill)

    for profile_skill in profile_skills:
        name = normalize_skill(profile_skill.get("name", ""))

        if name == normalized_target:
            return profile_skill.get("proficiency", "beginner")

    return None


def calculate_skill_match(required_skills, profile_skills):
    matched = []
    improve = []
    missing = []

    normalized_required = normalize_skills(required_skills)

    for skill in normalized_required:

        proficiency = get_skill_proficiency(profile_skills, skill)

        if proficiency is None:
            missing.append(skill)

        elif proficiency == "beginner":
            improve.append(skill)

        else:
            matched.append(skill)

    return matched, improve, missing


def calculate_experience_match(
    experience_required,
    resume_experience
):
    if not experience_required:
        return True

    if not resume_experience:
        return False

    return True


def calculate_education_match(
    education_required,
    resume_education
):
    if not education_required:
        return True

    if not resume_education:
        return False

    return True


def calculate_match_score(
    resume_analysis,
    job_analysis,
    profile_skills=None
):
    profile_skills = profile_skills or []

    required_skills = job_analysis.get("required_skills", [])
    preferred_skills = job_analysis.get("preferred_skills", [])

    resume_skills = resume_analysis.get("skills", [])

    # If profile skills are available, use them.
    # Otherwise use resume skills as the student's skill set.
    if profile_skills:
        matched_required, improve_required, missing_required = calculate_skill_match(
            required_skills,
            profile_skills
        )
    else:
        normalized_resume = set(normalize_skills(resume_skills))

        matched_required = []
        improve_required = []
        missing_required = []

        for skill in normalize_skills(required_skills):

            if skill in normalized_resume:
                matched_required.append(skill)
            else:
                missing_required.append(skill)

    normalized_resume = set(normalize_skills(resume_skills))
    normalized_profile = set(
        normalize_skill(skill.get("name", ""))
        for skill in profile_skills
    )

    combined_skills = normalized_resume.union(normalized_profile)

    matched_preferred = []
    missing_preferred = []

    for skill in normalize_skills(preferred_skills):

        if skill in combined_skills:
            matched_preferred.append(skill)
        else:
            missing_preferred.append(skill)

    experience_match = calculate_experience_match(
        job_analysis.get("experience_required", ""),
        resume_analysis.get("experience", [])
    )

    education_match = calculate_education_match(
        job_analysis.get("education_required", ""),
        resume_analysis.get("education", [])
    )

    # --------------------------------------------------
    # Transparent scoring
    # --------------------------------------------------

    required_total = len(
        matched_required + improve_required + missing_required
    )

    if required_total:
        required_score = (
            (len(matched_required) + (len(improve_required) * 0.5))
            / required_total
        ) * 70
    else:
        required_score = 70

    preferred_total = len(
        matched_preferred + missing_preferred
    )

    if preferred_total:
        preferred_score = (
            len(matched_preferred) / preferred_total
        ) * 10
    else:
        preferred_score = 10

    experience_score = 10 if experience_match else 0

    education_score = 10 if education_match else 0

    total_score = (
        required_score
        + preferred_score
        + experience_score
        + education_score
    )

    total_score = round(min(total_score, 100), 2)

    return {
        "match_score": total_score,
        "matched_skills": matched_required,
        "skills_to_improve": improve_required,
        "missing_skills": missing_required,
        "preferred_skills_missing": missing_preferred,
        "experience_match": experience_match,
        "education_match": education_match,
    }