from urllib.parse import quote_plus

from profiles.models import StudentProfile
from careerbridge import ai


# ---------------------------------------------------------
# Learning content for common skills
# ---------------------------------------------------------

SKILL_CONTENT = {

    "python": {
        "topics": [
            "Python fundamentals",
            "Functions and modules",
            "Lists, dictionaries and sets",
            "Exception handling",
            "File handling",
            "Object-oriented programming"
        ],
        "practice": [
            "Solve 10 Python programming problems",
            "Build a small data-processing script",
            "Practice functions and dictionary-based problems"
        ],
        "project": "Build a Python data analysis or automation project."
    },

    "sql": {
        "topics": [
            "SELECT and filtering",
            "GROUP BY and aggregate functions",
            "JOINs",
            "Subqueries",
            "CTEs",
            "Window functions"
        ],
        "practice": [
            "Solve 20 SQL queries",
            "Practice JOIN problems",
            "Practice aggregation and subquery problems"
        ],
        "project": "Build a small SQL analytics project using a real-world dataset."
    },

    "excel": {
        "topics": [
            "Excel formulas",
            "Lookup functions",
            "Pivot tables",
            "Data cleaning",
            "Conditional formatting",
            "Charts and dashboards"
        ],
        "practice": [
            "Create a sales analysis worksheet",
            "Practice XLOOKUP/VLOOKUP",
            "Create a pivot-table report"
        ],
        "project": "Create an interactive Excel business dashboard."
    },

    "power bi": {
        "topics": [
            "Power BI interface",
            "Data loading",
            "Power Query",
            "Data cleaning",
            "Data modeling",
            "DAX basics",
            "Dashboard design"
        ],
        "practice": [
            "Import and clean a dataset",
            "Create relationships between tables",
            "Create calculated measures",
            "Build an interactive dashboard"
        ],
        "project": "Build a Power BI sales or business analytics dashboard."
    },

    "tableau": {
        "topics": [
            "Tableau fundamentals",
            "Data connections",
            "Charts",
            "Filters",
            "Calculated fields",
            "Dashboard creation"
        ],
        "practice": [
            "Create five different visualizations",
            "Practice filters and calculated fields",
            "Build one complete dashboard"
        ],
        "project": "Build a Tableau analytics dashboard."
    },

    "statistics": {
        "topics": [
            "Mean, median and mode",
            "Variance and standard deviation",
            "Probability",
            "Distributions",
            "Correlation",
            "Hypothesis testing"
        ],
        "practice": [
            "Solve 15 statistics problems",
            "Analyze a dataset using descriptive statistics",
            "Practice correlation analysis"
        ],
        "project": "Perform statistical analysis on a real-world dataset."
    },

    "javascript": {
        "topics": [
            "JavaScript fundamentals",
            "Variables and functions",
            "Arrays and objects",
            "DOM manipulation",
            "ES6 features",
            "Async JavaScript"
        ],
        "practice": [
            "Solve 15 JavaScript problems",
            "Build interactive DOM components",
            "Practice array and object operations"
        ],
        "project": "Build an interactive JavaScript web application."
    },

    "react": {
        "topics": [
            "React fundamentals",
            "Components",
            "Props and state",
            "Hooks",
            "Forms",
            "API integration"
        ],
        "practice": [
            "Build reusable components",
            "Create a form",
            "Consume a REST API"
        ],
        "project": "Build a React dashboard connected to an API."
    },

    "django": {
        "topics": [
            "Django fundamentals",
            "Models",
            "Views",
            "URLs",
            "Django REST Framework",
            "Authentication",
            "API development"
        ],
        "practice": [
            "Create CRUD APIs",
            "Implement authentication",
            "Connect Django to MySQL"
        ],
        "project": "Build a complete Django REST API project."
    },

    "machine learning": {
        "topics": [
            "Machine learning fundamentals",
            "Data preprocessing",
            "Regression",
            "Classification",
            "Model evaluation",
            "Feature engineering"
        ],
        "practice": [
            "Train a regression model",
            "Train a classification model",
            "Evaluate model performance"
        ],
        "project": "Build and deploy a machine learning prediction project."
    },

    "html": {
        "topics": [
            "HTML fundamentals",
            "Semantic HTML",
            "Forms",
            "Tables",
            "Accessibility"
        ],
        "practice": [
            "Build a multi-section webpage",
            "Create an HTML form",
            "Practice semantic HTML"
        ],
        "project": "Build a responsive portfolio webpage."
    },

    "css": {
        "topics": [
            "CSS fundamentals",
            "Flexbox",
            "Grid",
            "Responsive design",
            "Animations"
        ],
        "practice": [
            "Create responsive layouts",
            "Practice Flexbox",
            "Practice CSS Grid"
        ],
        "project": "Build a responsive portfolio website."
    },
}


DEFAULT_CONTENT = {
    "topics": [
        "Understand the fundamentals",
        "Learn the core concepts",
        "Practice common problems",
        "Work with a real-world example"
    ],
    "practice": [
        "Complete 10 beginner practice problems",
        "Complete 5 intermediate practice problems",
        "Apply the skill to a small project"
    ],
    "project": "Build a small project demonstrating this skill."
}


CURATED_SEARCH_QUERIES = {
    "python": "Python full course for beginners",
    "sql": "SQL full course for data analyst",
    "excel": "Excel full course pivot tables VLOOKUP",
    "power bi": "Power BI full course dashboard tutorial",
    "tableau": "Tableau full course dashboard tutorial",
    "statistics": "Statistics for data analysis full course",
    "javascript": "JavaScript full course for beginners",
    "react": "React JS full course tutorial",
    "django": "Django REST framework full course",
    "machine learning": "Machine learning full course for beginners",
    "html": "HTML full course for beginners",
    "css": "CSS full course flexbox grid",
}

OFFICIAL_DOCS = {
    "python": "https://docs.python.org/3/",
    "sql": "https://dev.mysql.com/doc/",
    "excel": "https://support.microsoft.com/en-us/excel",
    "power bi": "https://learn.microsoft.com/en-us/power-bi/",
    "tableau": "https://help.tableau.com/current/guides/get-started-tutorial/en-us/",
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "react": "https://react.dev/",
    "django": "https://docs.djangoproject.com/",
    "html": "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "css": "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "machine learning": "https://scikit-learn.org/stable/documentation.html",
    "statistics": "https://www.khanacademy.org/math/statistics-probability",
}


def _youtube_search_url(query):
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


def get_learning_resources(skill):
    """Return a small list of learning links for a skill: one curated
    'always safe' YouTube search, one official documentation link, plus
    (when available) an AI-suggested video pick. We deliberately link to
    YouTube *search results* rather than a specific video URL, since we
    can't verify a fabricated video ID actually exists. Official doc links
    are also verified-safe: either a known, hand-picked docs URL, or a
    Google search for the docs (never a fabricated docs URL).
    """
    normalized = skill.strip().lower()
    query = CURATED_SEARCH_QUERIES.get(normalized, f"{skill} full course tutorial for beginners")

    resources = [{
        "title": f"{skill.title()} — Full Course / Playlist",
        "provider": "YouTube",
        "url": _youtube_search_url(query),
        "type": "video",
        "ai_recommended": False,
    }]

    doc_url = OFFICIAL_DOCS.get(normalized) or (
        f"https://www.google.com/search?q={quote_plus(f'{skill} official documentation')}"
    )
    resources.append({
        "title": f"{skill.title()} — Official Documentation",
        "provider": "Official Docs",
        "url": doc_url,
        "type": "doc",
        "ai_recommended": False,
    })

    try:
        picks = ai.generate_course_recommendations(skill, count=1)
    except Exception:
        picks = None

    if picks:
        pick = picks[0]
        resources.append({
            "title": pick.get("title") or f"AI pick: {skill.title()}",
            "provider": pick.get("provider", "YouTube"),
            "url": _youtube_search_url(pick.get("search_query") or query),
            "type": "video",
            "reason": pick.get("reason", ""),
            "ai_recommended": True,
        })

    try:
        from resources.models import CommunityResource
        community_items = CommunityResource.objects.filter(skill__iexact=skill)[:5]
        for item in community_items:
            resources.append({
                "title": item.title,
                "provider": f"Shared by {item.submitted_by.username}",
                "url": item.url,
                "type": item.resource_type,
                "community": True,
                "note": item.note,
            })
    except Exception:
        pass

    return resources


def get_skill_content(skill):
    normalized = skill.strip().lower()

    return SKILL_CONTENT.get(
        normalized,
        DEFAULT_CONTENT
    )


def get_current_level(profile, skill):
    if not profile:
        return "Not Available"

    profile_skills = profile.skills.all()

    target = skill.strip().lower()

    for profile_skill in profile_skills:

        if profile_skill.name.strip().lower() == target:
            return profile_skill.proficiency.title()

    return "Not Available"
def generate_learning_content(
    skill,
    category,
    current_level,
    target_level,
    job_title,
    job_description,
    resume_text,
    reason,
):
    """
    Generate a personalized learning module for one roadmap skill
    using Gemini.

    If Gemini is unavailable, return None so the roadmap can use
    the existing static fallback content.
    """

    try:
        module = ai.generate_roadmap_module(
            skill=skill,
            category=category,
            current_level=current_level,
            target_level=target_level,
            job_title=job_title,
            job_description=job_description,
            resume_text=resume_text,
            match_reason=reason,
        )

        if module:
            return module

    except Exception as exc:
        print(
            f"AI roadmap generation failed for {skill}: {exc}"
        )

    return None




# -----------------------------------------------------
# Personalized learning content + roadmap lifecycle data
# -----------------------------------------------------

def create_roadmap_data(match_result):
    user = match_result.user

    try:
        profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        profile = None

    items = []

    for skill in match_result.skills_to_improve:
        items.append({
            "skill": skill,
            "category": "improve",
            "priority": "high",
            "current_level": get_current_level(profile, skill),
            "target_level": "Intermediate",
            "reason": (
                f"You already have {skill}, but your current "
                "proficiency needs improvement for this job."
            ),
            "estimated_days": 7,
        })

    for skill in match_result.missing_skills:
        items.append({
            "skill": skill,
            "category": "missing",
            "priority": "high",
            "current_level": "Missing",
            "target_level": "Intermediate",
            "reason": (
                f"{skill} is required for the selected job "
                "but was not found in your current skill set."
            ),
            "estimated_days": 10,
        })

    for skill in match_result.preferred_skills_missing:
        items.append({
            "skill": skill,
            "category": "preferred",
            "priority": "low",
            "current_level": "Missing",
            "target_level": "Beginner",
            "reason": (
                f"{skill} is preferred for the selected job. "
                "Learning it can strengthen your profile."
            ),
            "estimated_days": 5,
        })

    job_description_obj = match_result.job_description
    job_title = job_description_obj.job_title
    job_description_text = (
        job_description_obj.extracted_text
        or job_description_obj.description
        or ""
    )
    resume_text = match_result.resume.extracted_text or ""

    final_items = []

    for item in items:
        skill = item["skill"]
        ai_content = generate_learning_content(
            skill=skill,
            category=item["category"],
            current_level=item["current_level"],
            target_level=item["target_level"],
            job_title=job_title,
            job_description=job_description_text,
            resume_text=resume_text,
            reason=item["reason"],
        )

        if ai_content:
            item["learning_content"] = ai_content
            item["learning_topics"] = (
                ai_content.get("concepts")
                or ai_content.get("learning_objectives")
                or []
            )
            item["practice_tasks"] = ai_content.get("practice_tasks") or []
            item["project_task"] = ai_content.get("project_task") or ""
        else:
            content = get_skill_content(skill)
            checklist = [
                f"Understand the fundamentals of {skill}",
                f"Complete the assigned {skill} practice tasks",
                f"Complete the project task for {skill}",
            ]
            item["learning_content"] = {
                "overview": f"Learn {skill} from the fundamentals to the target level.",
                "why_it_matters": item["reason"],
                "learning_objectives": content["topics"],
                "concepts": content["topics"],
                "examples": [],
                "practice_tasks": content["practice"],
                "project_task": content["project"],
                "completion_checklist": checklist,
                "suggested_search_queries": [
                    CURATED_SEARCH_QUERIES.get(
                        skill.strip().lower(),
                        f"{skill} tutorial for beginners",
                    )
                ],
            }
            item["learning_topics"] = content["topics"]
            item["practice_tasks"] = content["practice"]
            item["project_task"] = content["project"]

        try:
            resources = get_learning_resources(skill)
        except Exception as exc:
            print(f"Learning resource lookup failed for {skill}: {exc}")
            resources = []

        if ai_content:
            for query in ai_content.get("suggested_search_queries", []):
                if query:
                    resources.append({
                        "title": f"AI Learning Search: {query}",
                        "provider": "YouTube",
                        "url": _youtube_search_url(query),
                        "type": "video",
                        "ai_recommended": True,
                    })

        item["resources"] = resources
        item["completed_learning_steps"] = []
        item["learning_started_at"] = None
        item["learning_completed_at"] = None
        item["mock_pass_score"] = 70
        item["mock_completed"] = False
        final_items.append(item)

    priority_order = {"high": 1, "medium": 2, "low": 3}
    final_items.sort(key=lambda x: priority_order.get(x["priority"], 9))

    total_days = min(max(sum(x["estimated_days"] for x in final_items), 7), 90)

    title = f"{job_title} Career Readiness Roadmap"
    if final_items:
        summary = (
            "This roadmap is personalized from your resume, the exact company "
            "job description and your match result. It focuses on the skill gaps "
            f"identified for the {job_title} role."
        )
    else:
        summary = (
            f"No major skill gaps were identified for the {job_title} role. "
            "Focus on interview preparation and strengthening your existing skills."
        )

    return {
        "title": title,
        "summary": summary,
        "total_days": total_days,
        "items": final_items,
    }
