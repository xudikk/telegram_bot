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


def get_counters():
    count_active_vacancies = _count_vacancies("where hr_vacancies.status_id=2")
    count_not_active_vacancies = _count_vacancies("where hr_vacancies.status_id=1")

    count_active_resumes = _count_resumes("where resume.status_id=2")
    count_not_active_resumes = _count_resumes("where resume.status_id=1")
    count_users = _count_users()
    count_company = _count_company()

    return OrderedDict([
        ('users', count_users),
        ('company', count_company),
        ('vacancy', OrderedDict([
            ('active', count_active_vacancies),
            ('not_active', count_not_active_vacancies),
        ])),
        ('resume', OrderedDict([
            ('active', count_active_resumes),
            ('not_active', count_not_active_resumes),
        ])),
    ])


def get_top_category(request):
    rows = _top_category()
    result = []
    if rows:
        for data in rows:
            result.append(_format_top_category_list(data))

    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=len(result))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])


def _top_category():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select cnt, hr_category.id, hr_category.name->>'ru' as category_name, slug, is_active
from hr_category
inner join (
	select category_id, count(1)as cnt from hr_vacancicategories
	inner join hr_category on hr_vacancicategories.category_id = hr_category.id and hr_category.parent_id is not null
	group by category_id order by cnt desc, category_id  asc
) cats on hr_category.id = cats.category_id
order by cnt desc
limit 5
""")
        rows = dictfetchall(cursor)
        return rows


def _count_vacancies(filter_query):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt
from hr_vacancies
inner join user_users users on hr_vacancies.user_id = users.id
inner join company_companies company on hr_vacancies.company_id = company.id
inner join hr_statuses status on hr_vacancies.status_id = status.id
inner join (select vacancy_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_vacancicategories as categories
    inner join hr_category on categories.category_id = hr_category.id
    group by categories.vacancy_id 
) categories on hr_vacancies.id = categories.vacancy_id {filter_query}
""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result


def _count_resumes(filter_query):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt
from hr_resume resume
inner join user_users users on resume.user_id = users.id
inner join hr_statuses status on resume.status_id = status.id
inner join (select resume_id, array_to_json(array_agg(row_to_json(hr_category))) as cats
    from hr_resumecategories as categories
    inner join hr_category on categories.category_id = hr_category.id
    group by categories.resume_id 
) categories on resume.id = categories.resume_id {filter_query}
""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result


def _count_users():
    with closing(connection.cursor()) as cursor:
        cursor.execute("select count(1) as cnt from user_users")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result


def _count_company():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "select count(1) as cnt from company_companies inner join user_users on company_companies.user_id=user_users.id")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result


def _format_top_category_list(category):
    items = OrderedDict([
        ('count', category['cnt']),
        ('category', OrderedDict([
            ('id', category['id']),
            ('slug', category['slug']),
            ('name', category['category_name']),
            ('is_active', category['is_active'])
        ]))
    ])

    return items
