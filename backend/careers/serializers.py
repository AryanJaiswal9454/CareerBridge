from rest_framework import serializers
from .models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDescription
        fields = [
            "company_name",
            "job_title",
            "source_type",
            "file",
            "description",
        ]