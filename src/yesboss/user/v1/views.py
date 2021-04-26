from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import services

class UserAllListView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if 'id'in kwargs and kwargs['id']:
            result = services.get_one_users(request, kwargs['id'])
        else:
            result = services.get_list_users(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

