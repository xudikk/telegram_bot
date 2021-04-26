# -*- coding: utf-8 -*-
import json
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings
from ...base.utils.sqlpaginator import SqlPaginator
from ...base.utils.db import dictfetchone, dictfetchall

PER_PAGE = settings.PAGINATE_BY

MEDIA_URL = settings.MEDIA_LINK
def get_list_vacancies(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    if "category" in request.query_params:
        try:
            category = int(request.query_params.get('category', 1))
            category_filter = " and hr_category.id = %s" % category
        except:
            category_filter = ""
    else:
        category_filter = ""



    if "company" in request.query_params:
        try:
            company_id = int(request.query_params.get('company', 0))
            filter_query = f" where hr_vacancies.company_id = %s" % company_id
        except:
            filter_query = ""
    else:
        filter_query = ""

    count_records = _count_list_vacancies(filter_query, category_filter)

    rows = _get_all_vacancies(page, filter_query, category_filter)
    result = []

    for data in rows:
        result.append(_format_vacancy_list(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_one_vacancy(request, id):
    data = _get_one_vacancies(id)

    result = OrderedDict([
        ('item', _format_vacancy(data))
    ])
    return result


def _get_all_vacancies(page, filter_query, category_filter):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select hr_vacancies.id as vacancy_id, position_name, salary, created_dt , updated_dt, categories.cats, 
company.company_name, company.id as company_id, company.phone_number as phone_number,
users.id as user_id, users.first_name, status.alias as status_alias, status."name"->>'ru' as status_name, hr_vacancies.status_id
from hr_vacancies
inner join user_users users on hr_vacancies.user_id = users.id
inner join company_companies company on hr_vacancies.company_id = company.id
inner join hr_statuses status on hr_vacancies.status_id = status.id
inner join (select vacancy_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_vacancicategories as categories
    inner join hr_category on categories.category_id = hr_category.id{category_filter}
    group by categories.vacancy_id 
) categories on hr_vacancies.id = categories.vacancy_id{filter_query}
ORDER BY updated_dt desc
limit %s OFFSET %s
            """
    print(extra_sql)

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows



def _get_one_vacancies(id):

    extra_sql = f"""select hr_vacancies.id as vacancy_id, position_name, storing_files.file_type , storing_files.file_path, salary, hr_vacancies.age as hr_age, views_count, gender,
hr_vacancies.created_dt , hr_vacancies.updated_dt, categories.cats, languages.langs, company.company_name, company.id as company_id, company.phone_number as phone_number,
users.id as user_id, users.first_name, status.alias as status_alias, status."name"->>'ru' as status_name, schedule.id as schedule_id, schedule."name"->>'ru' as schedule_name,
region.id as region_id, region.name_ru as region_name, district.id as district_id, district.name_ru as district_name, hr_vacancies.status_id, experience.id as experience_id, experience.name->>'ru' as experience_name 
from hr_vacancies
inner join user_users users on hr_vacancies.user_id = users.id
inner join company_companies company on hr_vacancies.company_id = company.id
inner join hr_statuses status on hr_vacancies.status_id = status.id
left join geo_region region on hr_vacancies.region_id = region.id
left join geo_district district on hr_vacancies.district_id = district.id
left join hr_schedules schedule on hr_vacancies.schedule_id = schedule.id
left join hr_experience experience on hr_vacancies.experience_id = experience.id
left join storing_files on hr_vacancies.files_id = storing_files.id

inner join (select vacancy_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_vacancicategories as categories
    inner join hr_category on categories.category_id = hr_category.id
    group by categories.vacancy_id 
) categories on hr_vacancies.id = categories.vacancy_id

left join (
    select vacancy_id, array_to_json(array_agg(row_to_json(hr_languages))) as langs
    from hr_vacancilanguage as languages
    inner join hr_languages on languages.language_id = hr_languages.id
    group by languages.vacancy_id 
) languages on hr_vacancies.id = languages.vacancy_id

where hr_vacancies.id=%s limit 1
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)
    return rows

def _count_list_vacancies(filter_query, category_filter):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt
from hr_vacancies
inner join user_users users on hr_vacancies.user_id = users.id
inner join company_companies company on hr_vacancies.company_id = company.id
inner join hr_statuses status on hr_vacancies.status_id = status.id
inner join (select vacancy_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_vacancicategories as categories
    inner join hr_category on categories.category_id = hr_category.id{category_filter}
    group by categories.vacancy_id 
) categories on hr_vacancies.id = categories.vacancy_id{filter_query}
""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _format_vacancy_list(data):

    categories = data['cats']
    cat_items = []

    for category in categories:

        cat_items.append(OrderedDict([
            ('id', category['id']),
            ('slug', category['slug']),
            ('name', category['name']),
            ('is_active', category['is_active'])
        ]))

    items = OrderedDict([
        ('id', data['vacancy_id']),
        ('position_name', data['position_name']),
        ('salary', json.loads(data['salary'])),
        ('status', OrderedDict([
            ('id', data['status_id']),
            ('alias', data['status_alias']),
            ('name', data['status_name'])
        ])),
        ('updated_dt', data['updated_dt']),
        ('created_dt', data['created_dt']),
        ('company', OrderedDict([
            ('id', data['company_id']),
            ('name', data['company_name']),
            ('phone_number', data['phone_number'])
        ])),
        ('user', OrderedDict([
            ('id', data['user_id']),
            ('first_name', data['first_name'])
        ])),
        ('category', cat_items)
    ])

    return items

def _format_vacancy(data):

    categories = data['cats']
    cat_items = []
    if categories:
        cat_items = []

        for category in categories:
            cat_items.append(OrderedDict([
                ('id', category['id']),
                ('slug', category['slug']),
                ('name', category['name']),
                ('is_active', category['is_active'])
            ]))


    langs = data['langs']
    lang_items = []
    if langs:
        for lang_item in langs:
            lang_items.append(OrderedDict([
                ('id', lang_item['id']),
                ('alias', lang_item['alias']),
                ('name', lang_item['name']['ru']),
            ]))


    if data['file_path']:
        files = OrderedDict([
            ('id', data['schedule_id']),
            ('file_path', MEDIA_URL+data['file_path']),
            ('file_type', data['file_type'])
        ])
    else:
        files = None

    gender = []
    if data['gender']:

        if data['gender'] == 3:
            gender = ['male', 'female']
        elif data['gender'] == 2:
            gender = ['female']
        elif data['gender'] == 1:
            gender = ['male']
    schedule = None
    if data['schedule_id']:
        schedule = OrderedDict([
            ('id', data['schedule_id']),
            ('name', data['schedule_name'])
        ])

    experience = None
    if data['experience_id']:
        experience = OrderedDict([
            ('id', data['experience_id']),
            ('name', data['experience_name'])
        ])


    region = None
    if data['region_id']:
        region = OrderedDict([
            ('id', data['region_id']),
            ('name', data['region_name'])
        ])

    district = None
    if data['district_id']:
        district = OrderedDict([
            ('id', data['district_id']),
            ('name', data['district_name'])
        ])

    if data['schedule_id']:
        schedule = OrderedDict([
            ('id', data['schedule_id']),
            ('name', data['schedule_name'])
        ])

    items = OrderedDict([
        ('id', data['vacancy_id']),
        ('position_name', data['position_name']),
        ('files', files),
        ('salary', json.loads(data['salary'])),
        ('schedule', schedule),
        ('age', json.loads(data['hr_age'])),
        ('experience', experience),
        ('impressions', data['views_count']),
        ('gender', gender),
        ('languages', lang_items),
        ('region', region),
        ('district', district),
        ('status', OrderedDict([
            ('id', data['status_id']),
            ('alias', data['status_alias']),
            ('name', data['status_name'])
        ])),
        ('updated_dt', data['updated_dt']),
        ('created_dt', data['created_dt']),

    ])

    return OrderedDict([
        ('vacancy', items),
        ('company', OrderedDict([
            ('id', data['company_id']),
            ('name', data['company_name']),
            ('phone_number', data['phone_number'])
        ])),
        ('user', OrderedDict([
            ('id', data['user_id']),
            ('first_name', data['first_name'])
        ])),
        ('category', cat_items)
    ])

