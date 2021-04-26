import json
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from oauthlib.oauth2 import Server
from .serializers import (SignInSerializer, RefreshTokenSerializer, LogoutSerializer)
from ..oauth2_validators import OAuth2V1Validator
from ..oauth2_backends import JSONOAuthLibCore


class SignInView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.request.data
        oauth2 = JSONOAuthLibCore(Server(OAuth2V1Validator()))
        uri, headers, body, status = oauth2.create_token_response(request)

        data = json.loads(body)
        if status != 200:
            raise ValidationError({'username': [data['error']]})

        return Response(data, status=status)

class RefreshTokenView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RefreshTokenSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        oauth2 = JSONOAuthLibCore(Server(OAuth2V1Validator()))
        uri, headers, body, status = oauth2.create_token_response(request)
        return Response(json.loads(body), status=status)


class LogoutView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_response(self):
        oauth2 = JSONOAuthLibCore(Server(OAuth2V1Validator()))
        url, headers, body, status = oauth2.create_revocation_response(self.request)
        if status != 200:
            result = json.loads(body)
        else:
            result = {"detail": _("success logout")}
        return Response(result, status=status)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.get_response()