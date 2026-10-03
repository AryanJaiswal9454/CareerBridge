
from decimal import Decimal, InvalidOperation

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import StudentProfile, Skill


def profile_payload(profile, user):
    return {
        "id": profile.id,
        "username": user.username,
        "email": user.email,
        "full_name": profile.full_name,
        "phone": profile.phone,
        "date_of_birth": profile.date_of_birth,
        "college": profile.college,
        "degree": profile.degree,
        "graduation_year": profile.graduation_year,
        "career_goal": profile.career_goal,
        "bio": profile.bio,
    }


def skill_payload(skill):
    return {
        "id": skill.id,
        "name": skill.name,
        "proficiency": skill.proficiency,
        "years_of_experience": float(
            skill.years_of_experience
        ),
    }


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": (
                    request.user.get_full_name()
                    or request.user.username
                )
            },
        )

        return Response(
            profile_payload(
                profile,
                request.user
            )
        )

    def put(self, request):
        profile, _ = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": (
                    request.user.get_full_name()
                    or request.user.username
                )
            },
        )

        fields = [
            "full_name",
            "phone",
            "date_of_birth",
            "college",
            "degree",
            "graduation_year",
            "career_goal",
            "bio",
        ]

        for field in fields:
            if field not in request.data:
                continue

            value = request.data.get(field)

            if field == "full_name":
                setattr(
                    profile,
                    field,
                    value or ""
                )
            else:
                setattr(
                    profile,
                    field,
                    value or None
                )

        profile.save()

        return Response(
            {
                "message":
                    "Profile updated successfully.",
                "profile":
                    profile_payload(
                        profile,
                        request.user
                    ),
            }
        )


class SkillsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile(self, request):
        profile, _ = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": (
                    request.user.get_full_name()
                    or request.user.username
                )
            },
        )

        return profile

    def get(self, request):
        profile = self.get_profile(
            request
        )

        skills = (
            profile.skills
            .all()
            .order_by("name")
        )

        return Response(
            [
                skill_payload(skill)
                for skill in skills
            ]
        )

    def post(self, request):
        profile = self.get_profile(
            request
        )

        name = str(
            request.data.get(
                "name",
                ""
            )
        ).strip()

        proficiency = request.data.get(
            "proficiency",
            "beginner"
        )

        years = request.data.get(
            "years_of_experience",
            0
        )

        if not name:
            return Response(
                {
                    "error":
                        "Skill name is required."
                },
                status=400,
            )

        if proficiency not in {
            "beginner",
            "intermediate",
            "advanced",
        }:
            return Response(
                {
                    "error":
                        "Invalid proficiency."
                },
                status=400,
            )

        try:
            years_decimal = Decimal(
                str(years)
            )
        except (
            InvalidOperation,
            ValueError,
            TypeError,
        ):
            return Response(
                {
                    "error":
                        "Experience must be a valid number."
                },
                status=400,
            )

        if years_decimal < 0:
            return Response(
                {
                    "error":
                        "Experience cannot be negative."
                },
                status=400,
            )

        if years_decimal > 99:
            return Response(
                {
                    "error":
                        "Experience cannot exceed 99 years."
                },
                status=400,
            )

        try:
            skill, _ = (
                Skill.objects.update_or_create(
                    profile=profile,
                    name=name,
                    defaults={
                        "proficiency":
                            proficiency,
                        "years_of_experience":
                            years_decimal,
                    },
                )
            )
        except Exception as exc:
            return Response(
                {
                    "error":
                        str(exc)
                },
                status=400,
            )

        return Response(
            skill_payload(skill),
            status=201
        )


class SkillDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, skill_id):
        try:
            skill = Skill.objects.get(
                id=skill_id,
                profile__user=request.user,
            )
        except Skill.DoesNotExist:
            return Response(
                {
                    "error":
                        "Skill not found."
                },
                status=404,
            )

        skill_name = skill.name

        skill.delete()

        return Response(
            {
                "message":
                    f"{skill_name} removed successfully."
            }
        )

