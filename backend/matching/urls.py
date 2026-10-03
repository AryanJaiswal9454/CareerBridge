
from django.urls import path

from .views import (
    MatchResultsView,
    MatchResumeToJobView,
    ResumeOptimizationView,
    ResumeTemplatesView,
    TailoredResumeView,
    TailoredResumeDownloadView,
)


urlpatterns = [
    path(
        "",
        MatchResultsView.as_view(),
        name="match-results",
    ),

    path(
        "match/",
        MatchResumeToJobView.as_view(),
        name="match-resume-job",
    ),

    path(
        "templates/",
        ResumeTemplatesView.as_view(),
        name="resume-templates",
    ),

    path(
        "<int:match_id>/optimize/",
        ResumeOptimizationView.as_view(),
        name="resume-optimize",
    ),

    path(
        "<int:match_id>/tailored-resume/",
        TailoredResumeView.as_view(),
        name="tailored-resume",
    ),

    path(
        "<int:match_id>/tailored-resume/download/",
        TailoredResumeDownloadView.as_view(),
        name="tailored-resume-download",
    ),
]

