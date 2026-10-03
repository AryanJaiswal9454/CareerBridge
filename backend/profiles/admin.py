from django.contrib import admin
from .models import (
    StudentProfile,
    Skill,
    Education,
    Project,
    Certification,
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "college",
        "degree",
        "graduation_year",
        "career_goal",
    )

    search_fields = (
        "full_name",
        "college",
        "career_goal",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "proficiency",
        "years_of_experience",
        "profile",
    )

    list_filter = ("proficiency",)
    search_fields = ("name",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "degree",
        "institution",
        "field_of_study",
        "start_year",
        "end_year",
        "grade",
    )

    search_fields = (
        "degree",
        "institution",
        "field_of_study",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "profile",
        "created_at",
    )

    search_fields = (
        "title",
        "technologies",
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "issuing_organization",
        "issue_date",
        "profile",
    )

    search_fields = (
        "name",
        "issuing_organization",
    )