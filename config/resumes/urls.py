from django.urls import path
from .views import ResumeUploadView , JobRankingsView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('rankings/<int:job_id>/', JobRankingsView.as_view(), name='job-rankings'),
]
