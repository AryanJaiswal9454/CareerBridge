from django.urls import path
from .views import ResumeView, ResumeAnalyzeView, ResumeATSScoreView, ResumeGenerateView

urlpatterns = [
    path("", ResumeView.as_view(), name="resumes"),
    path("generate/", ResumeGenerateView.as_view(), name="resume-generate"),
    path("<int:pk>/analyze/", ResumeAnalyzeView.as_view(), name="resume-analyze"),
    path("<int:pk>/ats-score/", ResumeATSScoreView.as_view(), name="resume-ats-score"),
]