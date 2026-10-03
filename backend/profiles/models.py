from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    full_name = models.CharField(max_length=150)

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    college = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    degree = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    graduation_year = models.IntegerField(
        blank=True,
        null=True
    )

    career_goal = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.full_name
class Skill(models.Model):
    PROFICIENCY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(max_length=100)

    proficiency = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default="beginner"
    )

    years_of_experience = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.proficiency}"
class Education(models.Model):
    profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="education"
    )

    institution = models.CharField(max_length=200)

    degree = models.CharField(max_length=150)

    field_of_study = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    start_year = models.IntegerField(
        blank=True,
        null=True
    )

    end_year = models.IntegerField(
        blank=True,
        null=True
    )

    grade = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.degree} - {self.institution}"
class Project(models.Model):
    profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    technologies = models.TextField(
        blank=True,
        null=True
    )

    project_url = models.URLField(
        blank=True,
        null=True
    )

    github_url = models.URLField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
class Certification(models.Model):
    profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="certifications"
    )

    name = models.CharField(max_length=200)

    issuing_organization = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    issue_date = models.DateField(
        blank=True,
        null=True
    )

    credential_url = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name