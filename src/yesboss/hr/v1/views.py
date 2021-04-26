from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound


from . import (services, vacancy, resume, dashboard)
from .serializers import (CategorySerializer, PositionSerializer, ScheduleSerializer, VacancySerializer, ResumeSerializer)

class CategoryView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_editserializer_class(self,  *args, **kwargs):
        return CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, category=None)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        result = services.get_one_category(request, category.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            serializer = self.get_serializer(data=request.data, category=kwargs['id'])
            serializer.is_valid(raise_exception=True)
            category = serializer.save()
            result = services.get_one_category(request, category.id)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')

    def get(self, request, *args, **kwargs):
        if 'id'in kwargs and kwargs['id']:
            result = services.get_one_category(request, kwargs['id'])
        else:
            result = services.get_list_category(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class PositionView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = PositionSerializer

    def get_editserializer_class(self,  *args, **kwargs):
        return PositionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, position=None)
        serializer.is_valid(raise_exception=True)
        position = serializer.save()
        result = services.get_one_position(request, position.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            serializer = self.get_serializer(data=request.data, position=kwargs['id'])
            serializer.is_valid(raise_exception=True)
            position = serializer.save()
            result = services.get_one_position(request, position.id)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')



    def get(self, request, *args, **kwargs):
        if 'id'in kwargs and kwargs['id']:
            result = services.get_one_position(request, kwargs['id'])
        else:
            result = services.get_list_positions(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')


class ScheduleView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ScheduleSerializer

    def get_editserializer_class(self, *args, **kwargs):
        return ScheduleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, schedule=None)
        serializer.is_valid(raise_exception=True)
        position = serializer.save()
        result = services.get_one_schedule(request, position.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            serializer = self.get_serializer(data=request.data, schedule=kwargs['id'])
            serializer.is_valid(raise_exception=True)
            position = serializer.save()
            result = services.get_one_schedule(request, position.id)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            result = services.get_one_schedule(request, kwargs['id'])
        else:
            result = services.get_list_schedule(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')


class ExperienceView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            result = services.get_one_experiences(request, kwargs['id'])
        else:
            result = services.get_list_experiences(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class StatusView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        result = services.get_list_status(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class LanguagesView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        result = services.get_list_languages(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class VacancyView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VacancySerializer

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            result = vacancy.get_one_vacancy(request, kwargs['id'])
        else:
            result = vacancy.get_list_vacancies(request)

        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, vacancy=None)
        serializer.is_valid(raise_exception=True)
        vacancy_model = serializer.save()
        result = vacancy.get_one_vacancy(request, vacancy_model.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            serializer = self.get_serializer(data=request.data, vacancy=kwargs['id'])
            serializer.is_valid(raise_exception=True)
            vacancy_model = serializer.save()
            result = vacancy.get_one_vacancy(request, vacancy_model.id)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')

class ResumeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResumeSerializer

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            result = resume.get_one_resume(request, kwargs['id'])
        else:
            result = resume.get_list_resumes(request)

        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, resume=None)
        serializer.is_valid(raise_exception=True)
        resume_model = serializer.save()
        result = resume.get_one_resume(request, resume_model.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            serializer = self.get_serializer(data=request.data, resume=kwargs['id'])
            serializer.is_valid(raise_exception=True)
            resume_model = serializer.save()
            result = resume.get_one_resume(request, resume_model.id)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')

class CounterView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        result = dashboard.get_counters()
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class TopCategoryView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        result = dashboard.get_top_category(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')