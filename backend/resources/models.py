from django.contrib.auth.models import User
from django.db import models


class CommunityResource(models.Model):
    """A learning link contributed by one user and shown to everyone
    studying the same skill — alongside the curated YouTube/docs links.
    """

    RESOURCE_TYPE_CHOICES = [
        ("video", "Video"),
        ("doc", "Documentation"),
        ("article", "Article"),
        ("course", "Course"),
        ("other", "Other"),
    ]

    skill = models.CharField(max_length=150, db_index=True)

    title = models.CharField(max_length=200)

    url = models.URLField(max_length=500)

    note = models.CharField(max_length=300, blank=True)

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        default="other",
    )

    submitted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submitted_resources",
    )

    upvotes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-upvotes", "-created_at"]

    def __str__(self):
        return f"{self.skill}: {self.title}"
