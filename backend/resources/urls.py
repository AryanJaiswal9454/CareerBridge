from django.urls import path

from .views import CommunityResourceListCreateView, CommunityResourceUpvoteView

urlpatterns = [
    path("", CommunityResourceListCreateView.as_view(), name="community-resources"),
    path("<int:resource_id>/upvote/", CommunityResourceUpvoteView.as_view(), name="community-resource-upvote"),
]
