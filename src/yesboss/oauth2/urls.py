from django.urls import path
from .v1.views import SignInView

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='auth-login-v1'),
]