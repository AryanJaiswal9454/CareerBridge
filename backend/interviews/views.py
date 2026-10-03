from django.utils import timezone

import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from matching.models import MatchResult
from roadmap.models import RoadmapItem, Roadmap
from careerbridge import ai

from .models import (
    InterviewSession,
    InterviewQuestion,
)

from .serializers import (
    InterviewSessionSerializer,
)

from .engine import (
    generate_interview_questions,
    get_priority_skills,
    get_external_practice_links,
    get_question_bank_set,
    generate_targeted_interview_questions,
    get_role_catalog,
    get_role,
)


class CreateInterviewSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        match_id = request.data.get("match_id")
        roadmap_item_id = request.data.get("roadmap_item_id")
        session_type = request.data.get("session_type", "mixed")

        try:
            question_count = max(1, min(int(request.data.get("question_count", 5)), 10))
        except (TypeError, ValueError):
            question_count = 5

        if session_type not in {"mcq", "technical", "behavioral", "mixed"}:
            return Response({"error": "Invalid session_type."}, status=400)

        roadmap_item = None
        if roadmap_item_id:
            try:
                roadmap_item = RoadmapItem.objects.select_related(
                    "roadmap", "roadmap__match_result", "roadmap__resume", "roadmap__job_description"
                ).get(id=roadmap_item_id, roadmap__user=request.user)
            except RoadmapItem.DoesNotExist:
                return Response({"error": "Roadmap item not found."}, status=404)

            if not roadmap_item.learning_completed_at:
                return Response({"error": "Complete the learning module before starting this mock."}, status=400)
            match_result = roadmap_item.roadmap.match_result
        else:
            if not match_id:
                return Response({"error": "match_id is required."}, status=400)
            try:
                match_result = MatchResult.objects.get(id=match_id, user=request.user)
            except MatchResult.DoesNotExist:
                return Response({"error": "Match result not found."}, status=404)

        role_id = (request.data.get("role_id") or "").strip().lower()
        selected_skill = (request.data.get("skill") or "").strip()
        selected_topic = (request.data.get("topic") or "").strip()
        difficulty = (request.data.get("difficulty") or "medium").strip().lower()

        if roadmap_item:
            selected_skill = roadmap_item.skill
            content = roadmap_item.learning_content or {}
            concepts = content.get("concepts") or roadmap_item.learning_topics or []
            selected_topic = selected_topic or (concepts[0] if concepts else roadmap_item.skill)
            if not role_id:
                job_title = match_result.job_description.job_title.lower()
                for candidate in [
                    "python-developer", "data-analyst", "software-developer",
                    "django-developer", "full-stack-developer", "backend-developer",
                    "frontend-developer", "react-developer", "data-scientist",
                    "ml-engineer", "ai-engineer", "sql-developer",
                ]:
                    role = get_role(candidate)
                    if role and role["name"].lower() in job_title:
                        role_id = candidate
                        break
                if not role_id:
                    for candidate in [
                        "python-developer", "data-analyst", "software-developer",
                        "django-developer", "full-stack-developer", "backend-developer",
                        "frontend-developer", "react-developer", "data-scientist",
                    ]:
                        role = get_role(candidate)
                        if role and any(s.lower() == selected_skill.lower() for s in role["skills"]):
                            role_id = candidate
                            break

        if role_id and selected_skill and selected_topic:
            if difficulty not in {"easy", "medium", "hard"}:
                return Response({"error": "difficulty must be easy, medium or hard."}, status=400)
            try:
                questions = generate_targeted_interview_questions(
                    role_id=role_id,
                    skill=selected_skill,
                    topic=selected_topic,
                    difficulty=difficulty,
                    session_type=session_type,
                    limit=question_count,
                    user=request.user,
                )
            except ValueError as exc:
                return Response({"error": str(exc)}, status=400)
        else:
            questions = generate_interview_questions(
                match_result, session_type=session_type, limit=question_count
            )

        if not questions:
            return Response({"error": "Unable to generate interview questions for this target."}, status=400)

        session = InterviewSession.objects.create(
            user=request.user,
            resume=match_result.resume,
            job_description=match_result.job_description,
            match_result=match_result,
            roadmap_item=roadmap_item,
            session_type=session_type,
            total_questions=len(questions),
        )

        for question_data in questions:
            InterviewQuestion.objects.create(
                session=session,
                question=question_data["question"],
                category=question_data.get("category", "technical"),
                question_type=question_data.get("question_type", "open"),
                related_skill=question_data.get("related_skill") or selected_skill,
                expected_points=question_data.get("expected_points", []),
                options=question_data.get("options", []),
                correct_option=question_data.get("correct_option"),
                starter_code=question_data.get("starter_code"),
                language=question_data.get("language"),
                sample_solution=question_data.get("sample_solution"),
                explanation=question_data.get("explanation"),
            )

        serializer = InterviewSessionSerializer(session)
        practice_links = get_external_practice_links(get_priority_skills(match_result))

        return Response({
            "message": "Interview session created successfully.",
            "session": serializer.data,
            "practice_links": practice_links,
            "roadmap_item_id": roadmap_item.id if roadmap_item else None,
            "target": {
                "role_id": role_id,
                "skill": selected_skill,
                "topic": selected_topic,
            },
        }, status=201)


class InterviewSessionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        sessions = InterviewSession.objects.filter(
            user=request.user
        ).prefetch_related("questions")

        serializer = InterviewSessionSerializer(
            sessions,
            many=True
        )

        return Response(
            {
                "count": sessions.count(),
                "sessions": serializer.data
            }
        )


def _grade_mcq(question, request_data):
    selected_option = str(request_data.get("selected_option", "")).strip().upper()

    if not selected_option:
        return None, {"error": "selected_option is required."}

    is_correct = selected_option == (question.correct_option or "").strip().upper()

    question.selected_option = selected_option
    question.answer = selected_option
    question.is_correct = is_correct
    question.score = 100 if is_correct else 0
    question.feedback = "Correct!" if is_correct else "Not quite — see the explanation below."
    question.improvement_tips = [] if is_correct else [
        f"Review why option {question.correct_option} is correct.",
        "Revisit this topic before your next round.",
    ]
    return question, None


# Boilerplate/keyword tokens that show up in almost any sample solution but
# don't actually signal whether the candidate solved *this* problem — we
# ignore these when comparing the candidate's answer against the reference.
_GENERIC_CODE_TOKENS = {
    "def", "function", "return", "the", "and", "for", "self", "this",
    "let", "const", "var", "class", "import", "from", "true", "false",
    "none", "null", "int", "str", "string", "with", "then", "else",
}


def _heuristic_grade_coding(answer, sample_solution, question_text):
    """Response-dependent fallback grading used only when AI grading is
    unavailable: compares the candidate's actual answer against the
    meaningful tokens in the reference solution, so the feedback reflects
    what THIS answer is missing rather than one fixed message every time.
    """
    def meaningful_tokens(text):
        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]{2,}", text.lower())
        return {t for t in tokens if t not in _GENERIC_CODE_TOKENS}

    reference_tokens = meaningful_tokens(sample_solution or "")
    answer_tokens = meaningful_tokens(answer)

    matched = reference_tokens & answer_tokens
    missing = sorted(reference_tokens - answer_tokens)

    coverage = (len(matched) / len(reference_tokens)) if reference_tokens else 0.5
    word_count = len(answer.split())
    length_bonus = min(20, word_count // 3)

    score = max(0, min(100, round(coverage * 80) + length_bonus))
    is_correct = score >= 70

    if is_correct:
        feedback = f"Your answer covers most of the key ideas ({len(matched)}/{len(reference_tokens) or 1} key terms present)."
        missing_points = []
    else:
        feedback = (
            f"Your answer is missing some of the key ideas from a strong solution "
            f"({len(matched)}/{len(reference_tokens) or 1} key terms present)."
        )
        missing_points = [
            f"Consider whether your solution should involve: {', '.join(missing[:5])}."
        ] if missing else [
            "Try to more directly address what the question is asking for.",
        ]
        missing_points.append("Walk through a concrete example input and trace your logic by hand.")

    return score, is_correct, feedback, missing_points


def _grade_coding(question, request_data):
    answer = str(request_data.get("answer", "")).strip()

    if not answer:
        return None, {"error": "answer is required."}

    ai_result = None
    if question.sample_solution:
        try:
            ai_result = ai.evaluate_coding_answer(
                question.question,
                question.sample_solution,
                answer,
            )
        except Exception:
            ai_result = None

    if ai_result:
        score = max(0, min(100, int(ai_result.get("score", 0))))
        is_correct = bool(ai_result.get("is_correct", score >= 70))
        feedback = ai_result.get("feedback") or "Answer recorded."
        missing_points = ai_result.get("missing_points") or []
    else:
        score, is_correct, feedback, missing_points = _heuristic_grade_coding(
            answer, question.sample_solution, question.question
        )

    question.answer = answer
    question.is_correct = is_correct
    question.score = score
    question.feedback = feedback
    question.improvement_tips = missing_points
    return question, None


def _grade_open(question, request_data):
    answer = str(request_data.get("answer", "")).strip()

    if not answer:
        return None, {"error": "Answer is required."}

    # Rule-based evaluation (kept simple and transparent).
    word_count = len(answer.split())

    if word_count >= 80:
        score = 90
    elif word_count >= 50:
        score = 80
    elif word_count >= 25:
        score = 70
    elif word_count >= 10:
        score = 60
    else:
        score = 40

    question.answer = answer
    question.score = score
    question.is_correct = score >= 70
    question.feedback = (
        "Your answer has been recorded. "
        "For a stronger interview answer, "
        "include a clear explanation, an example "
        "and connect it to the job requirements."
    )
    question.improvement_tips = [
        "Give a structured answer.",
        "Include a practical example.",
        "Connect your answer to the target role.",
    ]
    return question, None


class SubmitInterviewAnswerView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):

        try:

            question = InterviewQuestion.objects.select_related(
                "session"
            ).get(
                id=question_id,
                session__user=request.user
            )

        except InterviewQuestion.DoesNotExist:

            return Response(
                {
                    "error": "Interview question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if question.question_type == "mcq":
            question, error = _grade_mcq(question, request.data)
        elif question.question_type == "coding":
            question, error = _grade_coding(question, request.data)
        else:
            question, error = _grade_open(question, request.data)

        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        question.answered_at = timezone.now()
        question.save()

        session = question.session

        answered_count = session.questions.filter(
            answer__isnull=False
        ).exclude(
            answer=""
        ).count()

        scores = list(
            session.questions.filter(
                score__isnull=False
            ).values_list(
                "score",
                flat=True
            )
        )

        session.questions_answered = answered_count

        if scores:
            session.overall_score = round(
                sum(float(score) for score in scores)
                / len(scores),
                2
            )

        roadmap_result = None

        if answered_count >= session.total_questions:
            session.status = "completed"

        session.save()

        if session.status == "completed" and session.roadmap_item_id:
            item = RoadmapItem.objects.select_related("roadmap").get(id=session.roadmap_item_id)
            score = float(session.overall_score or 0)
            passed = score >= item.mock_pass_score

            if passed:
                item.mock_completed = True
                item.status = "completed"
                item.save(update_fields=["mock_completed", "status", "updated_at"])

                roadmap = item.roadmap
                if not roadmap.items.exclude(status="completed").exists():
                    roadmap.status = "completed"
                    roadmap.save(update_fields=["status", "updated_at"])

            roadmap_result = {
                "roadmap_item_id": item.id,
                "passed": passed,
                "pass_score": item.mock_pass_score,
                "score": score,
                "message": (
                    "Mock passed. This roadmap skill is now completed."
                    if passed
                    else "Mock not passed yet. Review the weak areas and retry."
                ),
            }

        return Response(
            {
                "message": "Answer submitted successfully.",
                "question_id": question.id,
                "question_type": question.question_type,
                "is_correct": question.is_correct,
                "correct_option": question.correct_option,
                "sample_solution": question.sample_solution,
                "explanation": question.explanation,
                "score": question.score,
                "feedback": question.feedback,
                "improvement_tips": question.improvement_tips,
                "questions_answered": session.questions_answered,
                "overall_score": session.overall_score,
                "session_status": session.status,
                "roadmap_result": roadmap_result,
            }
        )

def _build_interview_analysis(session):
    """
    Build one consistent analysis payload for both the
    analysis endpoint and the final-answer response.
    """

    answered = [
        question
        for question in session.questions.all()
        if question.answered_at
    ]

    def _bucket(question_type):

        items = [
            question
            for question in answered
            if question.question_type ==
            question_type
        ]

        if not items:

            return {
                "count": 0,
                "average_score": None,
                "correct": 0,
            }

        scores = [
            float(question.score)
            for question in items
            if question.score is not None
        ]

        correct = sum(
            1
            for question in items
            if question.is_correct
        )

        return {
            "count": len(items),
            "average_score":
                round(
                    sum(scores) /
                    len(scores),
                    2,
                )
                if scores
                else None,
            "correct":
                correct,
        }

    by_type = {
        "mcq":
            _bucket("mcq"),
        "coding":
            _bucket("coding"),
        "open":
            _bucket("open"),
    }

    skill_scores = {}

    for question in answered:

        if (
            not question.related_skill
            or question.score is None
        ):
            continue

        skill_scores.setdefault(
            question.related_skill,
            [],
        ).append(
            float(question.score)
        )

    skill_breakdown = [
        {
            "skill":
                skill,
            "average_score":
                round(
                    sum(scores) /
                    len(scores),
                    2,
                ),
            "questions":
                len(scores),
        }
        for skill, scores
        in skill_scores.items()
    ]

    skill_breakdown.sort(
        key=lambda item:
            item["average_score"]
    )

    strong_skills = [
        item["skill"]
        for item in skill_breakdown
        if item["average_score"] >= 75
    ]

    weak_skills = [
        item["skill"]
        for item in skill_breakdown
        if item["average_score"] < 60
    ]

    coding_items = [
        question
        for question in answered
        if question.question_type ==
        "coding"
    ]

    coding_average = (
        by_type["coding"]
        ["average_score"]
    )

    if not answered:

        summary = (
            "Answer some questions to see "
            "your performance analysis here."
        )

    elif weak_skills:

        summary = (
            f"Focus next on "
            f"{', '.join(weak_skills[:3])}. "
            "These were the weakest areas "
            "in this session. Your strongest "
            "area so far is "
            f"{strong_skills[0] if strong_skills else 'still developing'}."
        )

    elif (
        coding_items
        and coding_average is not None
        and coding_average < 70
    ):

        summary = (
            f"Your coding performance averaged "
            f"{coding_average}%. Review the coding "
            "feedback and practice the underlying "
            "logic before your next attempt."
        )

    elif session.overall_score is not None:

        summary = (
            f"You completed the interview with "
            f"an overall score of "
            f"{session.overall_score}%. "
            "Keep practicing the areas shown "
            "below to improve consistency."
        )

    else:

        summary = (
            "Your interview has been completed. "
            "Review the breakdown below."
        )

    return {
        "session_id":
            session.id,

        "session_type":
            session.session_type,

        "overall_score":
            session.overall_score,

        "questions_answered":
            session.questions_answered,

        "total_questions":
            session.total_questions,

        "status":
            session.status,

        "by_type":
            by_type,

        "skill_breakdown":
            skill_breakdown,

        "strong_skills":
            strong_skills,

        "weak_skills":
            weak_skills,

        "summary":
            summary,
    }
class InterviewAnalysisView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):

        try:
            session = InterviewSession.objects.prefetch_related("questions").get(
                id=session_id,
                user=request.user,
            )
        except InterviewSession.DoesNotExist:
            return Response(
                {"error": "Interview session not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        answered = [q for q in session.questions.all() if q.answered_at]

        def _bucket(qtype):
            items = [q for q in answered if q.question_type == qtype]
            if not items:
                return {"count": 0, "average_score": None, "correct": 0}
            scores = [float(q.score) for q in items if q.score is not None]
            correct = sum(1 for q in items if q.is_correct)
            return {
                "count": len(items),
                "average_score": round(sum(scores) / len(scores), 2) if scores else None,
                "correct": correct,
            }

        by_type = {
            "mcq": _bucket("mcq"),
            "coding": _bucket("coding"),
            "open": _bucket("open"),
        }

        skill_scores = {}
        for q in answered:
            if not q.related_skill or q.score is None:
                continue
            skill_scores.setdefault(q.related_skill, []).append(float(q.score))

        skill_breakdown = [
            {
                "skill": skill,
                "average_score": round(sum(scores) / len(scores), 2),
                "questions": len(scores),
            }
            for skill, scores in skill_scores.items()
        ]
        skill_breakdown.sort(key=lambda x: x["average_score"])

        strong_skills = [s["skill"] for s in skill_breakdown if s["average_score"] >= 75]
        weak_skills = [s["skill"] for s in skill_breakdown if s["average_score"] < 60]

        if not answered:
            summary = "Answer some questions to see your performance analysis here."
        elif weak_skills:
            summary = (
                f"Focus next on {', '.join(weak_skills[:3])} — these scored lowest in this session. "
                f"Your strongest area so far is {strong_skills[0] if strong_skills else 'still developing'}."
            )
        else:
            summary = "Solid performance across the board. Keep practicing to maintain this level."

        return Response({
            "session_id": session.id,
            "session_type": session.session_type,
            "overall_score": session.overall_score,
            "questions_answered": session.questions_answered,
            "total_questions": session.total_questions,
            "status": session.status,
            "by_type": by_type,
            "skill_breakdown": skill_breakdown,
            "strong_skills": strong_skills,
            "weak_skills": weak_skills,
            "summary": summary,
        })


class QuestionBankCatalogView(APIView):
    """Return the full Role -> Skill -> Topic hierarchy."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"catalog": get_role_catalog()})


class QuestionBankCategoriesView(APIView):
    """Backward-compatible endpoint for older frontend builds."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        catalog = get_role_catalog()
        categories = []
        for category in catalog:
            for role in category["roles"]:
                categories.append({"id": role["id"], "label": role["name"]})
        return Response({"categories": categories, "catalog": catalog})


class QuestionBankView(APIView):
    """Return cached/generated questions for a selected Role -> Skill -> Topic."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        role_id = (request.query_params.get("role_id") or "").strip().lower()
        skill = (request.query_params.get("skill") or "").strip()
        topic = (request.query_params.get("topic") or "").strip()
        difficulty = (request.query_params.get("difficulty") or "medium").strip().lower()
        question_type = (request.query_params.get("question_type") or "mixed").strip().lower()

        if not role_id or not skill or not topic:
            return Response(
                {"error": "role_id, skill and topic are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            count = max(1, min(int(request.query_params.get("count", 12)), 20))
        except (TypeError, ValueError):
            count = 12

        try:
            role = get_role(role_id)
            if not role:
                raise ValueError("Unknown job role.")
            questions = get_question_bank_set(
                role_id, skill, topic, difficulty, count, question_type, user=request.user
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "role": {"id": role["id"], "name": role["name"]},
            "skill": skill,
            "topic": topic,
            "difficulty": difficulty,
            "question_type": question_type,
            "count": len(questions),
            "questions": questions,
        })
