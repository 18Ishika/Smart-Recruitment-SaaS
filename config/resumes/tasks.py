from celery import shared_task
from .models import Resume
from resumes.parsers import process_and_score_resume
from jobs.models import Job

from celery import shared_task
from .models import Resume
from resumes.parsers import process_and_score_resume
from jobs.models import Job

@shared_task(bind=True)
def process_resume_task(self, resume_id):
    resume = Resume.objects.get(id=resume_id)
    resume.status = "Processing"
    resume.save()

    try:
        result = process_and_score_resume(resume, resume.job.description)
        resume.status = "Processed"
        resume.save()
    except Exception:
        resume.status = "Failed"
        resume.save()
        raise
    return resume.id