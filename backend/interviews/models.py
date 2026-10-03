from django.db import models
from django.contrib.auth.models import User

from resumes.models import Resume
from careers.models import JobDescription
from matching.models import MatchResult


class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    match_result = models.ForeignKey(MatchResult, on_delete=models.CASCADE)

    roadmap_item = models.ForeignKey(
        "roadmap.RoadmapItem",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="interview_sessions",
    )

    SESSION_TYPES = [
        ("mcq", "MCQ Round"),
        ("technical", "Technical Round"),
        ("behavioral", "Behavioral"),
        ("mixed", "Mixed"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interview_sessions"
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="interview_sessions"
    )

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name="interview_sessions"
    )

    match_result = models.ForeignKey(
        MatchResult,
        on_delete=models.CASCADE,
        related_name="interview_sessions"
    )

    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPES,
        default="mixed"
    )

    total_questions = models.PositiveIntegerField(
        default=5
    )

    questions_answered = models.PositiveIntegerField(
        default=0
    )

    overall_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Interview {self.id} - {self.user.username}"


class InterviewQuestion(models.Model):

    CATEGORY_CHOICES = [
        ("technical", "Technical"),
        ("behavioral", "Behavioral"),
        ("resume", "Resume"),
        ("situational", "Situational"),
    ]

    QUESTION_TYPE_CHOICES = [
        ("mcq", "Multiple Choice"),
        ("coding", "Coding"),
        ("open", "Open Ended"),
    ]

    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="technical"
    )

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default="open"
    )

    related_skill = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    expected_points = models.JSONField(
        default=list
    )

    # MCQ-specific fields
    options = models.JSONField(
        default=list,
        blank=True
    )

    correct_option = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    selected_option = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # Coding-specific fields
    starter_code = models.TextField(
        blank=True,
        null=True
    )

    language = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    sample_solution = models.TextField(
        blank=True,
        null=True
    )

    is_correct = models.BooleanField(
        null=True,
        blank=True
    )

    explanation = models.TextField(
        blank=True,
        null=True
    )

    answer = models.TextField(
        blank=True,
        null=True
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    feedback = models.TextField(
        blank=True,
        null=True
    )

    improvement_tips = models.JSONField(
        default=list
    )

    answered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Question {self.id} - Interview {self.session.id}"

class QuestionBankQuestion(models.Model):
    """Cached question-bank item generated/curated for a role-skill-topic path.

    The hash prevents the same generated question from being stored twice,
    allowing Gemini to be used for variety without generating on every click.
    """

    SOURCE_CHOICES = [
        ("ai", "AI Generated"),
        ("fallback", "Local Fallback"),
        ("curated", "Curated"),
    ]

    role_id = models.CharField(max_length=100)
    role_name = models.CharField(max_length=150)
    skill = models.CharField(max_length=150)
    topic = models.CharField(max_length=180)
    difficulty = models.CharField(max_length=20, default="medium")
    question_type = models.CharField(max_length=20, default="conceptual")
    question = models.TextField()
    options = models.JSONField(default=list, blank=True)
    correct_option = models.CharField(max_length=10, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    starter_code = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    sample_solution = models.TextField(blank=True, null=True)
    model_answer = models.TextField(blank=True, null=True)
    key_points = models.JSONField(default=list, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="ai")
    question_hash = models.CharField(max_length=64, unique=True)
    seen_by = models.ManyToManyField(
        User,
        blank=True,
        related_name="seen_question_bank_questions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["role_id", "skill", "topic", "difficulty"]),
            models.Index(fields=["question_type", "difficulty"]),
        ]

    def __str__(self):
        return f"{self.role_name} · {self.skill} · {self.topic}"
