
from django.urls import path

from .views import (
    ProfileView,
    SkillsView,
    SkillDetailView,
)


urlpatterns = [
    path(
        "",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "skills/",
        SkillsView.as_view(),
        name="skills",
    ),

    path(
        "skills/<int:skill_id>/",
        SkillDetailView.as_view(),
        name="skill-detail",
    ),
]

