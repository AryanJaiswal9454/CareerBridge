from pathlib import Path

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .resume_generator import build_resume_docx, resume_to_text

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from docx import Document
from PyPDF2 import PdfReader

from .models import Resume
from .serializers import ResumeUploadSerializer
from careerbridge.ai import analyze_resume, generate_ats_report


def extract_text_from_file(file):
    """
    Extract text from PDF, DOCX or TXT resume files.
    """

    extension = Path(file.name).suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(file)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text).strip()

    elif extension == ".docx":
        document = Document(file)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs).strip()

    elif extension == ".txt":
        return file.read().decode("utf-8", errors="ignore").strip()

    raise ValueError(
        "Unsupported file type. Only PDF, DOCX and TXT are supported."
    )


class ResumeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    queryset = Resume.objects.all()
    serializer_class = ResumeUploadSerializer

    def get(self, request):
        resumes = Resume.objects.filter(
            user=request.user
        ).order_by("-created_at")

        data = []

        for resume in resumes:
            data.append({
                "id": resume.id,
                "title": resume.title,
                "file": resume.file.url if resume.file else None,
                "created_at": resume.created_at,
                "updated_at": resume.updated_at,
                "has_extracted_text": bool(resume.extracted_text),
                "has_ai_analysis": bool(resume.ai_analysis),
                "ai_analysis": resume.ai_analysis,
                "has_ats_report": bool(resume.ats_report),
            })

        return Response(data)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        resume = serializer.save(
            user=request.user
        )

        try:
            extracted_text = extract_text_from_file(
                resume.file
            )

            resume.extracted_text = extracted_text

            if not resume.title:
                resume.title = Path(
                    resume.file.name
                ).stem

            resume.save()

        except Exception as error:
            resume.delete()

            return Response(
                {
                    "error": "Unable to extract text from the uploaded resume.",
                    "details": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Resume uploaded successfully.",
                "resume": {
                    "id": resume.id,
                    "title": resume.title,
                    "file": resume.file.url,
                    "created_at": resume.created_at,
                    "has_extracted_text": bool(
                        resume.extracted_text
                    ),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ResumeAnalyzeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Resume.objects.all()

    def post(self, request, pk):
        resume = get_object_or_404(
            Resume,
            id=pk,
            user=request.user
        )

        if not resume.extracted_text:
            return Response(
                {
                    "error": "Resume text is not available.",
                    "message": "Upload the resume again or check file extraction.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            analysis = analyze_resume(
                resume.extracted_text
            )

            resume.ai_analysis = analysis
            resume.save(
                update_fields=[
                    "ai_analysis",
                    "updated_at",
                ]
            )

            return Response(
                {
                    "message": "Resume analyzed successfully.",
                    "resume_id": resume.id,
                    "analysis": analysis,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            return Response(
                {
                    "error": "Resume analysis failed.",
                    "details": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ResumeATSScoreView(GenericAPIView):
    """Generic, job-independent ATS friendliness check: is this resume
    structured in a way an ATS parser can actually read? Distinct from
    ResumeOptimizationView (matching app), which compares a resume to a
    specific job description instead.
    """

    permission_classes = [IsAuthenticated]

    queryset = Resume.objects.all()

    def get(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        if not resume.ats_report:
            return Response(
                {"error": "No ATS report yet — run the check first (POST)."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({"resume_id": resume.id, "report": resume.ats_report})

    def post(self, request, pk):
        resume = get_object_or_404(
            Resume,
            id=pk,
            user=request.user
        )

        if not resume.extracted_text:
            return Response(
                {"error": "Resume text is not available. Upload the resume again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            report = generate_ats_report(resume.extracted_text)

            resume.ats_report = report
            resume.save(update_fields=["ats_report", "updated_at"])

            return Response({
                "message": "ATS check completed.",
                "resume_id": resume.id,
                "report": report,
            })

        except Exception as error:
            return Response(
                {"error": "ATS check failed.", "details": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class ResumeGenerateView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        full_name = str(data.get("full_name") or "").strip()
        email = str(data.get("email") or "").strip()
        phone = str(data.get("phone") or "").strip()
        template = str(data.get("template") or "aryan_ats").strip()

        if not full_name:
            return Response(
                {"error": "Full name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email and not phone:
            return Response(
                {"error": "Add at least an email address or phone number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        skills = data.get("key_skills") or []
        education = data.get("education") or []

        if not isinstance(skills, list) or not skills:
            return Response(
                {"error": "Add at least one technical skill."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(education, list) or not education:
            return Response(
                {"error": "Add at least one education entry."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        allowed_templates = {
            "aryan_ats",
            "classic_ats",
            "modern_professional",
            "compact_ats",
        }

        if template not in allowed_templates:
            template = "aryan_ats"

        payload = {
            "full_name": full_name,
            "headline": str(data.get("headline") or "").strip(),
            "location": str(data.get("location") or "").strip(),
            "phone": phone,
            "email": email,
            "linkedin": str(data.get("linkedin") or "").strip(),
            "github": str(data.get("github") or "").strip(),
            "portfolio": str(data.get("portfolio") or "").strip(),
            "professional_summary": str(
                data.get("professional_summary") or ""
            ).strip(),
            "key_skills": [str(x).strip() for x in skills if str(x).strip()],
            "work_experience": data.get("work_experience") or [],
            "projects": data.get("projects") or [],
            "education": education,
            "certifications": data.get("certifications") or [],
        }

        try:
            document_bytes = build_resume_docx(
                payload,
                template_key=template,
            )

            extracted_text = resume_to_text(payload)

            title_base = payload["headline"] or "Resume"
            title = f"{full_name} — {title_base}"

            resume = Resume(
                user=request.user,
                title=title[:200],
                extracted_text=extracted_text,
            )

            filename = (
                f"{slugify(full_name) or 'resume'}"
                f"_{slugify(template) or 'aryan_ats'}.docx"
            )

            resume.file.save(
                filename,
                ContentFile(document_bytes),
                save=False,
            )

            resume.save()

            return Response(
                {
                    "message": "New resume generated successfully.",
                    "resume_id": resume.id,
                    "title": resume.title,
                    "template": template,
                    "file": resume.file.url if resume.file else None,
                    "has_extracted_text": bool(resume.extracted_text),
                    "has_ai_analysis": False,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as error:
            return Response(
                {
                    "error": "Unable to generate the resume.",
                    "details": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

