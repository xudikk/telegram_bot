import json
from django.db import transaction

from ..tg.models import Channel
from .employee.employee_service import get_resume_one
from .company.hirer_service import get_vacancies_one
from .employee.employee_trans import Texts as resume_text
from .company.hirer_trans import Texts as hirer_text
from .employee.resume import get_file_path
from .views import MQBot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (messagequeue as mq)
from telegram.utils.request import Request

class TgManager(object):

    def sendResume(self, resume_id):
        with transaction.atomic():
            channel_model = Channel.objects.get(pk=1)
            resume = get_resume_one(resume_id)
            post = self.formatResume(resume)
            self.sendChannel('resume', resume["resume_id"], resume, post, channel_model.resume_channel_id, channel_model.token)

    def sendVacancy(self, vacancy_id):
        with transaction.atomic():
            channel_model = Channel.objects.get(pk=1)
            vacancy = get_vacancies_one(vacancy_id)
            post = self.formatVacancy(vacancy)
            self.sendChannel('vacancy', vacancy["vacancy_id"], vacancy, post, channel_model.vacancy_channel_id, channel_model.token)

    def sendChannel(self, type, id, data, post, channel_id, bot_token):
        q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
        request = Request(con_pool_size=36)
        bot = MQBot(bot_token, request=request, mqueue=q)
        file_type = data['file_type']
        file_path = data['file_path']
        path = get_file_path(file_path)
        if file_type == 1:
            file_type = 'photo'
        else:
            file_type = 'video'

        inline_keyboard = [
            [InlineKeyboardButton('Показать контакт',
                                  callback_data=f'show_{type}_contact_{id}')]
        ]

        if file_type:
            if file_type == 'photo':
                bot.send_photo(channel_id, photo=open(path, 'rb'), caption=post, reply_markup=InlineKeyboardMarkup(inline_keyboard), parse_mode='HTML')
            else:
                bot.send_video(channel_id, video=open(path, 'rb'), caption=post, reply_markup=InlineKeyboardMarkup(inline_keyboard), parse_mode='HTML')
        else:
            bot.send_message(channel_id, post, parse_mode='HTML')

    def formatResume(self, resume):
        try:
            lang = 2
            lang_code = 'ru'
            fio = f"{resume['firstname']} {resume['lastname']} {resume['middlename']}"
            phone_number = resume["phone_number"]
            post = f"💼 {fio}️"
            post = "{}\n{} - {}".format(post, resume_text['POSITION'][lang], resume["position_name"])

            salary_types = json.loads(resume.get('salary'))
            salary_type = salary_types.get('text')
            if salary_type is None:
                salary = resume_text['BTN_SALARY_NO'][lang]
            else:
                salary = salary_types.get('text')
            post = "{}\n{} - {}".format(post, resume_text['SALARY'][lang], salary)

            schedule = json.loads(resume.get('schedule_name'))
            if schedule:
                post = "{}\n{} - {}".format(post, resume_text['SCHEDULE'][lang], schedule[lang_code])

            langs = resume['langs']
            if langs:
                p_langs = ''
                for l_type in langs:
                    name = l_type.get('name')
                    p_langs += name[lang_code] + ", "
                post = "{}\n{} - {}".format(post, resume_text['LANGS'][lang], p_langs.strip(", "))

            post = f"{post}\n{resume_text['AGE'][lang]} - {resume['user_age']}️"

            experience = json.loads(resume.get('experience_name'))
            if experience:
                post = "{}\n{} - {}".format(post, resume_text['EXPERIENCE'][lang], experience[lang_code])

            selected_gender = resume["gender"]
            if selected_gender:
                genders = [
                    {'id': 1, 'name': resume_text['BTN_SEND_MALE'][lang]},
                    {'id': 2, 'name': resume_text['BTN_SEND_FEMALE'][lang]},
                ]
                p_gender = ''
                for gender in genders:
                    if gender['id'] == selected_gender:
                        p_gender = gender["name"]
                        break
                post = "{}\n{} - {}".format(post, resume_text['GENDER'][lang], p_gender)

            region_id = resume['re_id']
            if region_id:
                p_region = resume[f'region_name_{lang}']
                district_id = resume['dis_id']
                if district_id:
                    p_region = "{}, {}".format(p_region, resume[f'district_name_{lang}'])

                post = "{}\n{} - {}".format(post, resume_text['REGION'][lang], p_region)

            # post = "{}\n \n{}\n☎️ {}".format(post, resume_text['PHONE_C'][lang], phone_number)
            return post
        except Exception as e:
            print('view error all:', str(e))

    def formatVacancy(self, vacancy):

        lang = 2
        lang_code = 'ru'
        company_name = vacancy['company_name']
        post = f"💼 {company_name}️"
        post = "{}\n{}-{}".format(post, hirer_text['POSITION'][lang], vacancy.get('position_name', '-'))
        salary_types = json.loads(vacancy.get('salary'))
        salary_type = salary_types.get('text')
        if salary_type == None:
            salary = hirer_text['BTN_SALARY_NO'][lang]
        else:
            salary = salary_types.get('text')
        post = "{}\n{}-{}".format(post, hirer_text['SALARY'][lang], salary)
        schedule = json.loads(vacancy.get('schedule_name'))

        if schedule:
            post = "{}\n{}-{}".format(post, hirer_text['SCHEDULE'][lang], schedule[lang_code])

        # langs = json.loads(vacancy.get('langs'))
        langs = vacancy.get('langs')
        if langs:
            p_langs = ''
            for lang_i in langs:
                name = lang_i['name']['ru']
                p_langs += name + ', '

            post = "{}\n{}-{}".format(post, hirer_text['LANGS'][lang], p_langs)

        age = json.loads(vacancy.get('vacancy_age'))
        post = f"{post}\n{hirer_text['AGE'][lang]}-{age.get('text', '-')}️"

        experience = json.loads(vacancy.get('experience_name'))
        if experience:
            post = "{}\n{}-{}".format(post, hirer_text['EXPERIENCE'][lang], experience[lang_code])
        # langs = vacancy['langs']

        selected_gender = vacancy.get('gender', 0)
        if selected_gender == 3:
            post = "{}\n{}-{}".format(post, hirer_text['GENDER'][lang], hirer_text['BTN_SEND_MALE'][lang] + ", " + hirer_text['BTN_SEND_FEMALE'][lang])

        elif selected_gender == 2:
            post = "{}\n{}-{}".format(post, hirer_text['GENDER'][lang], hirer_text['BTN_SEND_FEMALE'][lang])
        else:
            post = "{}\n{}-{}".format(post, hirer_text['GENDER'][lang],hirer_text['BTN_SEND_MALE'][lang])


        region = vacancy.get(f'region_name_{lang_code}')
        district = vacancy.get(f'district_name_{lang_code}')
        if region and district:
            post = "{}\n{}-{}".format(post, hirer_text['REGION'][lang], region + ", " + district)

        return post

