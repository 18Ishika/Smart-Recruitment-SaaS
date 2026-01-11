# Create your models here.
from django.db import models
from jobs.models import Job

class Resume(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='resumes')

    candidate_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    resume_file = models.FileField(upload_to='resumes/')
    parsed_text = models.TextField(blank=True)

    score = models.FloatField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} - {self.job.title}"
