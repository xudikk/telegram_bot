from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound


from . import services, vacancy
from .serializers import CompanySerializer

class CompanyView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer

    def get_editserializer_class(self,  *args, **kwargs):
        return CompanySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, company=None)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        result = services.get_one_company(request, company.id)

        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            serializer = self.get_serializer(data=request.data, company=kwargs['id'])
            serializer.is_valid(raise_exception=True)
            company = serializer.save()
            result = services.get_one_company(request, company.id)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')

    def get(self, request, *args, **kwargs):
        if 'id'in kwargs and kwargs['id']:
            result = services.get_one_company(request, kwargs['id'])
        else:
            result = services.get_list_company(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class StatusView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        result = services.get_list_status(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')
