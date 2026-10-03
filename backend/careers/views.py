from pathlib import Path
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader
from docx import Document
from .models import JobDescription
from careerbridge.ai import analyze_job_description


def extract_text_from_file(file):
    extension = Path(file.name).suffix.lower()
    try:
        if extension == ".pdf":
            reader = PdfReader(file)
            return "\n".join((page.extract_text() or "") for page in reader.pages).strip()
        if extension == ".docx":
            document = Document(file)
            return "\n".join(p.text for p in document.paragraphs if p.text.strip()).strip()
        if extension == ".txt":
            return file.read().decode("utf-8", errors="ignore").strip()
    except Exception as exc:
        print("JD FILE EXTRACTION ERROR:", exc)
    return ""


class JobDescriptionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        jobs = JobDescription.objects.filter(user=request.user).order_by("-created_at")
        return Response([
            {
                "id": job.id,
                "company_name": job.company_name,
                "job_title": job.job_title,
                "source_type": job.source_type,
                "file": job.file.url if job.file else None,
                "description": job.description,
                "extracted_text": job.extracted_text,
                "ai_analysis": job.ai_analysis,
                "created_at": job.created_at,
            } for job in jobs
        ])

    def post(self, request):
        company_name = str(request.data.get("company_name", "")).strip()
        job_title = str(request.data.get("job_title", "")).strip()
        description = str(request.data.get("description", "")).strip()
        uploaded_file = request.FILES.get("file")

        if not company_name:
            return Response({"error": "Company name is required."}, status=400)
        if not job_title:
            return Response({"error": "Job title is required."}, status=400)
        if not description and not uploaded_file:
            return Response({"error": "Paste the exact JD or upload a JD file."}, status=400)

        if uploaded_file:
            extension = Path(uploaded_file.name).suffix.lower()
            if extension not in {".pdf", ".docx", ".txt"}:
                return Response({"error": "Only PDF, DOCX and TXT files are supported."}, status=400)
            extracted = extract_text_from_file(uploaded_file)
            if not extracted:
                return Response({"error": "The file was received but no readable text could be extracted."}, status=400)
            job = JobDescription.objects.create(
                user=request.user, company_name=company_name, job_title=job_title,
                source_type="file", file=uploaded_file, description=extracted, extracted_text=extracted,
            )
        else:
            job = JobDescription.objects.create(
                user=request.user, company_name=company_name, job_title=job_title,
                source_type="text", description=description, extracted_text=description,
            )

        return Response({
            "message": "Job description saved successfully.", "id": job.id,
            "company_name": job.company_name, "job_title": job.job_title,
            "source_type": job.source_type, "text_length": len(job.extracted_text or ""),
        }, status=status.HTTP_201_CREATED)


class JobDescriptionAnalyzeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        try:
            job = JobDescription.objects.get(id=job_id, user=request.user)
        except JobDescription.DoesNotExist:
            return Response({"error": "Job description not found."}, status=404)
        if not job.extracted_text:
            return Response({"error": "No JD text available for analysis."}, status=400)
        try:
            analysis = analyze_job_description(job.extracted_text)
            job.ai_analysis = analysis
            job.save(update_fields=["ai_analysis"])
            return Response({"message": "Job description analyzed successfully.", "analysis": analysis})
        except Exception as exc:
            return Response({"error": "JD analysis failed.", "details": str(exc)}, status=500)
