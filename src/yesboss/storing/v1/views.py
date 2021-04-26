from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import NotFound
from django.conf import settings
from .serializers import FileSerializer
from ..models import Files

BASE_LINK = settings.BASE_LINK
class FileView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self, *args, **kwargs):
        try:
            files = Files.objects.get(id=kwargs['pk'])
        except Exception as e:
            print('Error : ', str(e))
            raise NotFound('not found file')
        return files

    def post(self, request, *args, **kwargs):
        '''API for creating product photo'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data = {
            'id': data.id,
            'file': BASE_LINK+data.file_path.url,
            'file_type': data.file_type,
        }
        return Response(data, status=status.HTTP_200_OK)

