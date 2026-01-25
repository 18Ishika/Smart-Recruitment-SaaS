from celery import shared_task
from .models import Resume
from resumes.parsers import process_and_score_resume
from jobs.models import Job

@shared_task(bind=True)
def process_resume_task(self, resume_id):
    resume = Resume.objects.get(id=resume_id)
    job = resume.job

    resume.status = "PROCESSING"
    resume.save()

    result = process_and_score_resume(resume, job.description)

    resume.score = result["score"]
    resume.parsed_text = result["text"]
    resume.status = "DONE"
    resume.save()

    return resume.id
