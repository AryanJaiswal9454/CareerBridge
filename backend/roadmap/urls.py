from django.urls import path

from .views import (
    GenerateRoadmapView,
    RoadmapListView,
    StartRoadmapItemView,
    SaveLearningProgressView,
    CompleteLearningView,
    StartRoadmapMockView,
    UpdateRoadmapItemView,
)


urlpatterns = [

    path(
        "generate/",
        GenerateRoadmapView.as_view(),
        name="generate-roadmap",
    ),

    path(
        "",
        RoadmapListView.as_view(),
        name="roadmap-list",
    ),

    path(
        "items/<int:item_id>/start/",
        StartRoadmapItemView.as_view(),
        name="start-roadmap-item",
    ),

    path(
        "items/<int:item_id>/progress/",
        SaveLearningProgressView.as_view(),
        name="save-learning-progress",
    ),

    path(
        "items/<int:item_id>/learning-complete/",
        CompleteLearningView.as_view(),
        name="complete-learning",
    ),

    path(
        "items/<int:item_id>/mock/start/",
        StartRoadmapMockView.as_view(),
        name="start-roadmap-mock",
    ),

    path(
        "items/<int:item_id>/",
        UpdateRoadmapItemView.as_view(),
        name="update-roadmap-item",
    ),
]