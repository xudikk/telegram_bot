from django.urls import path
from .v1.views import UserAllListView

urlpatterns = [
    path('', UserAllListView.as_view(), name='users-list-v1'),
    path('<int:id>/', UserAllListView.as_view(), name='users-list-v1'),
]