from django.db import models
from django.contrib.auth.models import User


class JobDescription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_descriptions"
    )

    company_name = models.CharField(max_length=200)

    job_title = models.CharField(max_length=200)

    source_type = models.CharField(
        max_length=20,
        choices=[
            ("text", "Text"),
            ("file", "File")
        ],
        default="text"
    )

    file = models.FileField(
        upload_to="job_descriptions/",
        blank=True,
        null=True
    )

    description = models.TextField()

    extracted_text = models.TextField(
        blank=True,
        null=True
    )

    ai_analysis = models.JSONField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )