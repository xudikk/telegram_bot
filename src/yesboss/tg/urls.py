from django.urls import path
from .v1.views import ResumeView, VacancyView

urlpatterns = [
    path('resume-send/', ResumeView.as_view(), name='tg-resume-send'),
    path('vacancy-send/', VacancyView.as_view(), name='tg-vacancy-send'),
]
