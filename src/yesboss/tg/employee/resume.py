import os.path
from datetime import datetime
from django.core.files import File
from django.conf import settings
from yesboss.hr.models import Resume, ResumeCategories, ResumeLanguage, Languages
from yesboss.storing.models import Files

from .employee_service import get_resume_one

MEDIA_DIR = settings.MEDIA_ROOT


def get_file_path(file_path):
    file = os.path.join(MEDIA_DIR, file_path)
    return file


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


def insertResume(bot, user_id, user_data):
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
        full_name = user_data.get('fio', None)
        phone_number = user_data.get('phone_number', None)
        if full_name:
            st_full_name = full_name.split(' ')
            if len(st_full_name) > 2:
                lastname = st_full_name[0]
                firstname = st_full_name[1]
                middlename = st_full_name[2]
            elif len(st_full_name) > 1:
                lastname = st_full_name[0]
                firstname = st_full_name[1]
                middlename = None
            else:
                lastname = st_full_name[0]
                firstname = None
                middlename = None
        else:
            firstname = None
            middlename = None
            lastname = None

        resume_model = Resume(user_id=user_id, schedule_id=schedule_id, files=files_model)
        resume_model.firstname = firstname
        resume_model.lastname = lastname
        resume_model.middlename = middlename
        resume_model.region_id = region_id
        resume_model.district_id = district_id
        resume_model.experience_id = experience_id
        resume_model.status_id = 1

        selected_gender = user_data.get('gender', '')

        if selected_gender == 'male':
            gender = 1
        elif selected_gender == 'female':
            gender = 2
        else:
            gender = None
        resume_model.gender = gender

        salary_type = user_data.get('salary_type', 2)
        if salary_type == 1:
            salary_amount = user_data.get('salary_amount', 0)
        else:
            salary_amount = None
        salary = {"from": 0, "to": 0, "text": salary_amount}

        birthday = user_data.get('dt', None)

        resume_model.salary = salary
        resume_model.birthday = birthday
        resume_model.position_name = user_data.get('position_name', '-')
        resume_model.phone_number = phone_number
        resume_model.save()

        cats = user_data.get('categories', [])
        for cat_id in cats:
            categories = ResumeCategories(resume=resume_model, category_id=cat_id)
            categories.save()

        langs = user_data.get('langs', [])
        for lang_id in langs:
            languages = ResumeLanguage(resume=resume_model, language_id=lang_id)
            languages.save()

    except Exception as e:
        print('insert error: ', str(e))


def change_gender(user_data, resume_id):
    selected_gender = user_data.get('gender', '')
    print(selected_gender)
    if selected_gender == 'male':
        gender = 1
    elif selected_gender == 'female':
        gender = 2
        print(gender)
    else:
        gender = None
    print(gender)
    Resume.objects.filter(pk=resume_id).update(gender=gender)


def change_schedule(resume_id, user_data):
    schedule_id = user_data.get('schedule_id', None)
    Resume.objects.filter(pk=resume_id).update(schedule_id=schedule_id)


def change_region(resume_id, user_data):
    region_id = user_data.get('region_id', None)
    Resume.objects.filter(pk=resume_id).update(region_id=region_id)


def change_district(resume_id, user_data):
    district_id = user_data.get('district_id', None)
    Resume.objects.filter(pk=resume_id).update(district_id=district_id)



def change_languages(resume_id, user_data):
    languages = user_data.get('langs', [])
    old_languages = []
    langs = ResumeLanguage.objects.raw('SELECT id, language_id FROM hr_resumelanguage WHERE resume_id = %s',
                                        [resume_id])
    if langs:
        for p in langs:
            old_languages.append(p.language_id)


    for language in languages:
        if language in old_languages:
            continue
        languages = ResumeLanguage(resume_id=resume_id, language_id=language)
        languages.save()

    for old in old_languages:
        if old in languages:
            continue
        ResumeLanguage.objects.filter(resume_id=resume_id, language_id=old).delete()


# ******************************


def change_position(user_data):
    resume_id = user_data.get('resume_id', None)
    position_name = user_data.get('position_name', '-')
    Resume.objects.filter(pk=resume_id).update(position_name=position_name)


def change_full_name(resume_id, full_name):
    print(resume_id, "change_full_name funksiaysi")
    if full_name:
        st_full_name = full_name.split(' ')
        if len(st_full_name) > 2:
            lastname = st_full_name[0]
            firstname = st_full_name[1]
            middlename = st_full_name[2]
        elif len(st_full_name) > 1:
            lastname = st_full_name[0]
            firstname = st_full_name[1]
            middlename = None
        else:
            lastname = st_full_name[0]
            firstname = None
            middlename = None

        Resume.objects.filter(pk=resume_id).update(firstname=firstname, lastname=lastname, middlename=middlename)
        return get_resume_one(resume_id)


def change_age(resume_id, user_data):
    birthday = user_data.get('dt', None)
    print(resume_id, "change_age funksiaysi")
    Resume.objects.filter(pk=resume_id).update(birthday=birthday)
    return get_resume_one(resume_id)


def delete_resume(resume_id, status):
    print(resume_id)
    a = Resume.objects.filter(pk=resume_id).update(status=status)
    print(a)

def change_photo(bot, user_id, user_data):
    resume_id = user_data.get('resume_id', None)
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
        Resume.objects.filter(pk=resume_id).update(files_id=files_model.id)
    else:
        files_model = None


def change_salary(resume_id, user_data):
    salary_type = user_data.get('salary_type', 2)
    if salary_type == 1:
        salary_amount = user_data.get('salary_amount', 0)
    else:
        salary_amount = None
    salary = {"from": 0, "to": 0, "text": salary_amount}
    Resume.objects.filter(pk=resume_id).update(salary=salary)


def change_phone(user_data):
    resume_id = user_data.get('resume_id', None)
    phone_number = user_data.get('phone_number', None)
    Resume.objects.filter(pk=resume_id).update(phone_number=phone_number)

def change_exp(resume_id, user_data):
    print("a")
    experience_id = user_data.get('experience_id', None)
    print(experience_id)
    Resume.objects.filter(pk=resume_id).update(experience_id=experience_id)
