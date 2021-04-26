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
def get_list_resumes(request):
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

    if "user" in request.query_params:
        try:
            user_id = int(request.query_params.get('user', 0))

            filter_query = f" where resume.user_id = %s" % user_id
        except:
            filter_query = ""
    else:
        filter_query = ""

    count_records = _count_list_resumes(filter_query, category_filter)

    rows = _get_all_resumes(page, filter_query, category_filter)
    result = []
    if rows:
        for data in rows:
            result.append(_format_resume_list(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_one_resume(request, id):
    data = _get_one_resume(id)

    result = OrderedDict([
        ('item', _format_resume(data))
    ])
    return result


def _get_all_resumes(page, filter_query, category_filter):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select resume.id as resume_id,  users.id as user_id, users.first_name as user_firstname, position_name, salary, created_dt , updated_dt, categories.cats, 
resume.firstname, resume.lastname, resume.middlename, resume.phone_number, resume.birthday, 
users.id as user_id, users.first_name, status.alias as status_alias, status."name"->>'ru' as status_name, resume.status_id
from hr_resume resume
inner join user_users users on resume.user_id = users.id
inner join hr_statuses status on resume.status_id = status.id
inner join (select resume_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_resumecategories as categories
    inner join hr_category on categories.category_id = hr_category.id{category_filter}
    group by categories.resume_id 
) categories on resume.id = categories.resume_id{filter_query}
ORDER BY updated_dt desc
limit %s OFFSET %s
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows



def _get_one_resume(id):

    extra_sql = f"""select resume.id as resume_id, users.id as user_id, users.first_name as user_firstname, position_name, categories.cats, resume.salary as resume_salary, 
resume.views_count as views_count, resume.contact_count as contact_count, resume.gender as gender, 
resume.firstname as firstname, resume.lastname as lastname, resume.middlename as middlename, resume.birthday as birthday, 
resume.phone_number as phone_number, resume.created_dt, resume.updated_dt,
schedule.id as schedule_id, schedule."name"->>'ru' as schedule_name, 
storing_files.file_type , storing_files.file_path, experience.id as experience_id, experience."name"->>'ru' as experience_name, 
languages.langs, status.alias as status_alias, status."name"->>'ru' as status_name, resume.status_id,
region.id as region_id, region.name_ru as region_name, district.id as district_id, district.name_ru as district_name
from hr_resume resume
inner join user_users users on resume.user_id = users.id
inner join hr_statuses status on resume.status_id = status.id
inner join (select resume_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_resumecategories as categories
    inner join hr_category on categories.category_id = hr_category.id
    group by categories.resume_id
) categories on resume.id = categories.resume_id
left join geo_region region on resume.region_id = region.id
left join geo_district district on resume.district_id = district.id
left join (
    select resume_id, array_to_json(array_agg(row_to_json(hr_languages))) as langs
    from hr_resumelanguage as languages
    inner join hr_languages on languages.language_id = hr_languages.id
    group by languages.resume_id 
) languages on resume.id = languages.resume_id

left join hr_schedules schedule on resume.schedule_id = schedule.id
left join hr_experience experience on resume.experience_id = experience.id
left join storing_files on resume.files_id = storing_files.id

where resume.id=%s limit 1
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)
    return rows

def _count_list_resumes(filter_query, category_filter):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt
from hr_resume resume
inner join user_users users on resume.user_id = users.id
inner join hr_statuses status on resume.status_id = status.id
inner join (select resume_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_resumecategories as categories
    inner join hr_category on categories.category_id = hr_category.id{category_filter}
    group by categories.resume_id 
) categories on resume.id = categories.resume_id{filter_query}
""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _format_resume_list(data):

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
        ('id', data['resume_id']),
        ('firstname', data['firstname']),
        ('lastname', data['lastname']),
        ('middlename', data['middlename']),
        ('birthday', str(data['birthday'])),
        ('position_name', data['position_name']),
        ('salary', json.loads(data['salary'])),
        ('status', OrderedDict([
            ('id', data['status_id']),
            ('alias', data['status_alias']),
            ('name', data['status_name'])
        ])),
        ('updated_dt', data['updated_dt']),
        ('created_dt', data['created_dt']),
        ('user', OrderedDict([
            ('id', data['user_id']),
            ('first_name', data['user_firstname'])
        ])),
        ('category', cat_items)
    ])

    return items

def _format_resume(data):

    categories = data['cats']

    cat_items = []
    if categories:
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

    if data['gender'] == 2:
        gender = ['female']
    elif data['gender'] == 1:
        gender = ['male']
    else:
        gender = None

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

    items = OrderedDict([
        ('id', data['resume_id']),
        ('firstname', data['firstname']),
        ('lastname', data['lastname']),
        ('middlename', data['middlename']),
        ('phone_number', data['phone_number']),
        ('birthday', str(data['birthday'])),
        ('position_name', data['position_name']),
        ('files', files),
        ('salary', json.loads(data['resume_salary'])),
        ('schedule', schedule),
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
        ('resume', items),
        ('user', OrderedDict([
            ('id', data['user_id']),
            ('first_name', data['user_firstname'])
        ])),
        ('category', cat_items)
    ])

