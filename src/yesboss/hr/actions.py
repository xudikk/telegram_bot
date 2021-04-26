from django.db import transaction
from .models import Vacancies, VacanciCategories, VacanciLanguage, Resume, ResumeCategories, ResumeLanguage

class VacnacyManager(object):

    def createVacanvy(self, company, position_name, categories, schedule, experience, region, district, salary, age, genders, languages, status, file):
        with transaction.atomic():
            user_id = company.user_id
            vacancy_model = Vacancies(user_id=user_id, company=company, schedule=schedule, files=file)
            vacancy_model.region = region
            vacancy_model.district = district
            vacancy_model.experience = experience
            vacancy_model.status = status

            if 'male' in genders and 'female' in genders:
                gender = 3
            elif 'male' in genders:
                gender = 1
            elif 'female' in genders:
                gender = 2
            else:
                gender = None
            vacancy_model.gender = gender

            salary = {"from": salary.get('from_price', '0'), "to": salary.get('to_price', '0'), "text": salary.get('text', '0')}
            age_data = {"from": age.get('from_age', '0'), "to": age.get('to_age', '0'), "text": age.get('text', '0')}

            vacancy_model.salary = salary
            vacancy_model.age = age_data
            vacancy_model.position_name = position_name

            vacancy_model.save()
            for category in categories:
                categories = VacanciCategories(vacancy=vacancy_model, category=category)
                categories.save()


            for language in languages:
                languages = VacanciLanguage(vacancy=vacancy_model, language=language)
                languages.save()

        return vacancy_model

    def updateVacanvy(self, vacancy_model, company, position_name, categories, schedule, experience, region, district, salary, age, genders, languages, status, file):
        with transaction.atomic():
            user_id = company.user_id
            vacancy_model.user_id = user_id
            vacancy_model.company = company
            vacancy_model.schedule = schedule
            vacancy_model.files = file
            vacancy_model.region = region
            vacancy_model.district = district
            vacancy_model.experience = experience
            vacancy_model.status = status

            if 'male' in genders and 'female' in genders:
                gender = 3
            elif 'male' in genders:
                gender = 1
            elif 'female' in genders:
                gender = 2
            else:
                gender = None
            vacancy_model.gender = gender

            salary = {"from": salary.get('from_price', '0'), "to": salary.get('to_price', '0'), "text": salary.get('text', '0')}
            age_data = {"from": age.get('from_age', '0'), "to": age.get('to_age', '0'), "text": age.get('text', '0')}

            vacancy_model.salary = salary
            vacancy_model.age = age_data
            vacancy_model.position_name = position_name

            vacancy_model.save()
            old_categories = []
            for p in VacanciCategories.objects.raw('SELECT id, category_id, vacancy_id FROM hr_vacancicategories WHERE vacancy_id = %s', [vacancy_model.id]):
                old_categories.append(p.category_id)
            new_categories = []
            for category in categories:
                new_categories.append(category.id)
                if category.id in old_categories:
                    continue
                categories = VacanciCategories(vacancy=vacancy_model, category=category)
                categories.save()


            for old in old_categories:
                if old in new_categories:
                    continue
                VacanciCategories.objects.filter(vacancy=vacancy_model, category_id=old).delete()

            old_languages = []
            for p in VacanciLanguage.objects.raw('SELECT id, language_id FROM hr_vacancilanguage WHERE vacancy_id = %s', [vacancy_model.id]):
                old_languages.append(p.language_id)

            new_langs = []
            for language in languages:
                new_langs.append(language.id)
                if language.id in old_languages:
                    continue
                languages = VacanciLanguage(vacancy=vacancy_model, language=language)
                languages.save()

            for old in old_languages:
                if old in new_langs:
                    continue
                VacanciLanguage.objects.filter(vacancy=vacancy_model, language_id=old).delete()

        return vacancy_model


class ResumeManager(object):

    def createResume(self, user, firstname, lastname, middlename, birthday, phone_number, position_name, categories, schedule, experience, region, district, salary, gender, languages, status, file):
        with transaction.atomic():
            user_id = user.id
            resume_model = Resume(user_id=user_id, firstname=firstname, lastname=lastname, middlename=middlename,
                                   birthday=birthday, phone_number=phone_number, schedule=schedule, files=file)
            resume_model.region = region
            resume_model.district = district
            resume_model.experience = experience
            resume_model.status = status


            if 'male' == gender:
                gender = 1
            elif 'female' == gender:
                gender = 2
            else:
                gender = None
            resume_model.gender = gender

            salary = {"from": salary.get('from_price', '0'), "to": salary.get('to_price', '0'), "text": salary.get('text', '0')}

            resume_model.salary = salary
            resume_model.position_name = position_name

            resume_model.save()
            for category in categories:
                categories = ResumeCategories(resume=resume_model, category=category)
                categories.save()

            for language in languages:
                languages = ResumeLanguage(resume=resume_model, language=language)
                languages.save()

        return resume_model

    def updateResume(self, resume_model, user, firstname, lastname, middlename, birthday, phone_number, position_name, categories, schedule, experience, region, district, salary, gender, languages, status, file):
        with transaction.atomic():
            user_id = user.id
            resume_model.user_id = user_id
            resume_model.firstname = firstname
            resume_model.lastname = lastname
            resume_model.middlename = middlename
            resume_model.birthday = birthday
            resume_model.phone_number = phone_number
            resume_model.schedule = schedule
            resume_model.files = file
            resume_model.region = region
            resume_model.district = district
            resume_model.experience = experience
            resume_model.status = status


            if 'male' == gender:
                gender = 1
            elif 'female' == gender:
                gender = 2
            else:
                gender = None
            resume_model.gender = gender

            salary = {"from": salary.get('from_price', '0'), "to": salary.get('to_price', '0'), "text": salary.get('text', '0')}

            resume_model.salary = salary
            resume_model.position_name = position_name

            resume_model.save()

            old_categories = []
            for p in ResumeCategories.objects.raw(
                    'SELECT id, category_id, resume_id FROM hr_resumecategories WHERE resume_id = %s',
                    [resume_model.id]):
                old_categories.append(p.category_id)

            new_categories = []
            for category in categories:
                new_categories.append(category.id)
                if category.id in old_categories:
                    continue
                categories = ResumeCategories(resume=resume_model, category=category)
                categories.save()

            for old in old_categories:
                if old in new_categories:
                    continue
                ResumeCategories.objects.filter(resume=resume_model, category_id=old).delete()

            old_languages = []
            for p in ResumeLanguage.objects.raw('SELECT id, language_id FROM hr_resumelanguage WHERE resume_id = %s',
                                                [resume_model.id]):
                old_languages.append(p.language_id)

            new_langs = []
            for language in languages:
                new_langs.append(language.id)
                if language.id in old_languages:
                    continue
                languages = ResumeLanguage(resume=resume_model, language=language)
                languages.save()

            for old in old_languages:
                if old in new_langs:
                    continue
                ResumeLanguage.objects.filter(resume=resume_model, language_id=old).delete()


        return resume_model
