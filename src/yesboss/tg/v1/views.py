from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from .serializers import (ResumeSerializer, VacancySerializer)

class ResumeView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ResumeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save()
        return Response({'ok': True}, status=status.HTTP_200_OK)



class VacancyView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = VacancySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save()
        return Response({'ok': True}, status=status.HTTP_200_OK)