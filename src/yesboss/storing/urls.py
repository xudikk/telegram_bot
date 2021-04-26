from django.urls import path
from .v1.views import FileView

urlpatterns = [
    path('files/', FileView.as_view(), name='files-v1'),
]
