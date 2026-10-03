from django.contrib import admin

from .models import InterviewSession, InterviewQuestion, QuestionBankQuestion


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "session_type", "status", "overall_score", "created_at"]
    list_filter = ["session_type", "status"]


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "session", "question_type", "related_skill", "score", "answered_at"]
    list_filter = ["question_type", "category"]


@admin.register(QuestionBankQuestion)
class QuestionBankQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "role_name", "skill", "topic", "difficulty", "question_type", "source", "created_at"]
    list_filter = ["difficulty", "question_type", "source"]
    search_fields = ["role_name", "skill", "topic", "question"]
