import os.path
from datetime import datetime
from django.core.files import File
from django.conf import settings
from yesboss.hr.models import Vacancies, VacanciCategories, VacanciLanguage
from yesboss.storing.models import Files

from .hirer_service import get_vacancies_one

MEDIA_DIR = settings.MEDIA_ROOT

def get_folder():
    today = datetime.now()
    year = today.strftime("%Y")
    m = today.strftime("%m")
    path = os.path.join(MEDIA_DIR, 'hr')
    path = os.path.join(path, year, m)
    if not os.path.exists(path):
        os.makedirs(path)
    return path, f"hr/{year}/{m}"

def file_save(file, user_id):
    try:
        file_name = '%s%s' % (str(file['file_id']), datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        base, ext = os.path.splitext(file['file_path'])
        file_name = "".join([str(user_id), "_", file_name, ext])
        base_path, folder = get_folder()
        file_main = os.path.join(base_path, file_name)
        file.download(file_main)
        return folder, file_name
    except Exception as e:
        print('FILE SAVE ERROR', str(e))

def insertVacancies(bot, user_id, company_model, user_data):
    try:
        file_id = user_data.get('file_id', None)
        if file_id:
            file_type = user_data.get('file_type', None)
            if file_type:
                if file_type == 'photo':
                    file_type = 1
                else:
                    file_type = 2

            file = bot.getFile(file_id)
            file_path, file_name = file_save(file, user_id)
            files = "{}/{}".format(file_path, file_name)
            files_model = Files(file_type=file_type)
            files_model.file_path.name = files
            files_model.save()
        else:
            files_model = None

        schedule_id = user_data.get('schedule_id', None)
        region_id = user_data.get('region_id', None)
        district_id = user_data.get('district_id', None)
        experience_id = user_data.get('experience_id', None)

        vacancy_model = Vacancies(user_id=user_id, company_id=company_model.id, schedule_id=schedule_id, files=files_model)
        vacancy_model.region_id = region_id
        vacancy_model.district_id = district_id
        vacancy_model.experience_id = experience_id
        vacancy_model.status_id = 1

        selected_genders = user_data.get('genders', [])

        if 'male' in selected_genders and 'female' in selected_genders:
            gender = 3
        elif 'male' in selected_genders:
            gender = 1
        elif 'female' in selected_genders:
            gender = 2
        else:
            gender = None
        vacancy_model.gender = gender

        salary_type = user_data.get('salary_type', 2)
        if salary_type == 1:
            salary_amount = user_data.get('salary_amount', 0)
        else:
            salary_amount = None
        salary = {"from": 0, "to": 0, "text": salary_amount}

        age = user_data.get('age', None)
        if age:
            age_data = {"from": 0, "to": 0, "text": age}
        else:
            age_data = {"from": 0, "to": 0, "text": None}


        vacancy_model.salary = salary
        vacancy_model.age = age_data
        vacancy_model.position_name = user_data.get('position_name', '-')


        vacancy_model.save()

        cats = user_data.get('categories', [])
        for cat_id in cats:
            categories = VacanciCategories(vacancy=vacancy_model, category_id=cat_id)
            categories.save()

        langs = user_data.get('langs', [])
        for lang_id in langs:
            languages = VacanciLanguage(vacancy=vacancy_model, language_id=lang_id)
            languages.save()

    except Exception as e:
        print('insert error: ', str(e))

def get_file_path(file_path):
    file = os.path.join(MEDIA_DIR, file_path)
    return file


def change_position(vacancy_id, position_name):
    Vacancies.objects.filter(pk=vacancy_id).update(position_name=position_name)
    return get_vacancies_one(vacancy_id)

def change_age(vacancy_id, age):
    age_data = {"from": 0, "to": 0, "text": age}
    Vacancies.objects.filter(pk=vacancy_id).update(age=age_data)
    return get_vacancies_one(vacancy_id)

def change_languages(vacancy_id, selected_langs):
    old_languages = []
    for p in VacanciLanguage.objects.raw('SELECT id, language_id FROM hr_vacancilanguage WHERE vacancy_id = %s',
                                         [vacancy_id]):
        old_languages.append(p.language_id)

    for lang_id in selected_langs:
        if lang_id in old_languages:
            continue
        languages = VacanciLanguage(vacancy_id=vacancy_id, language_id=lang_id)
        languages.save()

    for lang_id in old_languages:
        if lang_id in selected_langs:
            continue
        VacanciLanguage.objects.filter(vacancy_id=vacancy_id, language_id=lang_id).delete()
    return get_vacancies_one(vacancy_id)

def change_vacancy_gender(vacancy_id, selected_gender):
    Vacancies.objects.filter(pk=vacancy_id).update(gender=selected_gender)
    return get_vacancies_one(vacancy_id)

def change_media(bot, user_id, user_data):
    vacancy_id = user_data.get('vacancy_id', None)
    file_id = user_data.get('file_id', None)
    if file_id:
        file_type = user_data.get('file_type', None)
        if file_type:
            if file_type == 'photo':
                file_type = 1
            else:
                file_type = 2

        file = bot.getFile(file_id)
        file_path, file_name = file_save(file, user_id)
        files = "{}/{}".format(file_path, file_name)
        files_model = Files(file_type=file_type)
        files_model.file_path.name = files
        files_model.save()
        Vacancies.objects.filter(pk=vacancy_id).update(files_id=files_model.id)
    else:
        files_model = None

def change_schedule(vacancy_id, selected_schedule):
    Vacancies.objects.filter(pk=vacancy_id).update(schedule_id=selected_schedule)
    return get_vacancies_one(vacancy_id)

def change_experience(vacancy_id, selected_experences):
    print('vacancy vacancy_id: ', vacancy_id)
    print('selected_experences: ', selected_experences)
    Vacancies.objects.filter(pk=vacancy_id).update(experience_id=selected_experences)

def change_salary(vacancy_id, user_data):
    salary_type = user_data.get('salary_type', 2)
    if salary_type == 1:
        salary_amount = user_data.get('salary_amount', 0)
    else:
        salary_amount = None
    salary = {"from": 0, "to": 0, "text": salary_amount}
    Vacancies.objects.filter(pk=vacancy_id).update(salary=salary)

def change_region(vacancy_id, user_data):
    region_id = user_data.get('region_id', None)
    print("salom", vacancy_id, region_id)
    Vacancies.objects.filter(pk=vacancy_id).update(region_id=region_id)

def change_district(vacancy_id, user_data):
    district_id = user_data.get('district_id', None)
    Vacancies.objects.filter(pk=vacancy_id).update(district_id=district_id)

def delete_vacancy(vacancy_id,  status):
    Vacancies.objects.filter(pk=vacancy_id).update(status=status)
    return get_vacancies_one(vacancy_id)

