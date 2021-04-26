# -*- coding: utf-8 -*-
import json
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings
from ...base.utils.sqlpaginator import SqlPaginator
from ...base.utils.db import dictfetchone, dictfetchall

PER_PAGE = settings.PAGINATE_BY

def get_list_category(request, parent=None):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    if "main" in request.query_params:
        try:
            filter_query = "where parent_id is null"
        except:
            filter_query = ""
    else:
        filter_query = ""
    count_records = _count_list_category(filter_query)

    rows = _get_all_category(page, filter_query)
    nodes = {}
    for data in rows:
        nodes[data['id']] = _format_one(data)

    result = []
    if parent:
        for data in rows:
            result.append(nodes[data['id']])

    else:
        for data in rows:
            id = data['id']
            parent_id = data['parent_id']
            node = nodes[id]
            if parent_id is None:
                result.append(node)
            else:
                if parent_id in nodes:
                    parent = nodes[parent_id]
                    children = parent['children']
                    children.append(node)
                else:
                    result.append(node)
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_list_positions(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    if "category" in request.query_params:
        try:
            category = int(request.query_params.get('category', 1))
            filter_query = "where category_id = %s" % category
        except:
            filter_query = ""
    else:
        filter_query = ""
    count_records = _count_list_positions(filter_query)

    rows = _get_all_position(page, filter_query)
    result = []

    for data in rows:
        result.append(_format_position(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_list_schedule(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1


    count_records = _count_list_schedule()

    rows = _get_all_schedule()
    result = []

    for data in rows:
        result.append(_format_schedule(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_list_experiences(request):
    rows = _get_all_experiences()
    result = []

    for data in rows:
        result.append(_format_experiences(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=len(rows))
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

def get_list_languages(request):
    rows = _get_all_languages(1)
    result = []

    for data in rows:
        result.append(_format_select_languages(data))
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=len(rows))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_one_experiences(request, id):
    data = _get_one_experiences(id)

    result = OrderedDict([
        ('item', _format_experiences(data))
    ])
    return result


def get_one_schedule(request, id):
    data = _get_one_schedule(id)

    result = OrderedDict([
        ('item', _format_schedule(data))
    ])
    return result

def get_one_position(request, id):
    data = _get_one_position(id)

    result = OrderedDict([
        ('item', _format_position(data))
    ])
    return result

def get_one_category(request, id):
    category = _format_one(_get_one_category(id))
    if category:
        child_items = []
        childs = _get_category_childs(id)
        for data in childs:
            child_items.append(_format_one(data))
        category['children'] = child_items

    result = OrderedDict([
        ('item', category)
    ])
    return result


def _get_all_category(page, filter_query):

    extra_sql = f"""select id, name, hr_category.slug, parent_id as parent_id, sort_order,
    is_main, is_active
    from
    (
        SELECT  node.slug 
        FROM hr_category AS node,
            hr_category AS parent
        WHERE node.lft BETWEEN parent.lft AND parent.rght
        GROUP BY node.slug
    ) t
    inner join hr_category on t.slug = hr_category.slug
    {filter_query}
    ORDER BY tree_id, lft
    limit 500
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)
    return rows

def _get_all_position(page, filter_query):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select hr_positions.id as position_id, hr_positions.name as position_name, hr_positions.slug as position_slug, 
    category_id,hr_positions.is_active
    from hr_positions
    inner join hr_category on hr_positions.category_id = hr_category.id
    {filter_query}
    ORDER BY position_slug asc
    limit %s OFFSET %s
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows


def _get_one_position(id):
    extra_sql = f"""select hr_positions.id as position_id, hr_positions.name as position_name, hr_positions.slug as position_slug, 
        category_id, hr_positions.is_active
        from hr_positions
        inner join hr_category on hr_positions.category_id = hr_category.id
        where hr_positions.id = %s
                """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)
    return rows


def _get_one_category(id):

    extra_sql = """select id, name, slug, parent_id as parent_id, sort_order,
    is_main, is_active
    from hr_category
    where id=%s
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)
    return rows

def _get_category_childs(parent_id):
    extra_sql = """select id, name, slug, parent_id as parent_id, sort_order,
    is_main, is_active
        FROM hr_category
        WHERE parent_id=%s and is_active is true
        ORDER BY lft
        LIMIT 60
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [parent_id])
        rows = dictfetchall(cursor)
    return rows


def _get_all_schedule():

    extra_sql = f"""select id, data, name, alias, is_active
    from hr_schedules
    ORDER BY name asc
    limit 50
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)
    return rows

def _get_all_experiences():

    extra_sql = f"""select id, name, alias, sort_order
    from hr_experience
    ORDER BY sort_order asc
    limit 50
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)
    return rows

def _get_all_status(page):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select * from company_statuses order by id asc limit %s OFFSET %s """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows

def _get_all_languages(page):
    offset = (page - 1) * PER_PAGE
    extra_sql = f"""select * from hr_languages order by sort_order asc limit %s OFFSET %s """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        rows = dictfetchall(cursor)
    return rows

def _get_one_experiences(id):

    extra_sql = f"""select id, name, alias, sort_order
    from hr_experience where id = %s
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)
    return rows

def _get_one_schedule(id):
    extra_sql = f"""select id, data, name, alias, is_active
        from hr_schedules
        where hr_schedules.id = %s
                """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        rows = dictfetchone(cursor)
    return rows

def _count_list_schedule():
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt from hr_schedules""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _count_list_category(filter_query):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt from hr_category {filter_query}""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _count_list_positions(filter_query):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt from hr_positions {filter_query}""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result

def _format_one(data):
    items = OrderedDict([
            ('id', data['id']),
            ('slug', data['slug']),
            ('parent_id', data['parent_id']),
            ('name', json.loads(data['name'])),
            ('is_active', data['is_active']),
            ('is_main', data['is_main']),
            ('sort_order', data['sort_order']),
            ('children', []),
        ])
    return items

def _format_position(data):
    items = OrderedDict([
            ('id', data['position_id']),
            ('slug', data['position_slug']),
            ('category_id', data['category_id']),
            ('name', json.loads(data['position_name'])),
            ('is_active', data['is_active'])
        ])
    return items


def _format_schedule(data):
    items = OrderedDict([
            ('id', data['id']),
            ('slug', data['alias']),
            ('name', json.loads(data['name'])),
            ('is_active', data['is_active'])
        ])
    return items

def _format_experiences(data):
    items = OrderedDict([
            ('id', data['id']),
            ('alias', data['alias']),
            ('name', json.loads(data['name']))
        ])
    return items

def _format_status(data):
    items = OrderedDict([
            ('id', data['id']),
            ('alias', data['alias']),
            ('name', json.loads(data['name'])),
        ])
    return items

def _format_select_languages(data):
    items = OrderedDict([
            ('id', data['id']),
            ('alias', data['alias']),
            ('name', json.loads(data['name'])),
        ])
    return items