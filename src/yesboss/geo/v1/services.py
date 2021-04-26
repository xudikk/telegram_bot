# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.utils.translation import to_locale, get_language
from ...base.utils.sqlpaginator import SqlPaginator
from ...base.utils.db import dictfetchall

def get_region_list(request):
    rows = _get_regions(239)
    result = []
    for data in rows:
        result.append(OrderedDict([
            ('id', data['id']),
            ('name', data['name'])
        ]))
    paginator = SqlPaginator(request, page=1, per_page=len(result), count=len(result))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_district_list(request, id=None):
    rows = _get_districts(id)
    result = []
    for data in rows:
        result.append(OrderedDict([
            ('id', data['id']),
            ('region_id', data['region_id']),
            ('name', data['name'])
        ]))
    paginator = SqlPaginator(request, page=1, per_page=len(result), count=len(result))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])


def _get_regions(country_id):
    current_language = to_locale(get_language())
    if current_language == 'uz':
        select_text = 'name_uz as name'
    else:
        select_text = 'name_ru as name'
    extra_sql = """select id, {select_text}
    FROM geo_region
    ORDER BY ordering
    LIMIT 100
        """.format(select_text=select_text)

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)

    return rows

def _get_districts(region_id=None):
    current_language = to_locale(get_language())
    if current_language == 'uz':
        select_text = 'name_uz as name'
    else:
        select_text = 'name_ru as name'
    if region_id:
        extra_sql = """select id, region_id, {select_text}
        FROM geo_district
        WHERE region_id = %s
        ORDER BY ordering
        LIMIT 100
            """.format(select_text=select_text)
        params = [region_id]
    else:
        params = None
        extra_sql = """select id, region_id, {select_text}
                FROM geo_district                
                ORDER BY region_id
                LIMIT 200
                    """.format(select_text=select_text)

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, params)
        rows = dictfetchall(cursor)

    return rows
