from rest_framework import serializers
from .models import Resume
from jobs.models import Job

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['id', 'parsed_text', 'score', 'uploaded_at']
    def validate_job(self, job):
        if not Job.objects.filter(id=job.id).exists():
            raise serializers.ValidationError("Invalid job id.")
        return job
        
    def validate_resume_file(self, resume_file):
        if not resume_file.name.lower().endswith(('.pdf', '.doc', '.docx')):
            raise serializers.ValidationError("Unsupported file type. Please upload a PDF or Word document.")
        return resume_file