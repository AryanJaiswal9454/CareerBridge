from rest_framework import serializers

from .models import Roadmap, RoadmapItem


class RoadmapItemSerializer(serializers.ModelSerializer):
    learning_checklist = serializers.SerializerMethodField()
    learning_progress = serializers.SerializerMethodField()
    mock_unlocked = serializers.SerializerMethodField()
    completed_learning_steps = serializers.SerializerMethodField()

    class Meta:
        model = RoadmapItem
        fields = [
            "id", "skill", "category", "priority", "current_level", "target_level",
            "reason", "learning_topics", "practice_tasks", "project_task", "estimated_days",
            "resources", "learning_content", "completed_learning_steps", "learning_started_at",
            "learning_completed_at", "mock_pass_score", "mock_completed", "mock_unlocked",
            "learning_checklist", "learning_progress", "status", "order",
        ]

    def get_learning_checklist(self, obj):
        content = obj.learning_content or {}
        return (
            content.get("completion_checklist")
            or content.get("topic_checklist")
            or obj.learning_topics
            or []
        )

    def _completed_indexes(self, obj):
        checklist = self.get_learning_checklist(obj)
        indexes = set()
        for value in (obj.completed_learning_steps or []):
            try:
                index = int(value)
                if 0 <= index < len(checklist):
                    indexes.add(index)
                    continue
            except (TypeError, ValueError):
                pass
            if isinstance(value, str):
                normalized = value.strip().casefold()
                for index, topic in enumerate(checklist):
                    if str(topic).strip().casefold() == normalized:
                        indexes.add(index)
                        break
        return indexes

    def get_completed_learning_steps(self, obj):
        return sorted(self._completed_indexes(obj))

    def get_learning_progress(self, obj):
        checklist = self.get_learning_checklist(obj)
        if not checklist:
            return 100 if obj.learning_completed_at else 0
        completed = self._completed_indexes(obj)
        return round((len(completed) / len(checklist)) * 100)

    def get_mock_unlocked(self, obj):
        # The backend explicitly marks learning as complete only after every
        # checklist step has been saved. Use that lifecycle flag as the
        # single source of truth for unlocking the targeted mock.
        return bool(obj.learning_completed_at) and not obj.mock_completed


class RoadmapSerializer(serializers.ModelSerializer):
    items = RoadmapItemSerializer(many=True, read_only=True)

    class Meta:
        model = Roadmap
        fields = [
            "id", "resume", "job_description", "match_result", "title", "summary",
            "total_days", "status", "items", "created_at", "updated_at",
        ]
