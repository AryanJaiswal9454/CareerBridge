from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume
from careers.models import JobDescription


class MatchResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="match_results"
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="match_results"
    )

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name="match_results"
    )

    match_score = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    matched_skills = models.JSONField(
        default=list
    )

    skills_to_improve = models.JSONField(
        default=list
    )

    missing_skills = models.JSONField(
        default=list
    )

    preferred_skills_missing = models.JSONField(
        default=list
    )

    experience_match = models.BooleanField(
        default=False
    )

    education_match = models.BooleanField(
        default=False
    )

    optimization = models.JSONField(
        default=dict,
        blank=True
    )

    tailored_resume = models.JSONField(
        default=dict,
        blank=True
    )

    tailored_resume_history = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.job_description.job_title} - "
            f"{self.match_score}%"
        )