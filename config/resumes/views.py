from resumes.parsers import get_resume_path, rank_resumes , process_and_score_resume
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Resume
from .serializers import ResumeSerializer
from jobs.models import Job


class ResumeUploadView(APIView):
    def post(self, request):
        job_id = request.data.get('job')
        job = get_object_or_404(Job, id=job_id)

        files = request.FILES.getlist('resume_file')

        if not files:
            return Response(
                {"error": "No resume files provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_resumes = []

        # 1️⃣ Save only new resumes
        for file in files:
            serializer = ResumeSerializer(
                data={
                    'job': job.id,
                    'resume_file': file
                }
            )
            serializer.is_valid(raise_exception=True)
            resume = serializer.save()
            created_resumes.append(resume)

        # 2️⃣ Process ONLY new ones
        results = []
        for resume in created_resumes:
            result = process_and_score_resume(resume, job.description)
            results.append(result)

        # 3️⃣ Rank
        results.sort(key=lambda x: x['score'], reverse=True)

        return Response({
            "job_id": job.id,
            "uploaded_now": len(created_resumes),
            "rankings": results
        }, status=status.HTTP_201_CREATED)
