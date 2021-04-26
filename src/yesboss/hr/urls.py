from django.urls import path
from .v1.views import (CategoryView, PositionView, ScheduleView,
                       VacancyView, ExperienceView, StatusView, LanguagesView, ResumeView, CounterView, TopCategoryView)

urlpatterns = [
    path('counters/', CounterView.as_view(), name='dashboard-counters-v1'),
    path('top-categories/', TopCategoryView.as_view(), name='dashboard-categories-v1'),

    path('categories/', CategoryView.as_view(), name='category-list-v1'),
    path('categories/<int:id>/', CategoryView.as_view(), name='category-detail-v1'),

    path('positions/', PositionView.as_view(), name='positions-list-v1'),
    path('positions/<int:id>/', PositionView.as_view(), name='positions-detail-v1'),

    path('schedules/', ScheduleView.as_view(), name='schedules-list-v1'),
    path('schedules/<int:id>/', ScheduleView.as_view(), name='schedules-detail-v1'),

    path('vacancies/', VacancyView.as_view(), name='vacancies-list-v1'),
    path('vacancies/<int:id>/', VacancyView.as_view(), name='vacancies-detail-v1'),

    path('vacancies/', VacancyView.as_view(), name='vacancies-list-v1'),
    path('vacancies/<int:id>/', VacancyView.as_view(), name='vacancies-detail-v1'),

    path('resumes/', ResumeView.as_view(), name='resumes-list-v1'),
    path('resumes/<int:id>/', ResumeView.as_view(), name='resumes-detail-v1'),

    path('experiences/', ExperienceView.as_view(), name='experiences-list-v1'),
    path('experiences/<int:id>/', ExperienceView.as_view(), name='experiences-detail-v1'),

    path('statuses/', StatusView.as_view(), name='statuses-list-v1'),
    path('languages/', LanguagesView.as_view(), name='languages-list-v1'),

]
