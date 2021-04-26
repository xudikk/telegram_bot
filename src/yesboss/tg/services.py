# -*- coding: utf-8 -*-
from contextlib import closing
from django.db import connection
from collections import namedtuple
from random import randint
from datetime import datetime
import logging
import json
from ..user.models import Users, Contacts


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def createTgUser(user_id, first_name, username):
    try:
        with closing(connection.cursor()) as cursor:
            strtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO tg_users(user_id, first_name, username, created_at) VALUES(%s, %s, %s, %s)"
            cursor.execute(sql, [user_id, first_name, username, strtime])
            cursor.execute("SELECT * FROM tg_users where user_id = %s", [user_id])
            user = dictfetchone(cursor)
            return user
    except Exception as e:
        print("Error:", e)


def createUser(user_id, price, numbs):
    try:
        with closing(connection.cursor()) as cursor:
            strtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO tg_balance(user_id, price, created_at, is_payed, number_pay) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(sql, [user_id, price, strtime, False, numbs])
            return True
    except Exception as e:
        return False


def userByID(user_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM user_users where tg_id = %s", [user_id])
        user = dictfetchone(cursor)
    return user


def tgUserByID(user_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM tg_users where user_id = %s", [user_id])
        user = dictfetchone(cursor)
    return user


def contactUserByID(user_id, phone_number):
    if phone_number and phone_number[0] != '+':
        phone_number = f'+{phone_number}'
    with closing(connection.cursor()) as cursor:
        cursor.execute('SELECT id FROM user_contacts where user_id = %s and phone_number=%s', [user_id, phone_number])
        user = dictfetchone(cursor)
    if user:
        return user['id']
    else:
        contact = Contacts(user_id=user_id, phone_number=phone_number)
        contact.save()
        return contact.id


def contactByID(contact_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM user_contacts where id = %s", [contact_id])
        contact = dictfetchone(cursor)
    return contact


def categoryByID(ctg_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT id, parent_id,name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category where id = %s",
            [ctg_id])
        user = dictfetchone(cursor)
    return user


def getCategoryParent():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category 
            where is_active = true and parent_id is null limit 30""")
        user = dictfetchall(cursor)
    return user


def getSchedules():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_schedules limit 20")
        user = dictfetchall(cursor)
    return user


def getLanguages():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_languages 
            order by sort_order asc limit 20""")
        user = dictfetchall(cursor)
    return user


def getExperiences():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 
            FROM hr_experience order by sort_order asc limit 20""")
        user = dictfetchall(cursor)
    return user


def getPositions(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select id, name->>'uz' as name_1, name->>'ru' as name_2 from hr_positions 
            where category_id = %s order by sort_order asc limit 10""",
            [category_id])
        positions = dictfetchall(cursor)
    return positions


def tgChangeLang(user_id, lang_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("UPDATE tg_users SET lang = %s WHERE user_id=%s", [lang_id, user_id])


def tgChangeType(user_id, type_id, tg_model):
    with closing(connection.cursor()) as cursor:
        cursor.execute("UPDATE tg_users SET user_type_id = %s WHERE user_id=%s", [type_id, user_id])
    Users.objects.create_user_tg(user_id, tg_model['phone_number'], tg_model['first_name'], type_id, tg_model['lang'])


def tgChangePhone(user_id, phone_number):
    with closing(connection.cursor()) as cursor:
        cursor.execute("UPDATE tg_users SET phone_number = %s WHERE user_id=%s", [phone_number, user_id])


def getDistricts(region_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT id, name_uz as name_1, name_ru as name_2 FROM geo_district 
            where region_id = %s order by ordering asc limit 20""",
            [region_id])
        user = dictfetchall(cursor)
    return user


def getDistrictAndRegion(district_id):
    with closing(connection.cursor()) as cursor:
        sql = """select geo_region.name_uz as region_name_uz, geo_region.name_ru as region_name_ru, 
                geo_district.* from geo_district
        inner join geo_region on geo_region.id = geo_district.region_id 
        where geo_district.id = %s"""
        cursor.execute(sql, [district_id])
        result = dictfetchone(cursor)
    return result


def getExperienceById(experience_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_experience where id = {}".format(experience_id)
        cursor.execute(sql)
        experience = dictfetchone(cursor)
    return experience['name']


def getPositionById(position_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_positions where id = {}".format(position_id)
        cursor.execute(sql)
        experience = dictfetchone(cursor)
    return experience['name']


def getLanguagesByIds(ids):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_languages where id in ({})".format(ids)
        cursor.execute(sql)
        languages = dictfetchall(cursor)
    return languages


def getScheduleById(schedule_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_schedules where id = {}".format(schedule_id)
        cursor.execute(sql)
        schedule = dictfetchone(cursor)
    return schedule['name']


def getCategoriesByIds(ids):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_category where id in ({})".format(ids)
        cursor.execute(sql)
        categories = dictfetchall(cursor)
    return categories


def getCategoryById(category_id):
    with closing(connection.cursor()) as cursor:
        sql = "select name->>'uz' as name_1, name->>'ru' as name_2 from hr_category where id = {}".format(category_id)
        cursor.execute(sql)
        category = dictfetchone(cursor)
    return category


def createCompany(data):
    with closing(connection.cursor()) as cursor:
        sql = """INSERT INTO company_companies 
        (user_id, company_name, phone_number, district_id) VALUES (%s, %s, %s, %s) returning id"""
        cursor.execute(sql, [
            data['user_id'], data['company_name'], data['phone_number'], data['district_id'],
        ])
        company_id = dictfetchone(cursor)['id']
    return company_id


def createVacancy(data):
    try:
        with closing(connection.cursor()) as cursor:
            strtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = """INSERT INTO hr_vacancies (
                    user_id, company_id, schedule_id, category_id, subcats, requirements,
                    status_id, district_id, region_id, salary, experience_id,
                    age, languages, views_count, contact_count, gender, 
                    position_id, file_type, file_path, contacts, created_dt
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, [
                data['user_id'], data['company_id'], data['schedule_id'], data['category_id'], data['subcats'],
                data['requirements'],
                data['status_id'], data['district_id'], data['region_id'], data['salary'], data['experience_id'],
                data['age'], data['languages'], 0, 0, data['gender'], data['position_id'], data['file_type'],
                data['file_path'], data['contacts'], strtime
            ])
    except Exception as e:
        print("Vacancy Error:", e)


def createResume(data):
    with closing(connection.cursor()) as cursor:
        strtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """INSERT INTO hr_resume (
        user_id, full_name, schedule_id, category_id, subcats, position_id,
        status_id, district_id, region_id, salary, experience_id,
        languages, contacts, about, age, gender, skills,
        file_type, file_path, views_count, contact_count,
        created_dt
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, [
            data['user_id'], data['full_name'], data['schedule_id'], data['category_id'], data['subcats'],
            data['position_id'],
            data['status_id'], data['district_id'], data['region_id'], data['salary'], data['experience_id'],
            data['languages'], data['contacts'], data['about'], data['age'],
            data['gender'], data['skills'], data['file_type'], data['file_path'], 0, 0, strtime
        ])


def getResumes(user_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_resume where user_id = {} order by created_dt desc limit 2".format(user_id)
        cursor.execute(sql)
        resumes = dictfetchall(cursor)
    return resumes


def deleteResume(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "delete from hr_resume where id = {}".format(resume_id)
        cursor.execute(sql)


def getResumeById(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_resume where id = {}".format(resume_id)
        cursor.execute(sql)
        resume = dictfetchone(cursor)
    return resume


def deactivateResume(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "update hr_resume set status_id = 2 where id = {}".format(resume_id)
        cursor.execute(sql)


def activateResume(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "update hr_resume set status_id = 1 where id = {}".format(resume_id)
        cursor.execute(sql)


def getVacancies(user_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_vacancies where user_id = {} order by created_dt desc limit 2".format(user_id)
        cursor.execute(sql)
        resumes = dictfetchall(cursor)
    return resumes


def deleteVacancy(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "delete from hr_vacancies where id = {}".format(resume_id)
        cursor.execute(sql)


def getVacancyById(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_vacancies where id = {}".format(resume_id)
        cursor.execute(sql)
        resume = dictfetchone(cursor)
    return resume


def deactivateVacancy(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "update hr_vacancies set status_id = 2 where id = {}".format(resume_id)
        cursor.execute(sql)


def activateVacancy(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = "update hr_vacancies set status_id = 1 where id = {}".format(resume_id)
        cursor.execute(sql)


def getCompanyById(company_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from company_companies where id = {}".format(company_id)
        cursor.execute(sql)
        resume = dictfetchone(cursor)
    return resume


def getCompanyByUserId(user_id):
    with closing(connection.cursor()) as cursor:
        sql = "select * from company_companies where user_id = {}".format(user_id)
        cursor.execute(sql)
        resume = dictfetchone(cursor)
    return resume


def updateResumeData(resume_id, key, value):
    try:
        with closing(connection.cursor()) as cursor:
            sql = "update hr_resume set {} = {} where id = {}".format(key, "'{}'".format(value), resume_id)
            cursor.execute(sql)
    except Exception as e:
        print("Err:", e)


def updateVacancyData(vacancy_id, key, value):
    with closing(connection.cursor()) as cursor:
        sql = "update hr_vacancies set {} = {} where id = {}".format(key, "'{}'".format(value), vacancy_id)
        cursor.execute(sql)


def changeUserProfile(user_id, key, value):
    with closing(connection.cursor()) as cursor:
        sql = "update tg_users set {} = {} where user_id = {}".format(key, "'{}'".format(value), user_id)
        cursor.execute(sql)
        sql = "update user_users set {} = {} where tg_id = {}".format(key, "'{}'".format(value), user_id)
        cursor.execute(sql)


def changeUserProfileType(user_id, value):
    with closing(connection.cursor()) as cursor:
        sql = "update tg_users set user_type_id = {} where user_id = {}".format("'{}'".format(value), user_id)
        cursor.execute(sql)
        sql = "update user_users set types_id = {} where tg_id = {}".format("'{}'".format(value), user_id)
        cursor.execute(sql)


def changeCompanyProfile(user_id, key, value):
    with closing(connection.cursor()) as cursor:
        sql = "update company_companies set {} = {} where user_id = {}".format(key, "'{}'".format(value), user_id)
        cursor.execute(sql)


def searchResume(filter_data):
    with closing(connection.cursor()) as cursor:
        # sql = "select * from hr_resume where gender in ({}) and experience_id = {}"
        # cursor.execute(sql.format(filter_data['gender'], filter_data['experience_id']))
        sql = "select * from hr_resume"
        cursor.execute(sql)
        result = dictfetchall(cursor)
    return result


def searchVacancy(filter_data):
    with closing(connection.cursor()) as cursor:
        sql = "select * from hr_vacancies"
        cursor.execute(sql)
        result = dictfetchall(cursor)
    return result


def getResumeCategories(resume_id):
    with closing(connection.cursor()) as cursor:
        sql = """select category_id from hr_resumecategories where resume_id = %s"""
        cursor.execute(sql, [resume_id])
        categories = [c['category_id'] for c in dictfetchall(cursor)]
    return categories


def getUserContact(user_id):
    with closing(connection.cursor()) as cursor:
        sql = """select phone_number from user_contacts where user_id = %s"""
        cursor.execute(sql, [user_id])
        contacts = [c['phone_number'] for c in dictfetchall(cursor)]
    return contacts


def getParentCategories():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT id, parent_id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category 
            where is_active = true and parent_id is null limit 30""")
        user = dictfetchall(cursor)
    return user


def searchCategory(name, parent_id=None):
    if parent_id:
        parent = f'and parent_id={parent_id}'
    else:
        parent = 'and parent_id is null'
    with closing(connection.cursor()) as cursor:
        sql = """select id, parent_id, name->>'uz' as name_1, name->>'ru' as name_2 
from hr_category 
where (name->>'uz' = %s or name->>'ru' = %s) {parent}""".format(parent=parent)
        print(name)
        cursor.execute(sql, [name, name])
        category = dictfetchone(cursor)
    return category


def getCategoryChild(id, cats):
    with closing(connection.cursor()) as cursor:
        if cats and len(cats) > 0:
            st = ', '.join([str(elem) for elem in cats])
            where = f" and id not in ({st})"
            print(st)
        else:
            where = ''
        cursor.execute(
            f"""SELECT id, parent_id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category 
            where is_active = true and parent_id = %s{where} limit 30""",
            [id])
        user = dictfetchall(cursor)
    return user


def getRegions():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT id, name_uz as name_1, name_ru as name_2 FROM geo_region where country_id = 239 
            order by ordering asc limit 20""")
        user = dictfetchall(cursor)
    return user


def searchRegion(name, region_id=None):
    if region_id:
        parent = f'and id={region_id}'
    else:
        parent = ""
    with closing(connection.cursor()) as cursor:
        sql = """select id,  name_uz as name_1, name_ru as name_2 
            from geo_region 
            where (name_uz = %s or name_ru = %s) {parent}""".format(parent=parent)
        cursor.execute(sql, [name, name])
        region = dictfetchone(cursor)

    return region


def Districts(region_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT id, region_id, name_uz as name_1, name_ru as name_2 
                FROM geo_district where region_id = %s limit 30""",
            [region_id])
        rows = dictfetchall(cursor)
    print(rows)
    return rows


def district_by_name(name):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT id, region_id, name_uz as name_1, name_ru as name_2 
                FROM geo_district where (name_uz = %s or name_ru = %s) """,
            [name, name])
        rows = dictfetchone(cursor)
    print(rows)
    return rows


def schedule_by_name(name):
    with closing(connection.cursor()) as cursor:
        print("name: ", name)
        cursor.execute(
            f"""SELECT id, name->>'uz' as name_1, name->>'ru' as name_2, name->>'en' as name_3
                FROM hr_schedules where (name->>'uz' = %s or name->>'ru' = %s or name->>'en' = %s) """,
            [name, name, name])
        rows = dictfetchone(cursor)
    print(rows)
    return rows


def search_language_by_name(name):
    with closing(connection.cursor()) as cursor:
        sql = """select id, name->>'uz' as name_1, name->>'ru' as name_2 
            from hr_languages 
            where (name->>'uz' = %s or name->>'ru' = %s)"""
        cursor.execute(sql, [name, name])
        row = dictfetchone(cursor)
    return row


def get_languages(selected):
    with closing(connection.cursor()) as cursor:
        if selected and len(selected) > 0:
            st = ', '.join([str(elem) for elem in selected])
            where = f"where id not in ({st})"
        else:
            where = ''
        cursor.execute(
            f"SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_languages {where}limit 5")
        rows = dictfetchall(cursor)
    return rows


def select_exp_by_name(name):
    with closing(connection.cursor()) as cursor:
        sql = """select id, name->>'uz' as name_1, name->>'ru' as name_2 
               from hr_experience 
               where (name->>'uz' = %s or name->>'ru' = %s)"""
        cursor.execute(sql, [name, name])
        row = dictfetchone(cursor)
    return row


def select_schedule_by_name(name):
    with closing(connection.cursor()) as cursor:
        sql = """select id, name->>'uz' as name_1, name->>'ru' as name_2 
               from hr_experience 
               where (name->>'uz' = %s or name->>'ru' = %s)"""
        cursor.execute(sql, [name, name])
        row = dictfetchone(cursor)
    return row


# **********************************************************************************************************************

def search_vacancy(keyword, count):
    with closing(connection.cursor()) as cursor:
        sql = f"""
                   select company.company_name, vacancy.id as vacancy_id, position_name, vacancy.salary, 
        schedule.name as schedule_name, select_languages.langs, vacancy.age as vacancy_age, 
        experience.name as experience_name, 
        company.phone_number as phone_number,
        gender, region.name_ru as region_name_ru,region.name_uz as region_name_uz,
        district.name_ru as district_name_ru, district.name_uz as district_name_uz, 
        storing_files.file_type, storing_files.file_path
        from hr_vacancies vacancy
        inner join company_companies company on vacancy.company_id  = company.id
        inner join hr_schedules schedule on vacancy.schedule_id  = schedule.id
        inner join (
            select vacancy_id, array_to_json(array_agg(row_to_json(hr_languages))) as langs
            from hr_vacancilanguage as languages
            inner join hr_languages on languages.language_id = hr_languages.id
            group by languages.vacancy_id 
            
        ) select_languages on vacancy.id = select_languages.vacancy_id
        inner join hr_experience as experience on vacancy.experience_id = experience.id
        inner join geo_region region on vacancy.region_id  = region.id 
        inner join geo_district district on vacancy.district_id  = district.id
        left join storing_files on vacancy.files_id = storing_files.id
        
        where position_name like'%{keyword}%' or vacancy.id in (select distinct hr_vacancicategories.vacancy_id 
        from hr_category
        inner join hr_vacancicategories on hr_category.id = hr_vacancicategories.category_id 
        where hr_category.name->>'uz' like '%{keyword}%' or hr_category.name->>'ru' like '%{keyword}%')
        order by vacancy.created_dt desc
        limit 1 offset {count-1}

                  """
        cursor.execute(sql)
        row = dictfetchone(cursor)
    return row


def vac_count(keyword):
    with closing(connection.cursor()) as cursor:
        sql = f"""
                select count(1) as cnt
                from hr_vacancies vacancy
                inner join company_companies company on vacancy.company_id  = company.id
                where position_name like '%{keyword}%' or vacancy.id in (select distinct hr_vacancicategories.vacancy_id 
                from hr_category
                inner join hr_vacancicategories on hr_category.id = hr_vacancicategories.category_id 
                where hr_category.name->>'uz' like '%{keyword}%' or hr_category.name->>'ru' like '%{keyword}%')
            """
        cursor.execute(sql)
        row = dictfetchone(cursor)
    return row


def search_vac_phone_number(vac_id):
    with closing(connection.cursor()) as cursor:
        sql = f"""
                select vacancy.id as vac_id, company.phone_number as phone_number, company.company_name as comp_name
                from hr_vacancies vacancy
                inner join company_companies company on vacancy.company_id  = company.id
                where vacancy.id = {vac_id}
                """
        cursor.execute(sql)
        row = dictfetchone(cursor)
    return row



def search_resume(keyword, count):
    with closing(connection.cursor()) as cursor:
        sql = f"""
        select  resume.id as resume_id, position_name, resume.salary, 
        schedule.name as schedule_name, select_languages.langs, resume.birthday as user_age, 
        experience.name as experience_name, gender, region.name_ru as region_name_2,region.name_uz as region_name_1,
        district.name_ru as district_name_2, district.name_uz as district_name_1,
        user_id, resume.phone_number, resume.firstname, resume.lastname, resume.middlename,
        files.file_type as file_type, files.file_path, files.id as file_id, region.id as re_id, 
        district.id as dis_id
        
        from hr_resume 
        resume inner join hr_schedules schedule on resume.schedule_id  = schedule.id
        inner join (
            select resume_id, array_to_json(array_agg(row_to_json(hr_languages))) as langs
            from hr_resumelanguage as languages
            inner join hr_languages on languages.language_id = hr_languages.id
            group by languages.resume_id
        ) select_languages on resume.id = select_languages.resume_id
        inner join hr_experience as experience on resume.experience_id = experience.id
        inner join geo_region region on resume.region_id  = region.id 
        inner join geo_district district on resume.district_id  = district.id
        inner join user_users user_id on resume.user_id = user_id.id
        inner join storing_files files on resume.files_id = files.id

         where (position_name like '%{keyword}%') or resume.id in (select distinct hr_resumecategories.resume_id 
        from hr_category
        inner join hr_resumecategories on hr_category.id = hr_resumecategories.category_id 
        where hr_category.name->>'uz' like '%{keyword}%' or hr_category.name->>'ru' like '%{keyword}%')
        order by resume.created_dt desc
        limit 1 offset {count-1}
                  """
        cursor.execute(sql)
        row = dictfetchone(cursor)
    return row


def resume_count(keyword):
    with closing(connection.cursor()) as cursor:
        sql = f"""
                select count(1) as cnt
        from hr_resume resume
        where (position_name like '%{keyword}%') or resume.id in (select distinct hr_resumecategories.resume_id 
        from hr_category
        inner join hr_resumecategories on hr_category.id = hr_resumecategories.category_id 
        where hr_category.name->>'uz' like '%{keyword}%' or hr_category.name->>'ru' like '%{keyword}%')
            """
        cursor.execute(sql)
        row = dictfetchone(cursor)
    return row


def search_resume_phone_number(res_id):
    with closing(connection.cursor()) as cursor:
        sql = f"""
                select id as resume_id, phone_number, firstname, lastname, middlename
                from hr_resume resume
                where id = {res_id}
                """
        cursor.execute(sql)
        row = dictfetchone(cursor)
    return row


def user_ChangeLang(id, lang_id):
    print('services: ', lang_id)
    with closing(connection.cursor()) as cursor:
        cursor.execute("UPDATE user_users SET lang = %s WHERE id=%s", [lang_id, id])



