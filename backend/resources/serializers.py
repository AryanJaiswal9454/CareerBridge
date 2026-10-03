from rest_framework import serializers

from .models import CommunityResource


class CommunityResourceSerializer(serializers.ModelSerializer):

    submitted_by_username = serializers.CharField(
        source="submitted_by.username",
        read_only=True,
    )

    class Meta:
        model = CommunityResource
        fields = [
            "id",
            "skill",
            "title",
            "url",
            "note",
            "resource_type",
            "submitted_by_username",
            "upvotes",
            "created_at",
        ]
        read_only_fields = ["id", "submitted_by_username", "upvotes", "created_at"]
