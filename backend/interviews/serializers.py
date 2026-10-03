from rest_framework import serializers

from .models import (
    InterviewSession,
    InterviewQuestion,
)


class InterviewQuestionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = InterviewQuestion

        fields = [
            "id",
            "question",
            "category",
            "question_type",
            "related_skill",
            "options",
            "starter_code",
            "language",
            "answer",
            "selected_option",
            "is_correct",
            "score",
            "feedback",
            "correct_option",
            "sample_solution",
            "explanation",
            "expected_points",
            "improvement_tips",
            "answered_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Only reveal the correct answer / model solution / explanation
        # once the candidate has actually submitted an answer.
        if not instance.answered_at:
            data["correct_option"] = None
            data["sample_solution"] = None
            data["explanation"] = None
            data["is_correct"] = None
        return data


class InterviewSessionSerializer(
    serializers.ModelSerializer
):

    questions = InterviewQuestionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = InterviewSession

        fields = [
            "id",
            "resume",
            "job_description",
            "match_result",
            "roadmap_item",
            "session_type",
            "total_questions",
            "questions_answered",
            "overall_score",
            "status",
            "questions",
            "created_at",
            "updated_at",
        ]
