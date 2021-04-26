# -*- coding: utf-8 -*-
from contextlib import closing
from django.db import connection
from collections import namedtuple
from datetime import datetime

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

def createCompany(user_id, data):
    with closing(connection.cursor()) as cursor:
        sql = """INSERT INTO company_companies (user_id, company_name, phone_number, is_terms) VALUES (%s, %s, %s, %s) returning id"""
        cursor.execute(sql, [
            user_id, data['company_name'], data['phone_number'], False
        ])
        company_id = dictfetchone(cursor)['id']
    return company_id

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


def getCategoryParent():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category where is_active = true and parent_id is null limit 30")
        user = dictfetchall(cursor)
    return user

def categoryByID(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, parent_id,name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category where id = %s", [id])
        user = dictfetchone(cursor)
    return user

def getCategoryChild(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_category where is_active = true and parent_id = %s limit 30", [id])
        user = dictfetchall(cursor)
    return user

def getPositions(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("select id, name->>'uz' as name_1, name->>'ru' as name_2 from hr_positions where category_id = %s order by sort_order asc limit 10", [category_id])
        positions = dictfetchall(cursor)
    return positions

def getSchedules():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_schedules limit 20")
        user = dictfetchall(cursor)
    return user

def schuduleByID(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id,name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_schedules where id = %s", [id])
        user = dictfetchone(cursor)
    return user

def getLanguages():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_languages order by sort_order asc limit 20")
        user = dictfetchall(cursor)
    return user

def getLanguagesByids(ids):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_languages where id in ({}) limit 20".format(ids))
        user = dictfetchall(cursor)
    return user

def getExperiences():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_experience order by sort_order asc limit 20")
        user = dictfetchall(cursor)
    return user

def getExperienceById(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name->>'uz' as name_1, name->>'ru' as name_2 FROM hr_experience where id=%s limit 1", [id])
        user = dictfetchone(cursor)
    return user

def getRegions():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name_uz as name_1, name_ru as name_2 FROM geo_region where country_id = 239 order by ordering asc limit 20")
        regions = dictfetchall(cursor)
    return regions

def getRegionById(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name_uz as name_1, name_ru as name_2 FROM geo_region where id = %s limit 1", [id])
        regions = dictfetchone(cursor)
    return regions

def getDistricts(region_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name_uz as name_1, name_ru as name_2 FROM geo_district where region_id = %s order by ordering asc limit 20", [region_id])
        districts = dictfetchall(cursor)
    return districts


def getDistrictById(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT id, name_uz as name_1, name_ru as name_2 FROM geo_district where id = %s limit 1", [id])
        districts = dictfetchone(cursor)
    return districts


def getMyVacancies(user_id, count):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select company.company_name, vacancy.id as vacancy_id, position_name, vacancy.salary, 
        schedule.name as schedule_name, select_languages.langs, vacancy.age as vacancy_age, experience.name as experience_name, 
        gender, region.name_ru as region_name_ru,region.name_uz as region_name_uz,
        district.name_ru as district_name_ru, district.name_uz as district_name_uz, storing_files.file_type, storing_files.file_path
       
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
        where vacancy.user_id = %s and (vacancy.status_id = 1 or vacancy.status_id = 2)
        order by vacancy.created_dt desc
        limit 1 offset {count-1}
        """, [user_id])
        vacancies = dictfetchone(cursor)
    return vacancies


def get_cnt_vac(user_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""
        select count(1) as cnt
        from hr_vacancies vacancy
        inner join user_users user_id on vacancy.user_id = user_id.id
        where user_id.tg_id  = %s and (vacancy.status_id = 1 or vacancy.status_id = 2)
        """, [user_id])
        resume = dictfetchone(cursor)
    return resume


def get_vacancies_one( vacancy_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select company.company_name, vacancy.id as vacancy_id, position_name, vacancy.salary, 
        schedule.name as schedule_name, select_languages.langs, vacancy.age as vacancy_age, experience.name as experience_name, 
        gender, region.name_ru as region_name_ru,region.name_uz as region_name_uz,
        district.name_ru as district_name_ru, district.name_uz as district_name_uz, storing_files.file_type, storing_files.file_path
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
        where vacancy.id  = %s
        """, [vacancy_id])
        vacancies = dictfetchone(cursor)
    return vacancies


def getResumeByName(name):
    print('come ')
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute("select * from hr_vacancies where position_name like '%s%'", [name])
            resumes = dictfetchall(cursor)
            print(resumes)
        return resumes
    except Exception as e:
        print('error:  :  :  ', e)