from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from . import services
import json
from .globals import Texts


def go_message(context, user_id, message, reply_markup):
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                             disable_web_page_preview=True)


def edit_message(context, chat_id, message_id, message, reply_markup):
    try:
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message, reply_markup=reply_markup,
                                  parse_mode='HTML')
    except Exception as e:
        print('ERROR edit message: ', str(e))


def delete_message_user(context, chat_id, message_id):
    context.bot.delete_message(chat_id, message_id)


def draftDistrictAndRegion(district_id, lang):
    region = services.getDistrictAndRegion(district_id)
    if lang == 1:
        result = region['region_name_uz'] + ", " + region['name_uz']
    else:
        result = region['region_name_ru'] + ", " + region['name_ru']
    return result


def draftLanguages(ids):
    languages = services.getLanguagesByIds(str(ids).strip('[]'))
    result = ""
    for language in languages:
        temp = json.loads(language['name'])
        result += "     " + temp['ru']
    return result


def draftContacts(contacts):
    result = ""
    for contact in contacts:
        result += contact + ","
    return result


def draftCategories(ids, lang):
    categories = services.getCategoriesByIds(str(ids).strip('[]'))
    result = ""
    for category in categories:
        temp = json.loads(category['name'])
        if lang == 1:
            result += "     🔸" + temp['uz'] + "\n"
        else:
            result += "     🔸" + temp['ru'] + "\n"

    return result[0:-1]


def draftResume(context, user_id, lang, user_model):
    full_name = user_model['full_name']
    phone_number = user_model['phone_number']
    cats = draftCategories(context.user_data.get('cats', []), lang)
    salary_type = context.user_data.get('salary_type', False)
    if salary_type == "yes":
        salary = "{} - {}".format(context.user_data.get("salary", False)['from'], context.user_data.get("salary", False)['to'])
    else:
        if lang == 1:
            salary = "Kelishilgan"
        else:
            salary = "Договорная"
    langs = draftLanguages(context.user_data.get('langs', False))
    age = user_model['age']

    if user_model['gender'] == 'yes':
        gender = Texts['BTN_SEND_MALE'][lang]
    elif user_model['gender'] == 'no':
        gender = Texts['BTN_SEND_FEMALE'][lang]
    else:
        gender = ""
    about = user_model['about']
    skills = user_model['skills']
    district = draftDistrictAndRegion(user_model['district'], lang)

    if lang == 1:
        position = json.loads(services.getPositionById(user_model['position']))['uz']
        schedule = json.loads(services.getScheduleById(context.user_data.get('schedule', False)))['uz']
        experience = json.loads(services.getExperienceById(user_model['experience']))['uz']
        resume = "<b>👔 Ish qidiruvchi:</b> {}\n" \
                 "<b>💼 Mutahasisligi:</b> \n{}\n" \
                 "<b>🔳 Lavozimi:</b> {}\n" \
                 "<b>💵 Ish haqi:</b> {}\n" \
                 "<b>🕔 Ish grafigi:</b> {}\n" \
                 "<b>🌏 Biladigon tillari:</b> {}\n" \
                 "<b>⚡ Yoshi:</b> {}\n" \
                 "<b>🎖 Ish tajribasi:</b> {}\n" \
                 "<b>🚹🚺 Jinsi:</b> {}\n" \
                 "<b>📃 Ozi haqida:</b> {}\n" \
                 "<b>💼 Asosiy ko'nikmalari:</b> {}\n" \
                 "<b>📞 Telefon raqami:</b> {}\n" \
                 "<b>📍 Yashash joyi:</b> {}" \
            .format(
                full_name, cats, position, salary, schedule, langs, age,
                experience, gender, about, skills, phone_number, district
        )
        buttons = [
            [
                InlineKeyboardButton(text="✅ Narsh qilish", callback_data="resume_publish_yes"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data="resume_publish_no"),
            ]
        ]

    else:
        position = user_model['position']
        schedule = json.loads(services.getScheduleById(context.user_data.get('schedule', False)))['ru']
        experience = json.loads(services.getExperienceById(user_model['experience']))['ru']
        resume =    "<b>👔 Соискатель:</b> {}\n" \
                    "<b>💼 Специализация:</b> \n{}\n" \
                    "<b>🔳 Должность:</b> {}\n" \
                    "<b>💵 Зарплата:</b> {}\n" \
                    "<b>🕔 График работы:</b> {}\n" \
                    "<b>🌏 Знание языков:</b> {}\n" \
                    "<b>⚡ Возраст:</b> {}\n" \
                    "<b>🎖 Опыт работы:</b> {}\n" \
                    "<b>🚹🚺 Пол:</b> {}\n" \
                    "<b>📃 О себе:</b> {}\n" \
                    "<b>💼 Ключевые навыки:</b> {}\n" \
                    "<b>📞 Контактный номер:</b> {}\n" \
                    "<b>📍 Место проживание:</b> {}" \
                    .format(
                        full_name, cats, position, salary, schedule, langs, age,
                        experience, gender, about, skills, phone_number, district
                    )
        buttons = [
            [
                InlineKeyboardButton(text="✅ Публиковать", callback_data="resume_publish_yes"),
                InlineKeyboardButton(text="❌ Непубликовать", callback_data="resume_publish_no"),
            ]
        ]

    go_message(context, user_id, resume, InlineKeyboardMarkup(buttons))


def draftVacancy(context, user_id, lang):
    try:
        if not context.user_data['company_id']:
            company_name = context.user_data['company_name']
            phone_number = context.user_data['phone_number']
            district = draftDistrictAndRegion(context.user_data['district'], lang)
        else:
            company = services.getCompanyById(context.user_data['company_id'])
            company_name = company['company_name']
            phone_number = company['phone_number']
            district = draftDistrictAndRegion(company['district_id'], lang)
        salary_type = context.user_data.get('salary_type', False)
        salary = context.user_data.get("salary", False)
        if salary_type == "yes":
            salary = "{} - {}".format(salary['from'], salary['to'])
        else:
            salary = "Договорная"
        langs = draftLanguages(context.user_data.get('langs', False))
        age = "{} - {}".format(context.user_data['age']['from'], context.user_data['age']['to'])
        if context.user_data['gender'] == 1:
            gender = Texts['BTN_SEND_MALE'][lang]
        elif context.user_data['gender'] == 2:
            gender = Texts['BTN_SEND_FEMALE'][lang]
        else:
            if lang == 1:
                gender = Texts['BTN_SEND_MALE'][lang] + " va " + Texts['BTN_SEND_FEMALE'][lang]
            else:
                gender = Texts['BTN_SEND_MALE'][lang] + " и " + Texts['BTN_SEND_FEMALE'][lang]

        requirements = context.user_data['requirements']
        category = services.getCategoryById(context.user_data['category_id'])['name_{}'.format(lang)]
        cats = context.user_data['cats']
        if lang == 1:
            position = json.loads(services.getPositionById(context.user_data['position']))['uz']
            schedule = json.loads(services.getScheduleById(context.user_data.get('schedule', False)))['uz']
            experience = json.loads(services.getExperienceById(context.user_data['experience']))['uz']

            resume = "<b>💼 Kompaniya nomi: </b>{}\n" \
                     "<b>🧰 Mutaxassislik: {}\n</b>{}\n" \
                     "<b>❇ Lavozim: </b>{}\n" \
                     "<b>💵 Ish haqqi: </b>{}\n" \
                     "<b>⏰ Ish jadvali: </b>{}\n" \
                     "<b>🌏 Tillar: </b>{}\n" \
                     "<b>⚡ Kandidat yoshi: </b>{}\n" \
                     "<b>🎖 Kandidat ish tajribasi: </b>{}\n" \
                     "<b>👨💼👩💼 Jinsi: </b>{}\n" \
                     "\n{}\n\n" \
                     "<b>📍Ish joyi:</b>\n{}\n\n" \
                     "<b>✅Tasdiqlangan kompaniya</b>\n\n" \
                     "<b>Bog'lanish uchun telefonlar:</b>\n☎ {}\n". \
                format(company_name, category, draftCategories(cats, lang), position, salary, schedule, langs, age, experience,
                       gender, requirements, district, phone_number)
            buttons = [
                [
                    InlineKeyboardButton(text="✅ Narsh qilish", callback_data="vacancy_publish_yes"),
                    InlineKeyboardButton(text="❌ Rad etish", callback_data="vacancy_publish_no"),
                ]
            ]
        else:
            position = json.loads(services.getPositionById(context.user_data['position']))['ru']
            schedule = json.loads(services.getScheduleById(context.user_data.get('schedule', False)))['ru']
            experience = json.loads(services.getExperienceById(context.user_data['experience']))['ru']

            resume = "<b>💼 Название компании: </b>{}\n" \
                     "<b>🧰 Специализация: {}</b>\n{}\n" \
                     "<b>❇ Должность: </b>{}\n" \
                     "<b>💵 Зарплата: </b>{}\n" \
                     "<b>⏰ График работы: </b>{}\n" \
                     "<b>🌏 Знание языков: </b>{}\n" \
                     "<b>⚡ Возраст: </b>{}\n" \
                     "<b>🎖Опыт работы: </b>{}\n" \
                     "<b>👨💼👩💼 Пол: </b>{}\n" \
                     "\n{}\n\n" \
                     "<b>📍Место работы</b>\n{}\n\n" \
                     "<b>✅Верифицированная компания</b>\n\n" \
                     "<b>Номер телефона для связи</b>\n☎ {}\n". \
                format(company_name, category, draftCategories(cats, lang), position, salary, schedule, langs, age, experience,
                       gender, requirements, district, phone_number)
            buttons = [
                [
                    InlineKeyboardButton(text="✅ Публиковать", callback_data="vacancy_publish_yes"),
                    InlineKeyboardButton(text="❌ Непубликовать", callback_data="vacancy_publish_no"),
                ]
            ]
        go_message(context, user_id, resume, InlineKeyboardMarkup(buttons))
    except Exception as e:
        print("Error Vacancy:", e)


def sendResume(context, user_id, resume, lang, message_id=None):
    s = json.loads(resume['salary'])
    if s['from'] >= 0 and s['to'] > 0:
        salary = str(s['from']) + "-" + str(s['to'])
    else:
        if lang == 1:
            salary = "Kelishilgan"
        else:
            salary = "Договорная"
    if lang == 1:
        schedule = json.loads(services.getScheduleById(resume['schedule_id']))['uz']
        experience = json.loads(services.getExperienceById(resume['experience_id']))['uz']
    else:
        schedule = json.loads(services.getScheduleById(resume['schedule_id']))['ru']
        experience = json.loads(services.getExperienceById(resume['experience_id']))['ru']
    languages = draftLanguages(json.loads(resume['languages'])['languages'])
    if resume['gender'] == 1:
        gender = Texts['BTN_SEND_MALE'][lang]
    else:
        gender = Texts['BTN_SEND_FEMALE'][lang]
    location = draftDistrictAndRegion(resume['district_id'], lang)
    cats = services.getResumeCategories(resume['id'])
    contacts = services.getUserContact(resume['user_id'])
    if lang == 1:
        text = "<b>⏱ Yaratilgan sana:</b> {}\n" \
               "<b>👔 Ish qidiruvchi:</b>\n" \
               "<b>💼 Mutahasisligi:</b> \n{}\n" \
               "<b>🔳 Lavozimi:</b> {}\n" \
               "<b>💵 Ish haqi:</b> {}\n" \
               "<b>🕔 Ish grafigi:</b> {}\n" \
               "<b>🌏 Biladigon tillari:</b> {}\n" \
               "<b>⚡ Yoshi:</b> {}\n" \
               "<b>🎖 Ish tajribasi:</b> {}\n" \
               "<b>🚹🚺 Jinsi:</b> {}\n" \
               "<b>📃 Ozi haqida:</b> {}\n" \
               "<b>💼 Asosiy ko'nikmalari:</b> {}\n" \
               "<b>📞 Telefon raqami:</b> {}\n" \
               "<b>📍 Yashash joyi:</b> {}" \
               .format(
                   resume['created_dt'], draftCategories(cats, lang),
                   resume['postion'], salary, schedule, languages, resume['age'], experience, gender, resume['about'],
                   resume['skills'], draftContacts(contacts), location
               )

    else:
        text = "<b>⏱ Дата создания: </b>{}\n" \
               "<b>👔 Соискатель:</b>\n" \
               "<b>💼 Специализация:</b> \n{}\n" \
               "<b>🔳 Должность:</b> {}\n" \
               "<b>💵 Зарплата:</b> {}\n" \
               "<b>🕔 График работы:</b> {}\n" \
               "<b>🌏 Знание языков:</b> {}\n" \
               "<b>⚡ Возраст:</b> {}\n" \
               "<b>🎖 Опыт работы:</b> {}\n" \
               "<b>🚹🚺 Пол:</b> {}\n" \
               "<b>📃 О себе:</b> {}\n" \
               "<b>💼 Ключевые навыки:</b> {}\n" \
               "<b>📞 Контактный номер:</b> {}\n" \
               "<b>📍 Место проживание:</b> {}" \
               .format(
                   resume['created_dt'], draftCategories(cats, lang),
                   resume['postion'], salary, schedule, languages, resume['age'], experience, gender, resume['about'],
                   resume['skills'], draftContacts(contacts), location
               )

    if resume['status_id'] == 1:
        status_btn = InlineKeyboardButton(text=Texts['BTN_DEACTIVATE'][lang], callback_data="resume_deactivate_{}".format(resume['id']))
    else:
        status_btn = InlineKeyboardButton(text=Texts['BTN_ACTIVATE'][lang],
                                          callback_data="resume_activate_{}".format(resume['id']))

    buttons = [
        [
            InlineKeyboardButton(text=Texts['BTN_EDIT'][lang], callback_data="resume_edit_{}".format(resume['id'])),
            status_btn,
        ],
        [
            InlineKeyboardButton(text=Texts['BTN_DELETE'][lang], callback_data="resume_delete_{}".format(resume['id'])),
        ]
    ]
    if message_id:
        edit_message(context, user_id, message_id, text, InlineKeyboardMarkup(buttons))
    else:
        go_message(context, user_id, text, InlineKeyboardMarkup(buttons))


def sendVacancy(context, user_id, vacancy, lang, message_id=None):
    s = json.loads(vacancy['salary'])
    if s['from'] >= 0 and s['to'] > 0:
        salary = str(s['from']) + "-" + str(s['to'])
    else:
        salary = "Договорная"
    if lang == 1:
        schedule = json.loads(services.getScheduleById(vacancy['schedule_id']))['uz']
        experience = json.loads(services.getExperienceById(vacancy['experience_id']))['uz']
        position = json.loads(services.getPositionById(vacancy['position_id']))['uz']
    else:
        schedule = json.loads(services.getScheduleById(vacancy['schedule_id']))['ru']
        experience = json.loads(services.getExperienceById(vacancy['experience_id']))['ru']
        position = json.loads(services.getPositionById(vacancy['position_id']))['ru']
    languages = draftLanguages(json.loads(vacancy['languages'])['languages'])
    if vacancy['gender'] == 1:
        gender = Texts['BTN_SEND_MALE'][lang]
    elif vacancy['gender'] == 2:
        gender = Texts['BTN_SEND_FEMALE'][lang]
    else:
        gender = Texts['BTN_SEND_MALE'][lang] + ", " + Texts['BTN_SEND_FEMALE'][lang]
    location = draftDistrictAndRegion(vacancy['district_id'], lang)
    age = str(json.loads(vacancy['age'])['from']) + " - " + str(json.loads(vacancy['age'])['to'])
    company_name = services.getCompanyById(vacancy['company_id'])['company_name']
    cats = json.loads(vacancy['subcats'])['cats']
    if lang == 1:
        text = "<b>💼 Kompaniya nomi: </b>{}\n" \
                 "<b>🧰 Mutaxassislik: </b>\n{}\n" \
                 "<b>❇ Lavozimi: </b>{}\n" \
                 "<b>💵 Ish haqi: </b>{}\n" \
                 "<b>⏰ Ish grafigi: </b>{}\n" \
                 "<b>🌏 Tillar: </b>{}\n" \
                 "<b>⚡ Kandidant Yoshi: </b>{}\n" \
                 "<b>🎖Ish tajribasi: </b>{}\n" \
                 "<b>👨💼👩💼 Kandidant Jinsi: </b>{}\n" \
                 "\n{}\n\n" \
                 "<b>📍Ish joyi</b>\n{}\n\n" \
                 "<b>✅Tasdiqlangan kompaniya</b>\n\n" \
                 "<b>Bog'lanish uchun telefon raqam</b>\n☎ {}\n". \
            format(company_name, draftCategories(cats, lang), position, salary, schedule, languages, age, experience,
                   gender, vacancy['requirements'], location, json.loads(vacancy['contacts'])['mobile'])
    else:
        text = "<b>💼 Название компании: </b>{}\n" \
               "<b>🧰 Специализация: </b>\n{}\n" \
               "<b>❇ Должность: </b>{}\n" \
               "<b>💵 Зарплата: </b>{}\n" \
               "<b>⏰ График работы: </b>{}\n" \
               "<b>🌏 Знание языков: </b>{}\n" \
               "<b>⚡ Возраст: </b>{}\n" \
               "<b>🎖Опыт работы: </b>{}\n" \
               "<b>👨💼👩💼 Пол: </b>{}\n" \
               "\n{}\n\n" \
               "<b>📍Место работы</b>\n{}\n\n" \
               "<b>✅Верифицированная компания</b>\n\n" \
               "<b>Номер телефона для связи</b>\n☎ {}\n". \
            format(company_name, draftCategories(cats, lang), position, salary, schedule, languages, age, experience,
                   gender, vacancy['requirements'], location, json.loads(vacancy['contacts'])['mobile'])

    if vacancy['status_id'] == 1:
        status_btn = InlineKeyboardButton(text=Texts['BTN_DEACTIVATE'][lang], callback_data="vacancy_deactivate_{}".format(vacancy['id']))
    else:
        status_btn = InlineKeyboardButton(text=Texts['BTN_ACTIVATE'][lang],
                                          callback_data="vacancy_activate_{}".format(vacancy['id']))

    buttons = [
        [
            InlineKeyboardButton(text=Texts['BTN_EDIT'][lang], callback_data="vacancy_edit_{}".format(vacancy['id'])),
            status_btn,
        ],
        [
            InlineKeyboardButton(text=Texts['BTN_DELETE'][lang], callback_data="vacancy_delete_{}".format(vacancy['id'])),
        ]
    ]
    if message_id:
        edit_message(context, user_id, message_id, text, InlineKeyboardMarkup(buttons))
    else:
        go_message(context, user_id, text, InlineKeyboardMarkup(buttons))


def sendSearchResume(context, user_id, resume, lang, message_id=None):
    s = json.loads(resume['salary'])
    if s['from'] >= 0 and s['to'] > 0:
        salary = str(s['from']) + "-" + str(s['to'])
    else:
        if lang == 1:
            salary = "Kelishilgan"
        else:
            salary = "Договорная"
    if lang == 1:
        schedule = json.loads(services.getScheduleById(resume['schedule_id']))['uz']
        experience = json.loads(services.getExperienceById(resume['experience_id']))['uz']
    else:
        schedule = json.loads(services.getScheduleById(resume['schedule_id']))['ru']
        experience = json.loads(services.getExperienceById(resume['experience_id']))['ru']
    languages = draftLanguages(json.loads(resume['languages'])['languages'])
    if resume['gender'] == 1:
        gender = Texts['BTN_SEND_MALE'][lang]
    else:
        gender = Texts['BTN_SEND_FEMALE'][lang]
    location = draftDistrictAndRegion(resume['district_id'], lang)
    cats = services.getResumeCategories(resume['id'])
    contacts = services.getUserContact(resume['user_id'])
    if lang == 1:
        text = "<b>⏱ Yaratilgan sana:</b> {}\n" \
               "<b>👔 Ish qidiruvchi:</b>\n" \
               "<b>💼 Mutahasisligi:</b> \n{}\n" \
               "<b>🔳 Lavozimi:</b> {}\n" \
               "<b>💵 Ish haqi:</b> {}\n" \
               "<b>🕔 Ish grafigi:</b> {}\n" \
               "<b>🌏 Biladigon tillari:</b> {}\n" \
               "<b>⚡ Yoshi:</b> {}\n" \
               "<b>🎖 Ish tajribasi:</b> {}\n" \
               "<b>🚹🚺 Jinsi:</b> {}\n" \
               "<b>📃 Ozi haqida:</b> {}\n" \
               "<b>💼 Asosiy ko'nikmalari:</b> {}\n" \
               "<b>📞 Telefon raqami:</b> {}\n" \
               "<b>📍 Yashash joyi:</b> {}" \
               .format(
                   resume['created_dt'], draftCategories(cats, lang),
                   resume['postion'], salary, schedule, languages, resume['age'], experience, gender, resume['about'],
                   resume['skills'], draftContacts(contacts), location
               )

    else:
        text = "<b>⏱ Дата создания: </b>{}\n" \
               "<b>👔 Соискатель:</b>\n" \
               "<b>💼 Специализация:</b> \n{}\n" \
               "<b>🔳 Должность:</b> {}\n" \
               "<b>💵 Зарплата:</b> {}\n" \
               "<b>🕔 График работы:</b> {}\n" \
               "<b>🌏 Знание языков:</b> {}\n" \
               "<b>⚡ Возраст:</b> {}\n" \
               "<b>🎖 Опыт работы:</b> {}\n" \
               "<b>🚹🚺 Пол:</b> {}\n" \
               "<b>📃 О себе:</b> {}\n" \
               "<b>💼 Ключевые навыки:</b> {}\n" \
               "<b>📞 Контактный номер:</b> {}\n" \
               "<b>📍 Место проживание:</b> {}" \
               .format(
                   resume['created_dt'], draftCategories(cats, lang),
                   resume['postion'], salary, schedule, languages, resume['age'], experience, gender, resume['about'],
                   resume['skills'], draftContacts(contacts), location
               )

    buttons = [
        [
            InlineKeyboardButton(text=Texts['BTN_SUBSCRIBE'][lang], callback_data="filterR_subscribe_{}".format(resume['id'])),
        ]
    ]
    if message_id:
        edit_message(context, user_id, message_id, text, InlineKeyboardMarkup(buttons))
    else:
        go_message(context, user_id, text, InlineKeyboardMarkup(buttons))


def sendSearchVacancy(context, user_id, vacancy, lang, message_id=None):
    s = json.loads(vacancy['salary'])
    if s['from'] >= 0 and s['to'] > 0:
        salary = str(s['from']) + "-" + str(s['to'])
    else:
        salary = "Договорная"
    if lang == 1:
        schedule = json.loads(services.getScheduleById(vacancy['schedule_id']))['uz']
        experience = json.loads(services.getExperienceById(vacancy['experience_id']))['uz']
        position = json.loads(services.getPositionById(vacancy['position_id']))['uz']
    else:
        schedule = json.loads(services.getScheduleById(vacancy['schedule_id']))['ru']
        experience = json.loads(services.getExperienceById(vacancy['experience_id']))['ru']
        position = json.loads(services.getPositionById(vacancy['position_id']))['ru']
    languages = draftLanguages(json.loads(vacancy['languages'])['languages'])
    if vacancy['gender'] == 1:
        gender = Texts['BTN_SEND_MALE'][lang]
    elif vacancy['gender'] == 2:
        gender = Texts['BTN_SEND_FEMALE'][lang]
    else:
        gender = Texts['BTN_SEND_MALE'][lang] + ", " + Texts['BTN_SEND_FEMALE'][lang]
    location = draftDistrictAndRegion(vacancy['district_id'], lang)
    age = str(json.loads(vacancy['age'])['from']) + " - " + str(json.loads(vacancy['age'])['to'])
    company_name = services.getCompanyById(vacancy['company_id'])['company_name']
    cats = json.loads(vacancy['subcats'])['cats']
    if lang == 1:
        text = "<b>💼 Kompaniya nomi: </b>{}\n" \
               "<b>🧰 Mutaxassislik: </b>\n{}\n" \
               "<b>❇ Lavozimi: </b>{}\n" \
               "<b>💵 Ish haqi: </b>{}\n" \
               "<b>⏰ Ish grafigi: </b>{}\n" \
               "<b>🌏 Tillar: </b>{}\n" \
               "<b>⚡ Kandidant Yoshi: </b>{}\n" \
               "<b>🎖Ish tajribasi: </b>{}\n" \
               "<b>👨💼👩💼 Kandidant Jinsi: </b>{}\n" \
               "\n{}\n\n" \
               "<b>📍Ish joyi</b>\n{}\n\n" \
               "<b>✅Tasdiqlangan kompaniya</b>\n\n" \
               "<b>Bog'lanish uchun telefon raqam</b>\n☎ {}\n". \
            format(company_name, draftCategories(cats, lang), position, salary, schedule, languages, age, experience,
                   gender, vacancy['requirements'], location, json.loads(vacancy['contacts'])['mobile'])
    else:
        text = "<b>💼 Название компании: </b>{}\n" \
               "<b>🧰 Специализация: </b>\n{}\n" \
               "<b>❇ Должность: </b>{}\n" \
               "<b>💵 Зарплата: </b>{}\n" \
               "<b>⏰ График работы: </b>{}\n" \
               "<b>🌏 Знание языков: </b>{}\n" \
               "<b>⚡ Возраст: </b>{}\n" \
               "<b>🎖Опыт работы: </b>{}\n" \
               "<b>👨💼👩💼 Пол: </b>{}\n" \
               "\n{}\n\n" \
               "<b>📍Место работы</b>\n{}\n\n" \
               "<b>✅Верифицированная компания</b>\n\n" \
               "<b>Номер телефона для связи</b>\n☎ {}\n". \
            format(company_name, draftCategories(cats, lang), position, salary, schedule, languages, age, experience,
                   gender, vacancy['requirements'], location, json.loads(vacancy['contacts'])['mobile'])

    buttons = [
        [
            InlineKeyboardButton(text=Texts['BTN_SUBSCRIBE'][lang],
                                 callback_data="filterV_subscribe_{}".format(vacancy['id'])),
        ]
    ]
    if message_id:
        edit_message(context, user_id, message_id, text, InlineKeyboardMarkup(buttons))
    else:
        go_message(context, user_id, text, InlineKeyboardMarkup(buttons))



