from django.http import Http404
from django.utils import six
from rest_framework.views import set_rollback
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

def api_exception_handler(exc, context):
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        field_errors = {}

        if isinstance(exc.detail, (list, dict)):
            for i in exc.detail:
                try:
                    field_errors[i] = exc.detail[i][0]
                except Exception as e:
                    field_errors[i] = ''
            data = {'error_message': 'Bad request', 'errors': field_errors}
        else:
            data = {'error_message': exc.detail, 'errors': None}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = {'_error_message': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'_error_message': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    return None
