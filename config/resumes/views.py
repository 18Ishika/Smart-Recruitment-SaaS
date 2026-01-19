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
            return Response({"error": "No resume files provided."}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for file in files:
            # 1. Save to DB
            serializer = ResumeSerializer(data={'job': job.id, 'resume_file': file})
            serializer.is_valid(raise_exception=True)
            resume = serializer.save()

            # 2. Process only this specific instance
            result = process_and_score_resume(resume, job.description)
            results.append(result)

        # 3. Sort the local list (no folder scanning)
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:5]
        return Response({
            "job_id": job.id,
            "uploaded_now": len(results),
            "rankings": top_results
        }, status=status.HTTP_201_CREATED)