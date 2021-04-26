from django.urls import path
from .v1.views import CompanyView, StatusView

urlpatterns = [
    path('company/', CompanyView.as_view(), name='company-list-v1'),
    path('company/<int:id>/', CompanyView.as_view(), name='company-detail-v1'),

    path('statuses/', StatusView.as_view(), name='statuses-list-v1'),

]