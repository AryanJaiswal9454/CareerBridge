from rest_framework import serializers
from .models import Resume


class ResumeUploadSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Resume
        fields = ["title", "file"]

    def validate_file(self, value):
        allowed_extensions = (
            ".pdf",
            ".docx",
            ".txt"
        )

        if not value.name.lower().endswith(
            allowed_extensions
        ):
            raise serializers.ValidationError(
                "Only PDF, DOCX and TXT files are supported."
            )

        return value