from datetime import datetime
from django.utils.text import slugify
from text_unidecode import unidecode
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from ..actions import VacnacyManager, ResumeManager
from ..models import (Category, Positions, Schedules, Statuses, Experience, Languages, Vacancies, Resume)
from ...company.models import Companies
from ...geo.models import District, Region
from ...storing.models import Files
from ...user.models import Users

class langField(serializers.Serializer):
    uz = serializers.CharField(max_length=150, required=True)
    ru = serializers.CharField(max_length=150, required=True)

class salaryField(serializers.Serializer):
    from_price = serializers.IntegerField(min_value=1, required=False)
    to_price = serializers.IntegerField(min_value=1, required=False)
    text = serializers.CharField(max_length=150, required=True)

class ageField(serializers.Serializer):
    from_age = serializers.IntegerField(min_value=1, required=False)
    to_age = serializers.IntegerField(min_value=1, required=False)
    text = serializers.CharField(max_length=150, required=True)

class BusSerializer(serializers.Serializer):
    idn = serializers.IntegerField(read_only=True)
    stops_left = serializers.IntegerField(read_only=True)

class CategorySerializer(serializers.Serializer):
    parent_id = serializers.IntegerField(required=False, )
    name = langField()
    is_active = serializers.BooleanField(required=False, )
    is_main = serializers.BooleanField(required=False, )
    sort_order = serializers.IntegerField(required=False, )

    def __init__(self, *args, **kwargs):
        self.category_id = kwargs.pop('category')
        super(CategorySerializer, self).__init__(*args, **kwargs)

    def save(self):

        if self.category_id:
            try:
                category_model = Category.objects.get(id=self.category_id)
            except Category.DoesNotExist:
                raise serializers.ValidationError({'category': ['category found region']})
        else:
            category_model = Category()

        parent_id = self.validated_data.get('parent_id', category_model.parent_id)
        name = self.validated_data.get('name', category_model.name)
        is_active = self.validated_data.get('is_active', category_model.is_active)
        is_main = self.validated_data.get('is_main', category_model.is_main)
        sort_order = self.validated_data.get('sort_order', category_model.sort_order)
        slug = slugify(unidecode(name['ru']))
        if Category.objects.filter(slug__iexact=slug).exists():
            slug = f"{slug}-{datetime.now().timestamp()}"

        category_model.parent_id = parent_id
        category_model.name = name
        category_model.is_active = is_active
        category_model.is_main = is_main
        category_model.sort_order = sort_order
        category_model.slug = slug
        category_model.save()

        return category_model

class PositionSerializer(serializers.Serializer):
    category = serializers.IntegerField(required=True, )
    name = langField()
    slug = serializers.CharField(max_length=100, required=True)
    is_active = serializers.BooleanField(required=False, )

    def __init__(self, *args, **kwargs):
        self.position_id = kwargs.pop('position')
        super(PositionSerializer, self).__init__(*args, **kwargs)

    def save(self):

        if self.position_id:
            try:
                position_model = Positions.objects.get(id=self.position_id)
            except Positions.DoesNotExist:
                raise serializers.ValidationError({'category': ['position not found']})
        else:
            position_model = Positions()

        category_id = self.validated_data.get('category', position_model.category_id)
        name = self.validated_data.get('name', position_model.name)
        is_active = self.validated_data.get('is_active', position_model.is_active)
        slug = slugify(unidecode(name['ru']))
        if Positions.objects.filter(slug__iexact=slug).exists():
            slug = f"{slug}-{datetime.now().timestamp()}"

        position_model.category_id = category_id
        position_model.name = name
        position_model.is_active = is_active
        position_model.slug = slug
        position_model.save()
        try:
            position_model.clean()
        except Exception as e:
            print('error')
            print(str(e))
        return position_model

class ScheduleSerializer(serializers.Serializer):
    name = langField()
    alias = serializers.CharField(max_length=100, required=True)
    is_active = serializers.BooleanField(required=False, )

    def __init__(self, *args, **kwargs):
        self.schedule_id = kwargs.pop('schedule')
        super(ScheduleSerializer, self).__init__(*args, **kwargs)

    def save(self):

        if self.schedule_id:
            try:
                schedule_model = Schedules.objects.get(id=self.schedule_id)
            except Schedules.DoesNotExist:
                raise serializers.ValidationError({'schedule': ['schedule not found']})
        else:
            schedule_model = Schedules()

        name = self.validated_data.get('name', schedule_model.name)
        is_active = self.validated_data.get('is_active', schedule_model.is_active)
        slug = self.validated_data.get("alias", schedule_model.alias)
        slug = slugify(unidecode(slug))

        if not self.schedule_id:
            if Schedules.objects.filter(alias__iexact=slug).exists():
                slug = f"{slug}-{datetime.now().timestamp()}"

        schedule_model.name = name
        schedule_model.alias = slug
        schedule_model.is_active = is_active
        schedule_model.save()
        try:
            schedule_model.clean()
        except Exception as e:
            print('error')
            print(str(e))
        return schedule_model

class VacancySerializer(serializers.Serializer):
    company = serializers.IntegerField(required=True, )
    category = serializers.ListField(required=True, )
    position_name = serializers.CharField(max_length=200, required=True)
    schedule = serializers.IntegerField(required=True, )
    experience = serializers.IntegerField(required=True, )
    gender = serializers.ListField(required=True, )
    languages = serializers.ListField(required=True, )
    status = serializers.IntegerField(required=True, )
    region = serializers.IntegerField(required=True, )
    file = serializers.IntegerField(required=True, )
    district = serializers.IntegerField(required=True, )
    salary = salaryField()
    age = ageField()


    def __init__(self, *args, **kwargs):
        self.vacancy_id = kwargs.pop('vacancy')
        self.district_obj = None
        self.region_obj = None
        self.status_obj = None
        self.company_obj = None
        self.experience_obj = None
        self.schedule_obj = None
        self.file_obj = None
        self.categories = []
        self.languages_objs = []
        super(VacancySerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        if self.vacancy_id:
            try:
                vacancy_model = Vacancies.objects.get(id=self.vacancy_id)
            except Vacancies.DoesNotExist:
                raise serializers.ValidationError({'vacancy': ['vacancy not found']})
        else:
            vacancy_model = Vacancies()

        attrs['district'] = district = attrs.get('district', vacancy_model.district_id)
        attrs['region'] = region = attrs.get('region', vacancy_model.region_id)
        attrs['file'] = files = attrs.get('file', vacancy_model.files_id)
        attrs['status'] = status = attrs.get('status', vacancy_model.status_id)
        attrs['company'] = company = attrs.get('company', vacancy_model.company_id)
        attrs['experience'] = experience = attrs.get('experience', vacancy_model.experience_id)
        attrs['schedule'] = schedule = attrs.get('schedule', vacancy_model.schedule_id)
        categories = attrs.get('category', [])
        languages_objs = attrs.get('languages', [])
        if district:
            try:
                self.district_obj = District.objects.get(id=district)
            except District.DoesNotExist:
                raise serializers.ValidationError({'district': ['district not found']})
        if region:
            try:
                self.region_obj = Region.objects.get(id=region)
            except Region.DoesNotExist:
                raise serializers.ValidationError({'region': ['district not found']})
        if status:
            try:
                self.status_obj = Statuses.objects.get(id=status)
            except Statuses.DoesNotExist:
                raise serializers.ValidationError({'status': ['status not found']})

        if files:
            try:
                self.file_obj = Files.objects.get(id=files)
            except Files.DoesNotExist:
                raise serializers.ValidationError({'file': ['file not found']})

        if company:
            try:
                self.company_obj = Companies.objects.get(id=company)
            except Companies.DoesNotExist:
                raise serializers.ValidationError({'company': ['Company22 not found']})
        if experience:
            try:
                self.experience_obj = Experience.objects.get(id=experience)
            except Experience.DoesNotExist:
                raise serializers.ValidationError({'experience': ['Experience not found']})

        if schedule:
            try:
                self.schedule_obj = Schedules.objects.get(id=schedule)
            except Schedules.DoesNotExist:
                raise serializers.ValidationError({'schedule': ['Schedules not found']})

        try:
            for data in categories:
                self.categories.append(Category.objects.get(pk=data))
        except Category.DoesNotExist:
            raise serializers.ValidationError({'categories': ['invalid categories']})

        try:
            for data in languages_objs:
                self.languages_objs.append(Languages.objects.get(pk=data))
        except Languages.DoesNotExist:
            raise serializers.ValidationError({'languages': ['invalid languages']})
        return attrs

    def save(self):
        if self.vacancy_id:
            try:
                vacancy_model = Vacancies.objects.get(id=self.vacancy_id)
            except Vacancies.DoesNotExist:
                raise serializers.ValidationError({'vacancy': ['vacancy not found']})
        else:
            vacancy_model = Vacancies()
        position_name = self.validated_data.get('position_name', vacancy_model.position_name)
        salary = self.validated_data.get('salary', vacancy_model.salary)
        age = self.validated_data.get('age', vacancy_model.age)
        genders = self.validated_data.get('gender', None)
        manager = VacnacyManager()
        if self.vacancy_id:
            vacancy = manager.updateVacanvy(vacancy_model, self.company_obj, position_name, self.categories, self.schedule_obj,
                                            self.experience_obj, self.region_obj, self.district_obj, salary, age, genders,
                                            self.languages_objs, self.status_obj, self.file_obj)
        else:
            vacancy = manager.createVacanvy(self.company_obj, position_name, self.categories, self.schedule_obj,
                                            self.experience_obj, self.region_obj, self.district_obj, salary, age, genders,
                                            self.languages_objs, self.status_obj, self.file_obj)
        return vacancy


class ResumeSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True, )
    firstname = serializers.CharField(max_length=20, required=True)
    lastname = serializers.CharField(max_length=20, required=True)
    middlename = serializers.CharField(max_length=20, required=False)
    birthday = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    category = serializers.ListField(required=True, )
    position_name = serializers.CharField(max_length=200, required=True)
    schedule = serializers.IntegerField(required=True, )
    experience = serializers.IntegerField(required=True, )
    gender = serializers.CharField(required=True, )
    languages = serializers.ListField(required=True, )
    status = serializers.IntegerField(required=True, )
    region = serializers.IntegerField(required=True, )
    file = serializers.IntegerField(required=True, )
    district = serializers.IntegerField(required=True, )
    salary = salaryField()

    def __init__(self, *args, **kwargs):
        self.resume_id = kwargs.pop('resume')
        self.district_obj = None
        self.region_obj = None
        self.status_obj = None
        self.user_obj = None
        self.experience_obj = None
        self.schedule_obj = None
        self.file_obj = None
        self.categories = []
        self.languages_objs = []
        super(ResumeSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        if self.resume_id:
            try:
                resume_model = Resume.objects.get(id=self.resume_id)
            except Resume.DoesNotExist:
                raise serializers.ValidationError({'resume': ['resume not found']})
        else:
            resume_model = Resume()

        attrs['district'] = district = attrs.get('district', resume_model.district_id)
        attrs['region'] = region = attrs.get('region', resume_model.region_id)
        attrs['file'] = files = attrs.get('file', resume_model.files_id)
        attrs['status'] = status = attrs.get('status', resume_model.status_id)
        attrs['user'] = user = attrs.get('user', resume_model.user_id)
        attrs['experience'] = experience = attrs.get('experience', resume_model.experience_id)
        attrs['schedule'] = schedule = attrs.get('schedule', resume_model.schedule_id)
        categories = attrs.get('category', [])
        languages_objs = attrs.get('languages', [])
        if district:
            try:
                self.district_obj = District.objects.get(id=district)
            except District.DoesNotExist:
                raise serializers.ValidationError({'district': ['district not found']})
        if region:
            try:
                self.region_obj = Region.objects.get(id=region)
            except Region.DoesNotExist:
                raise serializers.ValidationError({'region': ['district not found']})
        if status:
            try:
                self.status_obj = Statuses.objects.get(id=status)
            except Statuses.DoesNotExist:
                raise serializers.ValidationError({'status': ['status not found']})

        if files:
            try:
                self.file_obj = Files.objects.get(id=files)
            except Files.DoesNotExist:
                raise serializers.ValidationError({'file': ['file not found']})

        if user:
            try:
                self.user_obj = Users.objects.get(id=user)
            except Users.DoesNotExist:
                raise serializers.ValidationError({'user': ['User not found']})
        if experience:
            try:
                self.experience_obj = Experience.objects.get(id=experience)
            except Experience.DoesNotExist:
                raise serializers.ValidationError({'experience': ['Experience not found']})

        if schedule:
            try:
                self.schedule_obj = Schedules.objects.get(id=schedule)
            except Schedules.DoesNotExist:
                raise serializers.ValidationError({'schedule': ['Schedules not found']})

        try:
            for data in categories:
                self.categories.append(Category.objects.get(pk=data))
        except Category.DoesNotExist:
            raise serializers.ValidationError({'categories': ['invalid categories']})

        try:
            for data in languages_objs:
                self.languages_objs.append(Languages.objects.get(pk=data))
        except Languages.DoesNotExist:
            raise serializers.ValidationError({'languages': ['invalid languages']})
        return attrs

    def save(self):
        if self.resume_id:
            try:
                resume_model = Resume.objects.get(id=self.resume_id)
            except Resume.DoesNotExist:
                raise serializers.ValidationError({'resume': ['resume not found']})
        else:
            resume_model = Resume()
        firstname = self.validated_data.get('firstname', resume_model.firstname)
        lastname = self.validated_data.get('lastname', resume_model.lastname)
        middlename = self.validated_data.get('middlename', resume_model.middlename)
        birthday = self.validated_data.get('birthday', resume_model.birthday)
        phone_number = self.validated_data.get('phone_number', resume_model.phone_number)
        position_name = self.validated_data.get('position_name', resume_model.position_name)
        salary = self.validated_data.get('salary', resume_model.salary)
        genders = self.validated_data.get('gender', None)
        manager = ResumeManager()

        if self.resume_id:
            resume = manager.updateResume(resume_model, self.user_obj, firstname, lastname, middlename, birthday, phone_number,
                                           position_name, self.categories, self.schedule_obj,
                                           self.experience_obj, self.region_obj, self.district_obj, salary,
                                           genders,
                                           self.languages_objs, self.status_obj, self.file_obj)
        else:
            resume = manager.createResume(self.user_obj, firstname, lastname, middlename, birthday, phone_number, position_name, self.categories, self.schedule_obj,
                                            self.experience_obj, self.region_obj, self.district_obj, salary,
                                            genders,
                                            self.languages_objs, self.status_obj, self.file_obj)

        return resume
