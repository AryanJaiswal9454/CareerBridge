from django.db.models.signals import post_save
from django.dispatch import receiver

from interviews.models import InterviewSession


@receiver(
    post_save,
    sender=InterviewSession
)
def sync_roadmap_after_mock(
    sender,
    instance,
    **kwargs
):
    """
    A roadmap slab becomes completed only after
    its linked targeted mock has been completed
    and the student reaches the required score.
    """

    item = instance.roadmap_item

    if not item:
        return

    if instance.status != "completed":
        return

    score = float(
        instance.overall_score or 0
    )

    required_score = float(
        item.mock_pass_score or 70
    )

    if score >= required_score:

        if (
            not item.mock_completed
            or item.status != "completed"
        ):

            item.mock_completed = True
            item.status = "completed"

            item.save(
                update_fields=[
                    "mock_completed",
                    "status",
                    "updated_at",
                ]
            )

        roadmap = item.roadmap

        total = roadmap.items.count()

        completed = (
            roadmap.items
            .filter(status="completed")
            .count()
        )

        if (
            total
            and completed == total
            and roadmap.status != "completed"
        ):

            roadmap.status = "completed"

            roadmap.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )