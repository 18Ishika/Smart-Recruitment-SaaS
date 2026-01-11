from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()

    location = models.CharField(max_length=255, blank=True)
    experience_required = models.IntegerField(null=True, blank=True)

    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('FT', 'Full-time'),
            ('PT', 'Part-time'),
            ('IN', 'Internship'),
            ('CT', 'Contract')
        ],
        default='FT'
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
