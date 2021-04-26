from rest_framework import serializers
from ...hr.models import Resume, Vacancies
from ..actions import TgManager


class ResumeSerializer(serializers.Serializer):
    resume = serializers.IntegerField(required=True, )

    def validate(self, attrs):
        resume_id = attrs.get('resume', 0)
        try:
            resume_model = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            raise serializers.ValidationError({'resume': ['resume not found']})
        return attrs

    def save(self):
        resume = self.validated_data.get('resume', 0)
        manager = TgManager()
        manager.sendResume(resume)
        return 1

class VacancySerializer(serializers.Serializer):
    vacancy = serializers.IntegerField(required=True, )

    def validate(self, attrs):
        vacancy_id = attrs.get('vacancy', 0)
        try:
            resume_model = Vacancies.objects.get(id=vacancy_id)
        except Vacancies.DoesNotExist:
            raise serializers.ValidationError({'vacancy': ['vacancy not found']})
        return attrs

    def save(self):
        vacancy = self.validated_data.get('vacancy', 0)
        manager = TgManager()
        manager.sendVacancy(vacancy)
        return 1