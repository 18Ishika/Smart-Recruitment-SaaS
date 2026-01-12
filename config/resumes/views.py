from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Resume
from .serializers import ResumeSerializer

class ResumeUploadView(APIView):

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            resume = serializer.save()

            # 🚀 Celery task will be triggered here later
            # process_resume.delay(resume.id)

            return Response(
                ResumeSerializer(resume).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
