from django.urls import path
from .views import JobDescriptionView, JobDescriptionAnalyzeView

urlpatterns = [
    path("", JobDescriptionView.as_view(), name="job-descriptions"),
    path("<int:job_id>/analyze/", JobDescriptionAnalyzeView.as_view(), name="job-description-analyze"),
]
