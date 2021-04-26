# -*- coding: utf-8 -*-
import json
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings
from ...base.utils.sqlpaginator import SqlPaginator
from ...base.utils.db import dictfetchone, dictfetchall

PER_PAGE = settings.PAGINATE_BY

def get_list_company(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    count_records = _count_list_company()

    rows = _get_all_company(page)
    result = []

    for data in rows:
        result.append(_format_company(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_list_status(request):
    rows = _get_all_status(1)
    result = []

    for data in rows:
        result.append(_format_status(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=len(rows))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_one_company(request, id):
    data = _get_one_company(id)
    result = OrderedDict([
        ('item', _format_company(data))
    ])
    return result


def _get_all_company(page):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select company_companies.*, geo_region.name_ru as region_name_ru, geo_region.name_uz as region_name_uz,
geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru, 
users.id as user_id, users.first_name, status.id as status_id, status.alias as status_alias, status."name"->>'ru' as status_name
    from company_companies
    inner join user_users users on company_companies.user_id = users.id
    inner join company_statuses status on company_companies.status_id = status.id
    left join geo_region on company_companies.region_id = geo_region.id
    left join geo_district on company_companies.district_id = geo_district.id
    ORDER BY company_companies.id asc
    limit %s OFFSET %s
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows

def _get_all_status(page):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select * from company_statuses order by id asc limit %s OFFSET %s """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows


def _get_one_company(id):
    extra_sql = f"""select company_companies.*, geo_region.name_ru as region_name_ru, geo_region.name_uz as region_name_uz,
geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru, 
users.id as user_id, users.first_name, status.id as status_id, status.alias as status_alias, status."name"->>'ru' as status_name
    from company_companies
    inner join user_users users on company_companies.user_id = users.id
    inner join company_statuses status on company_companies.status_id = status.id
    left join geo_region on company_companies.region_id = geo_region.id
    left join geo_district on company_companies.district_id = geo_district.id
        where company_companies.id = %s
                """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)

    print('company model')
    print(rows)

    return rows

def _count_list_company():
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt from company_companies""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _format_company(data):
    if data['region_id']:
        region = OrderedDict([
                ('id', data['region_id']),
                ('name_ru', data['region_name_ru']),
                ('name_uz', data['region_name_uz'])
            ])
    else:
        region = None

    if data['region_id']:
        district = OrderedDict([
                ('id', data['district_id']),
                ('name_ru', data['district_name_ru']),
                ('name_uz', data['district_name_uz'])
            ])
    else:
        district = None

    items = OrderedDict([
            ('id', data['id']),
            ('name', data['company_name']),
            ('title', data['title']),
            ('email', data['email']),
            ('description', data['description']),
            ('phone_number', data['phone_number']),
            ('address', data['address']),
            ('region', region),
            ('district', district),
            ('status', OrderedDict([
                ('id', data['status_id']),
                ('alias', data['status_alias']),
                ('name', data['status_name'])
            ])),
            ('user', OrderedDict([
                ('id', data['user_id']),
                ('first_name', data['first_name'])
            ])),
        ])
    return items

def _format_status(data):
    items = OrderedDict([
            ('id', data['id']),
            ('alias', data['alias']),
            ('name', json.loads(data['name'])),
        ])
    return items
