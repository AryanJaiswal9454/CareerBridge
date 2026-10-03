from django.db import models
from django.contrib.auth.models import User

from resumes.models import Resume
from careers.models import JobDescription
from matching.models import MatchResult


class Roadmap(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("paused", "Paused"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="roadmaps"
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="roadmaps"
    )

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name="roadmaps"
    )

    match_result = models.OneToOneField(
        MatchResult,
        on_delete=models.CASCADE,
        related_name="roadmap"
    )

    title = models.CharField(max_length=250)

    summary = models.TextField(blank=True)

    total_days = models.PositiveIntegerField(default=30)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class RoadmapItem(models.Model):

    CATEGORY_CHOICES = [
        ("improve", "Improve"),
        ("missing", "Missing"),
        ("preferred", "Preferred"),
    ]

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="items"
    )

    skill = models.CharField(max_length=150)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    current_level = models.CharField(
        max_length=50,
        default="Not Available"
    )

    target_level = models.CharField(
        max_length=50,
        default="Intermediate"
    )

    reason = models.TextField()

    learning_topics = models.JSONField(default=list)

    practice_tasks = models.JSONField(default=list)

    project_task = models.TextField(blank=True)

    estimated_days = models.PositiveIntegerField(default=5)

    resources = models.JSONField(default=list, blank=True)
        # AI-generated learning module for this roadmap item
    learning_content = models.JSONField(default=dict, blank=True)

    # Stores which learning checklist steps the student has completed
    completed_learning_steps = models.JSONField(default=list, blank=True)

    # Learning lifecycle timestamps
    learning_started_at = models.DateTimeField(null=True, blank=True)
    learning_completed_at = models.DateTimeField(null=True, blank=True)

    # Targeted mock interview configuration
    mock_pass_score = models.PositiveIntegerField(default=70)
    mock_completed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started"
    )

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.skill} - {self.category}"