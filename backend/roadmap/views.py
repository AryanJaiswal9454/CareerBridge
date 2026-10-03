from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from matching.models import MatchResult
from interviews.models import InterviewSession, InterviewQuestion
from interviews.engine import (
    generate_targeted_interview_questions,
    get_role,
)

from .models import Roadmap, RoadmapItem
from .serializers import RoadmapSerializer, RoadmapItemSerializer
from .engine import create_roadmap_data


def _find_role_for_item(item):
    """Find a role that supports the roadmap item's exact skill."""
    job_title = (item.roadmap.job_description.job_title or "").strip().lower()
    skill = (item.skill or "").strip().lower()

    candidates = [
        "python-developer", "data-analyst", "software-developer",
        "django-developer", "full-stack-developer", "backend-developer",
        "frontend-developer", "react-developer", "data-scientist",
        "ml-engineer", "ai-engineer", "sql-developer",
    ]

    def supports_skill(role):
        return bool(role) and any(
            str(role_skill).strip().lower() == skill
            for role_skill in role.get("skills", {})
        )

    # Prefer the job-title role only when it also supports the roadmap skill.
    for role_id in candidates:
        role = get_role(role_id)
        if role and role["name"].strip().lower() in job_title and supports_skill(role):
            return role_id

    # Otherwise use any catalog role that supports this skill.
    for role_id in candidates:
        role = get_role(role_id)
        if supports_skill(role):
            return role_id

    # Skill is outside the fixed role catalog; the caller will use a safe
    # deterministic targeted-question fallback.
    return None


def _fallback_targeted_questions(skill, topic, role_name, limit=6):
    """Create deterministic targeted questions when the catalog cannot be used."""
    skill = skill or "General skill"
    topic = topic or skill
    role_name = role_name or "candidate"

    templates = [
        f"Explain {topic} in the context of {skill}. What problem does it solve and give one practical example?",
        f"What is one common mistake when working with {topic}, and how would you detect and prevent it?",
        f"As a {role_name}, how would you decide between two approaches involving {topic}? Explain the trade-off.",
        f"Describe a realistic project task where {topic} would be useful. Explain the steps you would take.",
        f"What edge case should you test first when implementing a feature involving {topic}? Why?",
        f"How would you explain {topic} to a teammate who understands {skill} basics but has not used {topic} before?",
    ]

    return [
        {
            "question": question,
            "category": "technical",
            "question_type": "open",
            "related_skill": skill,
            "expected_points": [
                f"Understand {topic}",
                "Explain the reasoning clearly",
                "Give a practical example",
            ],
            "options": [],
            "correct_option": None,
            "starter_code": None,
            "language": None,
            "sample_solution": None,
            "explanation": f"Focus your answer on {topic}, practical reasoning, and a concrete example.",
        }
        for question in templates[:limit]
    ]


def _topic_for_item(item, role):

    content = item.learning_content or {}

    candidates = (
        content.get("concepts")
        or content.get("learning_objectives")
        or item.learning_topics
        or []
    )

    role_skills = (
        role.get("skills", {})
        if role
        else {}
    )

    skill_topics = []

    for role_skill, topics in role_skills.items():

        if (
            role_skill.lower()
            == item.skill.lower()
        ):
            skill_topics = topics
            break

    if skill_topics:

        for candidate in candidates:

            for topic in skill_topics:

                if (
                    topic.lower()
                    == str(candidate).lower()
                ):
                    return topic

        return skill_topics[0]

    return (
        skill_topics[0]
        if skill_topics
        else (
            candidates[0]
            if candidates
            else item.skill
        )
    )


def _get_checklist(item):

    content = item.learning_content or {}

    return (
        content.get("completion_checklist")
        or content.get("topic_checklist")
        or item.learning_topics
        or []
    )


class GenerateRoadmapView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        match_id = request.data.get("match_id")

        if not match_id:

            return Response(
                {
                    "error":
                        "match_id is required."
                },
                status=400,
            )

        try:

            match_result = MatchResult.objects.get(
                id=match_id,
                user=request.user,
            )

        except MatchResult.DoesNotExist:

            return Response(
                {
                    "error":
                        "Match result not found."
                },
                status=404,
            )

        try:
            existing_roadmap = (
                Roadmap.objects
                .prefetch_related("items")
                .filter(match_result=match_result, user=request.user)
                .first()
            )

            if existing_roadmap:
                return Response({
                    "message": "Saved roadmap loaded.",
                    "roadmap": RoadmapSerializer(existing_roadmap).data,
                    "existing": True,
                })

            # Only call the AI/roadmap engine when this exact match has no
            # saved roadmap yet. Re-opening the roadmap must not spend an
            # AI call or replace the student's saved progress.
            roadmap_data = create_roadmap_data(match_result)

            with transaction.atomic():
                roadmap = Roadmap.objects.create(
                    user=request.user,
                    resume=match_result.resume,
                    job_description=match_result.job_description,
                    match_result=match_result,
                    title=roadmap_data["title"],
                    summary=roadmap_data["summary"],
                    total_days=roadmap_data["total_days"],
                    status="active",
                )

                for index, item in enumerate(
                    roadmap_data["items"],
                    start=1,
                ):

                    RoadmapItem.objects.create(
                        roadmap=roadmap,
                        skill=item["skill"],
                        category=item["category"],
                        priority=item["priority"],
                        current_level=item[
                            "current_level"
                        ],
                        target_level=item[
                            "target_level"
                        ],
                        reason=item["reason"],
                        learning_topics=item.get(
                            "learning_topics",
                            [],
                        ),
                        practice_tasks=item.get(
                            "practice_tasks",
                            [],
                        ),
                        project_task=item.get(
                            "project_task",
                            "",
                        ),
                        estimated_days=item.get(
                            "estimated_days",
                            5,
                        ),
                        resources=item.get(
                            "resources",
                            [],
                        ),
                        learning_content=item.get(
                            "learning_content",
                            {},
                        ),
                        completed_learning_steps=[],
                        mock_pass_score=item.get(
                            "mock_pass_score",
                            70,
                        ),
                        mock_completed=False,
                        status="not_started",
                        order=index,
                    )

            return Response(
                {
                    "message":
                        "Roadmap generated successfully.",
                    "roadmap":
                        RoadmapSerializer(
                            roadmap
                        ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as exc:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "error":
                        "Roadmap generation failed.",
                    "details": str(exc),
                },
                status=500,
            )


class RoadmapListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        roadmaps = (
            Roadmap.objects
            .filter(user=request.user)
            .prefetch_related("items")
        )

        return Response(
            {
                "count":
                    roadmaps.count(),
                "roadmaps":
                    RoadmapSerializer(
                        roadmaps,
                        many=True,
                    ).data,
            }
        )


class StartRoadmapItemView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):

        try:

            item = RoadmapItem.objects.get(
                id=item_id,
                roadmap__user=request.user,
            )

        except RoadmapItem.DoesNotExist:

            return Response(
                {
                    "error":
                        "Roadmap item not found."
                },
                status=404,
            )

        if item.status == "completed":

            return Response(
                {
                    "error":
                        "This roadmap item is already completed."
                },
                status=400,
            )

        if not item.learning_started_at:

            item.learning_started_at = (
                timezone.now()
            )

        item.status = "in_progress"

        item.save(
            update_fields=[
                "learning_started_at",
                "status",
                "updated_at",
            ]
        )

        return Response(
            {
                "message":
                    "Learning module started.",
                "item":
                    RoadmapItemSerializer(
                        item
                    ).data,
            }
        )


class SaveLearningProgressView(APIView):

    permission_classes = [IsAuthenticated]

    def _save(self, request, item_id):
        try:
            item = RoadmapItem.objects.get(
                id=item_id,
                roadmap__user=request.user,
            )
        except RoadmapItem.DoesNotExist:
            return Response({"error": "Roadmap item not found."}, status=404)

        # Accept both names used by older/newer frontend versions.
        raw_steps = request.data.get("completed_steps", None)
        if raw_steps is None:
            raw_steps = request.data.get("completed_learning_steps", [])

        if not isinstance(raw_steps, list):
            return Response({"error": "completed_steps must be a list."}, status=400)

        checklist = _get_checklist(item)
        valid = []

        for value in raw_steps:
            # New format: checklist index.
            try:
                index = int(value)
                if 0 <= index < len(checklist):
                    valid.append(index)
                    continue
            except (TypeError, ValueError):
                pass

            # Backward compatibility: older UI stored the checklist text.
            if isinstance(value, str):
                normalized = value.strip().casefold()
                for idx, topic in enumerate(checklist):
                    if str(topic).strip().casefold() == normalized:
                        valid.append(idx)
                        break

        valid = sorted(set(valid))
        item.completed_learning_steps = valid

        if not item.learning_started_at:
            item.learning_started_at = timezone.now()
        if item.status != "completed":
            item.status = "in_progress"

        item.save(update_fields=[
            "completed_learning_steps",
            "learning_started_at",
            "status",
            "updated_at",
        ])
        item.refresh_from_db()

        return Response({
            "item": RoadmapItemSerializer(item).data,
            "saved_steps": valid,
            "total_steps": len(checklist),
        })

    def post(self, request, item_id):
        return self._save(request, item_id)

    def patch(self, request, item_id):
        return self._save(request, item_id)


class CompleteLearningView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            item = RoadmapItem.objects.get(
                id=item_id, roadmap__user=request.user
            )
        except RoadmapItem.DoesNotExist:
            return Response({"error": "Roadmap item not found."}, status=404)

        checklist = _get_checklist(item)
        completed = set()
        for value in (item.completed_learning_steps or []):
            try:
                index = int(value)
                if 0 <= index < len(checklist):
                    completed.add(index)
            except (TypeError, ValueError):
                normalized = str(value).strip().casefold()
                for idx, topic in enumerate(checklist):
                    if str(topic).strip().casefold() == normalized:
                        completed.add(idx)
                        break

        required = set(range(len(checklist)))
        missing = sorted(required - completed)

        if missing:
            return Response({
                "error": "Complete every learning checklist step before unlocking the mock interview.",
                "missing_steps": missing,
                "missing_topics": [checklist[i] for i in missing],
                "learning_progress": round((len(completed) / len(required)) * 100) if required else 100,
            }, status=400)

        now = timezone.now()
        item.completed_learning_steps = sorted(completed)
        item.learning_completed_at = now
        item.status = "in_progress"
        item.save(update_fields=[
            "completed_learning_steps",
            "learning_completed_at",
            "status",
            "updated_at",
        ])

        return Response({
            "message": "Learning completed. Targeted mock interview unlocked.",
            "item": RoadmapItemSerializer(item).data,
        })


class StartRoadmapMockView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):

        try:

            item = (
                RoadmapItem.objects
                .select_related(
                    "roadmap",
                    "roadmap__match_result",
                    "roadmap__resume",
                    "roadmap__job_description",
                )
                .get(
                    id=item_id,
                    roadmap__user=request.user,
                )
            )

        except RoadmapItem.DoesNotExist:

            return Response(
                {
                    "error":
                        "Roadmap item not found."
                },
                status=404,
            )

        if not item.learning_completed_at:

            return Response(
                {
                    "error": (
                        "Complete the learning "
                        "module before starting "
                        "the mock interview."
                    )
                },
                status=400,
            )

        if item.mock_completed:

            return Response(
                {
                    "error": (
                        "This roadmap item has "
                        "already passed its mock interview."
                    )
                },
                status=400,
            )

        role_id = _find_role_for_item(item)

        role = get_role(role_id) if role_id else None

        topic = _topic_for_item(
            item,
            role,
        )

        existing = (
            item.interview_sessions
            .filter(status="active")
            .order_by("-created_at")
            .first()
        )

        if existing:

            from interviews.serializers import (
                InterviewSessionSerializer,
            )

            return Response(
                {
                    "session":
                        InterviewSessionSerializer(
                            existing
                        ).data,
                    "resumed": True,
                }
            )

        questions = []

        if role_id:
            try:
                questions = generate_targeted_interview_questions(
                    role_id=role_id,
                    skill=item.skill,
                    topic=topic,
                    difficulty="medium",
                    session_type="mixed",
                    limit=6,
                    user=request.user,
                ) or []
            except Exception:
                questions = []

        # Never make a completed roadmap item unusable because its skill is
        # outside the fixed role catalog or an external AI call failed.
        if not questions:
            questions = _fallback_targeted_questions(
                skill=item.skill,
                topic=topic,
                role_name=role["name"] if role else item.roadmap.job_description.job_title,
                limit=6,
            )

        match_result = (
            item.roadmap.match_result
        )

        session = (
            InterviewSession.objects.create(
                user=request.user,
                resume=item.roadmap.resume,
                job_description=(
                    item.roadmap.job_description
                ),
                match_result=match_result,
                roadmap_item=item,
                session_type="mixed",
                total_questions=len(
                    questions
                ),
            )
        )

        for question_data in questions:

            InterviewQuestion.objects.create(
                session=session,
                question=question_data[
                    "question"
                ],
                category=question_data.get(
                    "category",
                    "technical",
                ),
                question_type=question_data.get(
                    "question_type",
                    "open",
                ),
                related_skill=question_data.get(
                    "related_skill"
                ) or item.skill,
                expected_points=question_data.get(
                    "expected_points",
                    [],
                ),
                options=question_data.get(
                    "options",
                    [],
                ),
                correct_option=question_data.get(
                    "correct_option"
                ),
                starter_code=question_data.get(
                    "starter_code"
                ),
                language=question_data.get(
                    "language"
                ),
                sample_solution=question_data.get(
                    "sample_solution"
                ),
                explanation=question_data.get(
                    "explanation"
                ),
            )

        from interviews.serializers import (
            InterviewSessionSerializer,
        )

        return Response(
            {
                "message":
                    "Targeted mock interview created.",
                "session":
                    InterviewSessionSerializer(
                        session
                    ).data,
                "roadmap_item_id":
                    item.id,
                "target": {
                    "role_id":
                        role_id,
                    "skill":
                        item.skill,
                    "topic":
                        topic,
                },
            },
            status=201,
        )


class UpdateRoadmapItemView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):

        try:

            item = (
                RoadmapItem.objects
                .select_related("roadmap")
                .get(
                    id=item_id,
                    roadmap__user=request.user,
                )
            )

        except RoadmapItem.DoesNotExist:

            return Response(
                {
                    "error":
                        "Roadmap item not found."
                },
                status=404,
            )

        new_status = request.data.get(
            "status"
        )

        if new_status not in {
            "not_started",
            "in_progress",
            "completed",
        }:

            return Response(
                {
                    "error":
                        "Invalid roadmap status."
                },
                status=400,
            )

        if (
            new_status == "completed"
            and not item.mock_completed
        ):

            return Response(
                {
                    "error": (
                        "A roadmap item can only "
                        "be completed after passing "
                        "its targeted mock interview."
                    )
                },
                status=400,
            )

        if (
            new_status == "in_progress"
            and not item.learning_started_at
        ):

            item.learning_started_at = (
                timezone.now()
            )

        item.status = new_status

        item.save(
            update_fields=[
                "status",
                "learning_started_at",
                "updated_at",
            ]
        )

        return Response(
            {
                "message":
                    "Roadmap item updated successfully.",
                "item":
                    RoadmapItemSerializer(
                        item
                    ).data,
            }
        )