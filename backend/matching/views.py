

from django.http import HttpResponse
from django.utils.timezone import now

from .ats import calculate_ats_score, compare_ats_scores
from .resume_templates import get_templates, build_resume_docx

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from resumes.models import Resume
from careers.models import JobDescription
from .models import MatchResult
from .engine import calculate_match_score
from careerbridge.ai import generate_resume_optimization, generate_tailored_resume


def _match_payload(match, result=None, existing=False):
    payload = {
        "match_id": match.id,
        "id": match.id,
        "resume_id": match.resume_id,
        "job_id": match.job_description_id,
        "resume_title": match.resume.title,
        "company_name": match.job_description.company_name,
        "job_title": match.job_description.job_title,
        "match_score": float(match.match_score),
        "matched_skills": match.matched_skills,
        "skills_to_improve": match.skills_to_improve,
        "missing_skills": match.missing_skills,
        "preferred_skills_missing": match.preferred_skills_missing,
        "experience_match": match.experience_match,
        "education_match": match.education_match,
        "has_optimization": bool(match.optimization),
        "has_tailored_resume": bool(match.tailored_resume),
        "created_at": match.created_at,
        "updated_at": match.updated_at,
        "existing": existing,
    }
    if result:
        payload.update(result)
    return payload

class ResumeTemplatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_templates())


class MatchResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = (
            MatchResult.objects
            .filter(user=request.user)
            .select_related("resume", "job_description")
            .order_by("-created_at")
        )
        return Response([_match_payload(r) for r in results])


class MatchResumeToJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")

        if not resume_id or not job_id:
            return Response({"error": "resume_id and job_id are required."}, status=400)

        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found."}, status=404)

        try:
            job = JobDescription.objects.get(id=job_id, user=request.user)
        except JobDescription.DoesNotExist:
            return Response({"error": "Job description not found."}, status=404)

        if not resume.ai_analysis:
            return Response({"error": "Resume has not been analyzed yet."}, status=400)
        if not job.ai_analysis:
            return Response({"error": "Job description has not been analyzed yet."}, status=400)

        existing = (
            MatchResult.objects
            .select_related("resume", "job_description")
            .filter(
                user=request.user,
                resume=resume,
                job_description=job,
            )
            .first()
        )

        # Matching is deterministic and the result is a stored career artifact.
        # Reuse it instead of creating duplicate records every time the page opens.
        if existing:
            return Response(_match_payload(existing, existing=True))

        result = calculate_match_score(resume.ai_analysis, job.ai_analysis)
        match_result = MatchResult.objects.create(
            user=request.user,
            resume=resume,
            job_description=job,
            match_score=result["match_score"],
            matched_skills=result["matched_skills"],
            skills_to_improve=result["skills_to_improve"],
            missing_skills=result["missing_skills"],
            preferred_skills_missing=result["preferred_skills_missing"],
            experience_match=result["experience_match"],
            education_match=result["education_match"],
        )
        return Response(_match_payload(match_result, result=result), status=status.HTTP_201_CREATED)


class ResumeOptimizationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        return self._respond(request, match_id, force_refresh=False)

    def post(self, request, match_id):
        return self._respond(request, match_id, force_refresh=True)

    def _respond(self, request, match_id, force_refresh):
        try:
            match = (
                MatchResult.objects
                .select_related("resume", "job_description")
                .get(id=match_id, user=request.user)
            )
        except MatchResult.DoesNotExist:
            return Response({"error": "Match result not found."}, status=404)

        if match.optimization and not force_refresh:
            return Response(match.optimization)

        try:
            optimization = generate_resume_optimization(
                match.resume.extracted_text,
                match.job_description.description,
                match.missing_skills + match.preferred_skills_missing,
                match.matched_skills,
            )
        except Exception as exc:
            return Response(
                {"error": "Unable to generate resume optimization suggestions right now.", "details": str(exc)},
                status=500,
            )

        match.optimization = optimization
        match.save(update_fields=["optimization", "updated_at"])
        return Response(optimization)



class TailoredResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        return self._respond(request, match_id, force_refresh=False)

    def post(self, request, match_id):
        return self._respond(request, match_id, force_refresh=True)

    def _respond(self, request, match_id, force_refresh):
        try:
            match = (
                MatchResult.objects
                .select_related("resume", "job_description")
                .get(id=match_id, user=request.user)
            )
        except MatchResult.DoesNotExist:
            return Response({"error": "Match result not found."}, status=404)

        history = list(match.tailored_resume_history or [])

        if match.tailored_resume and not history:
            history = [{
                "version": 1,
                "generated_at": match.updated_at.isoformat(),
                "job_title": match.job_description.job_title,
                "company_name": match.job_description.company_name,
                "resume_title": match.resume.title,
                "template": "aryan_ats",
                "data": match.tailored_resume,
            }]

            match.tailored_resume_history = history
            match.save(
                update_fields=[
                    "tailored_resume_history",
                    "updated_at",
                ]
            )

        if match.tailored_resume and not force_refresh:
            payload = dict(match.tailored_resume)
            payload["history"] = history
            payload["current_version"] = (
                history[-1].get("version", 1)
                if history
                else 1
            )

            return Response(payload)

        try:
            tailored = generate_tailored_resume(
                match.resume.extracted_text,
                match.job_description.description,
                match.job_description.job_title,
                match.job_description.company_name,
                match.missing_skills + match.preferred_skills_missing,
                match.matched_skills,
            )

            # --------------------------------------------------
            # ATS score BEFORE tailoring
            # --------------------------------------------------

            before_ats = calculate_ats_score(
                match.resume.extracted_text,
                match.job_description.ai_analysis or {},
            )

            # --------------------------------------------------
            # ATS score AFTER tailoring
            # --------------------------------------------------

            tailored_text = self._tailored_to_text(tailored)

            after_ats = calculate_ats_score(
                tailored_text,
                match.job_description.ai_analysis or {},
            )

            comparison = compare_ats_scores(
                before_ats,
                after_ats,
            )

            tailored["ats_report"] = {
                "before": before_ats,
                "after": after_ats,
                "comparison": comparison,
            }

            tailored["selected_template"] = "aryan_ats"

        except Exception as exc:
            return Response(
                {
                    "error": "Unable to generate a tailored resume right now.",
                    "details": str(exc),
                },
                status=500,
            )

        existing_versions = [
            int(item.get("version", 0))
            for item in history
            if str(item.get("version", "")).isdigit()
        ]

        next_version = max(existing_versions, default=0) + 1

        history.append({
            "version": next_version,
            "generated_at": now().isoformat(),
            "job_title": match.job_description.job_title,
            "company_name": match.job_description.company_name,
            "resume_title": match.resume.title,
            "template": "aryan_ats",
            "data": tailored,
        })

        match.tailored_resume = tailored
        match.tailored_resume_history = history

        match.save(
            update_fields=[
                "tailored_resume",
                "tailored_resume_history",
                "updated_at",
            ]
        )

        payload = dict(tailored)
        payload["history"] = history
        payload["current_version"] = next_version

        return Response(payload)

    @staticmethod
    def _tailored_to_text(data):
        parts = []

        for key in (
            "full_name",
            "contact_line",
            "professional_summary",
        ):
            if data.get(key):
                parts.append(str(data[key]))

        for skill in data.get("key_skills") or []:
            parts.append(str(skill))

        for job in data.get("work_experience") or []:
            if not isinstance(job, dict):
                continue

            parts.extend([
                job.get("title", ""),
                job.get("organization", ""),
                job.get("duration", ""),
            ])

            parts.extend(job.get("bullets") or [])

        for project in data.get("projects") or []:
            if isinstance(project, dict):
                parts.extend([
                    project.get("name", ""),
                    project.get("title", ""),
                    project.get("description", ""),
                    project.get("tech_stack", ""),
                ])
                parts.extend(project.get("bullets") or [])
            else:
                parts.append(str(project))

        parts.extend(data.get("education") or [])
        parts.extend(data.get("certifications") or [])

        return "\n".join(
            str(value)
            for value in parts
            if value
        )




class TailoredResumeDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        try:
            match = (
                MatchResult.objects
                .select_related("job_description", "resume")
                .get(
                    id=match_id,
                    user=request.user,
                )
            )
        except MatchResult.DoesNotExist:
            return Response(
                {"error": "Match result not found."},
                status=404,
            )

        tailored = match.tailored_resume
        history = list(match.tailored_resume_history or [])

        version = request.query_params.get("version")

        if version:
            try:
                version_number = int(version)
            except (TypeError, ValueError):
                return Response(
                    {"error": "Invalid tailored resume version."},
                    status=400,
                )

            selected = next(
                (
                    item
                    for item in history
                    if int(item.get("version", 0)) == version_number
                ),
                None,
            )

            if not selected:
                return Response(
                    {"error": "Tailored resume version not found."},
                    status=404,
                )

            tailored = selected.get("data") or {}

        if not tailored:
            return Response(
                {
                    "error": (
                        "Generate the tailored resume first "
                        "before downloading it."
                    )
                },
                status=400,
            )

        template_key = (
            request.query_params.get("template")
            or tailored.get("selected_template")
            or "aryan_ats"
        )

        try:
            document_buffer = build_resume_docx(
                tailored,
                template_key,
            )
        except Exception as exc:
            return Response(
                {
                    "error": "Unable to build the selected resume template.",
                    "details": str(exc),
                },
                status=500,
            )

        company = "_".join(
            (match.job_description.company_name or "target").split()
        )

        role = "_".join(
            (match.job_description.job_title or "role").split()
        )

        version_suffix = (
            f"_v{version}"
            if version
            else ""
        )

        filename = (
            f"Tailored_Resume_{company}_{role}"
            f"{version_suffix}.docx"
        )

        response = HttpResponse(
            document_buffer.read(),
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{filename}"'
        )

        return response

