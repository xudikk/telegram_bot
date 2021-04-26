# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.contrib.sites.shortcuts import get_current_site
from ...base.utils.sqlpaginator import SqlPaginator
from ...base.utils.db import dictfetchone, dictfetchall

PER_PAGE = 50

def get_list_users(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    count_records = _count_list_users()

    users = _get_user_sql(page)
    items = []
    if users:
        for pr in users:
            items.append(_format_list(pr))

    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', pagging)
    ])

def get_one_users(request, id):
    user = _get_one_user_sql(id)

    result = OrderedDict([
        ('item', _format_one(user))
    ])
    return result

def _get_user_sql(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select user_users.*,  
user_types.id as types_id, user_types."name" ->>'ru' as types_name, user_statuses.id as status_id, user_statuses."name" ->>'ru' as status_name
from user_users
left join user_types on user_users.types_id=user_types.id
left join user_statuses on user_users.status_id=user_statuses.id
order by date_joined desc
            limit %s
            OFFSET %s""", [PER_PAGE, offset])
        rows = dictfetchall(cursor)
        return rows

def _get_one_user_sql(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select user_users.*,  
user_types.id as types_id, user_types."name" ->>'ru' as types_name, user_statuses.id as status_id, user_statuses."name" ->>'ru' as status_name
from user_users
left join user_types on user_users.types_id=user_types.id
left join user_statuses on user_users.status_id=user_statuses.id
where user_users.id=%s
""", [id])
        row = dictfetchone(cursor)
        return row

def _count_list_users():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select count(1) as cnt from user_users""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _format_list(data):
    if data['status_id']:
        status = OrderedDict([
            ('id', int(data['status_id'])),
            ('name', data['status_name'])
        ])

    else:
        status = None

    if data['types_id']:
        types = OrderedDict([
            ('id', int(data['types_id'])),
            ('name', data['types_name'])
        ])

    else:
        types = None

    items = OrderedDict([
        ('id', data['id']),
        ('email', data['email']),
        ('phone_number', data['phone_number']),
        ('first_name', data['first_name']),
        ('last_name', data['last_name']),
        ('user_type', types),
        ('status', status),
        ('date_joined', str(data['date_joined']))
    ])
    return items

def _format_one(data):
    if data['status_id']:
        status = OrderedDict([
            ('id', int(data['status_id'])),
            ('name', data['status_name'])
        ])

    else:
        status = None

    if data['types_id']:
        types = OrderedDict([
            ('id', int(data['types_id'])),
            ('name', data['types_name'])
        ])

    else:
        types = None

    items = OrderedDict([
        ('id', data['id']),
        ('email', data['email']),
        ('phone_number', data['phone_number']),
        ('first_name', data['first_name']),
        ('last_name', data['last_name']),
        ('lang', data['lang']),
        ('user_type', types),
        ('status', status),
        ('date_joined', str(data['date_joined']))
    ])
    return items