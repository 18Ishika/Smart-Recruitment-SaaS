from django.db import models
from jobs.models import Job
import uuid, os

def resume_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return f"resumes/job_{instance.job.id}/{unique_name}"

class Resume(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='resumes'
    )

    resume_file = models.FileField(upload_to=resume_upload_path)
    actual_resume_file_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(
    max_length=20,
    default="PENDING"
)


    parsed_text = models.TextField(blank=True)
    score = models.FloatField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - Job {self.job.title}"