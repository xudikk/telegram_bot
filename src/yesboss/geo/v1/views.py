from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from .services import get_region_list, get_district_list

class RegionListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        '''API for getting regions list'''
        result = get_region_list(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')


class DistrictListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        '''API for getting district list'''
        if kwargs['id']:
            try:
                result = get_district_list(request, kwargs['id'])
                return Response(result, status=status.HTTP_200_OK, content_type='application/json')
            except Exception as e:
                raise NotFound('invalid argument1')
