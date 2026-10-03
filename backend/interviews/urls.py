from django.urls import path

from .views import (
    CreateInterviewSessionView,
    InterviewSessionListView,
    SubmitInterviewAnswerView,
    InterviewAnalysisView,
    QuestionBankCatalogView,
    QuestionBankCategoriesView,
    QuestionBankView,
)

urlpatterns = [
    path("", InterviewSessionListView.as_view(), name="interview-list"),
    path("create/", CreateInterviewSessionView.as_view(), name="interview-create"),
    path("questions/<int:question_id>/answer/", SubmitInterviewAnswerView.as_view(), name="interview-answer"),
    path("<int:session_id>/analysis/", InterviewAnalysisView.as_view(), name="interview-analysis"),

    path("question-bank/catalog/", QuestionBankCatalogView.as_view(), name="question-bank-catalog"),
    path("question-bank/categories/", QuestionBankCategoriesView.as_view(), name="question-bank-categories"),
    path("question-bank/", QuestionBankView.as_view(), name="question-bank"),
]
