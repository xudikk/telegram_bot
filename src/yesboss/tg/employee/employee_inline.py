from telegram import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
# from .employee_search import SearchVacancies
from ..user_data import UserData
from . import employee_service as services
from .employee_trans import Texts
from .resume import *
from .employee_service import *
import json


class Employee(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]

    def get_trans(self, txt):
        try:
            result = Texts[txt][self.user_model['lang']].encode('utf-8')
        except Exception:
            result = Texts[txt][self.user_model['lang']]
        return result

    def get_main_buttons(self, btn_back=False, edit=None):
        lang = self.user_model['lang']
        if edit == "back":
            return ReplyKeyboardMarkup([
                [Texts['BTN_SEND_BACK'][lang]],
                [Texts['BTN_ADD_RESUME'][lang], Texts['BTN_FIND_VACANCIES'][lang]],
                [Texts['BTN_REPLY'][lang], Texts['BTN_RESUMES'][lang]],
                [Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]]
            ], resize_keyboard=True, one_time_keyboard=True)
        elif edit == "contact":
            return ReplyKeyboardMarkup(
                [[KeyboardButton(self.send_trans('BTN_SEND_PHONE'), request_contact=True)],
                 [KeyboardButton(self.send_trans('BTN_SEND_BACK'))]],
                one_time_keyboard=True,
                resize_keyboard=True)
        elif btn_back:
            return ReplyKeyboardMarkup([
                [Texts['BTN_SEND_BACK'][lang]], [Texts['BTN_ADD_RESUME'][lang], Texts['BTN_FIND_VACANCIES'][lang]],
                [Texts['BTN_REPLY'][lang], Texts['BTN_RESUMES'][lang]],
                [Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]]
            ], resize_keyboard=True, one_time_keyboard=True)

        else:
            return ReplyKeyboardMarkup([
                [Texts['BTN_ADD_RESUME'][lang], Texts['BTN_FIND_VACANCIES'][lang]],
                [Texts['BTN_REPLY'][lang], Texts['BTN_RESUMES'][lang]],
                [Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]]
            ], resize_keyboard=True, one_time_keyboard=True)

    def get_main_inline_buttons(self, resume_id, type_btn=None, region_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        if type_btn == "salary":
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans('BTN_SALARY_YES'),
                                         callback_data=f'all_resume_edit_salary_yes_{resume_id}'),
                    InlineKeyboardButton(self.send_trans('BTN_SALARY_NO'),
                                         callback_data=f'all_resume_edit_salary_no_{resume_id}')],
            ]

        if type_btn == "exp":
            experiences = services.getExperiences()
            for experience in experiences:
                inline_keyboard.append(
                    [InlineKeyboardButton(experience[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_exp_{experience["id"]}_{resume_id}')])

        if type_btn == "gender":
            genders = [
                {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
            ]
            for gender in genders:
                inline_keyboard.append(
                    [InlineKeyboardButton(gender['name'],
                                          callback_data=f'all_resume_edit_gender_{gender["id"]}_{resume_id}')])

        if type_btn == "region":
            regions = services.getRegions()
            for region in regions:
                inline_keyboard.append(
                    [InlineKeyboardButton(region[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_region_{region["id"]}_{resume_id}')])

        if type_btn == "district":
            districts = services.getDistricts(region_id)
            for district in districts:
                inline_keyboard.append(
                    [InlineKeyboardButton(district[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_region_district_{district["id"]}_{resume_id}')])

        if type_btn == "schedule":
            schedules = services.getSchedules()
            for schedule in schedules:
                inline_keyboard.append(
                    [InlineKeyboardButton(schedule[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_schedule_{schedule["id"]}_{resume_id}')])

        if type_btn == "language":
            languages = services.getLanguages()
            langs = self.user_data.get('langs', [])
            for language in languages:
                if language['id'] not in langs:
                    inline_keyboard.append(
                        [InlineKeyboardButton(language[f'name_{lang}'],
                                              callback_data=f'add_resume_edit_language_{language["id"]}_{resume_id}')])

        inline_keyboard.append(
            [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                  callback_data=f"all_resume_edit_absolute_back_{resume_id}")])
        if type_btn == "publication":
            inline_keyboard = [
                [
                    InlineKeyboardButton("EDIT", callback_data=f'all_resume_edit_edit_{resume_id}'),
                    InlineKeyboardButton('DELETE', callback_data=f'all_resume_edit_delete_{resume_id}')
                ]
            ]
        if type_btn is None:
            lang = self.user_model['lang']
            inline_keyboard = [
                [InlineKeyboardButton(Texts['BTN_EDIT_FIO'][lang],
                                      callback_data=f'all_resume_edit_fio_{resume_id}'),
                 InlineKeyboardButton(Texts['POSITION'][lang],
                                      callback_data=f'all_resume_edit_position_{resume_id}')],
                [InlineKeyboardButton(Texts['SALARY'][lang],
                                      callback_data=f'all_resume_edit_salary_{resume_id}'),
                 InlineKeyboardButton(Texts['SCHEDULE'][lang],
                                      callback_data=f'all_resume_edit_schedule_choise_{resume_id}')],
                [InlineKeyboardButton(Texts['LANGS'][lang],
                                      callback_data=f'all_resume_edit_lang_select_{resume_id}'),
                 InlineKeyboardButton(Texts['AGE'][lang],
                                      callback_data=f'all_resume_edit_age_{resume_id}')],
                [InlineKeyboardButton(Texts['EXPERIENCE'][lang],
                                      callback_data=f'all_resume_edit_exp_choise_{resume_id}'),
                 InlineKeyboardButton(Texts['GENDER'][lang],
                                      callback_data=f'all_resume_edit_gender_main_{resume_id}')],
                [InlineKeyboardButton(Texts['REGION'][lang],
                                      callback_data=f'all_resume_edit_region_main_{resume_id}'),
                 InlineKeyboardButton(Texts['BTN_SEND_PHONE'][lang],
                                      callback_data=f'all_resume_edit_phone_{resume_id}')],
                [InlineKeyboardButton(Texts['BTN_CHANGE_PHOTO'][lang],
                                      callback_data=f'all_resume_edit_photo_{resume_id}')],
                [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                      callback_data=f'all_resume_edit_back_{resume_id}')]
            ]

        return inline_keyboard

    def sendCategoryParent(self, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        categories = services.getCategoryParent()
        for category in categories:
            inline_keyboard.append(
                [InlineKeyboardButton(category[f'name_{lang}'],
                                      callback_data=f'add_resume_category_{category["id"]}')])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY'][lang],
                              InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], InlineKeyboardMarkup(inline_keyboard))

    def sendChildCategories(self, parent_id, message_id, chat_id):
        lang = self.user_model['lang']
        inline_keyboard = []
        categories = services.getCategoryChild(parent_id)
        cats = self.user_data.get('categories', [])

        for category in categories:
            if category['id'] not in cats:
                inline_keyboard.append(
                    [InlineKeyboardButton(category[f'name_{lang}'],
                                          callback_data=f'add_resume_categorychild_{category["id"]}')])

        if len(inline_keyboard) > 0:
            if len(cats) > 0:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                             callback_data=f'add_resume_categorychild_back'),
                        InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang],
                                             callback_data=f'add_resume_categorychild_next')
                    ])
                self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY_CHILDS'][lang],
                                  InlineKeyboardMarkup(inline_keyboard))
            else:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                             callback_data=f'add_resume_categorychild_back')
                    ])
                self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY_CHILDS'][lang],
                                  InlineKeyboardMarkup(inline_keyboard))
        else:
            self.delete_message_user(chat_id, message_id)
            self.go_message(chat_id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))
            # Texts['TEXT_SEND_MEDIA'][lang],
            # self.edit_message(chat_id, message_id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))

    def send_schedules(self, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        schedules = services.getSchedules()
        for schedule in schedules:
            inline_keyboard.append(
                [InlineKeyboardButton(schedule[f'name_{lang}'], callback_data=f'add_resume_schedule_{schedule["id"]}')])
        inline_keyboard.append(
            [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data="add_resume_schedule_back")])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_SCHEDULE'][lang],
                              InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, Texts['TEXT_SELECT_SCHEDULE'][lang], InlineKeyboardMarkup(inline_keyboard))

    def send_languages(self, message_id=None, chat_id=None):
        try:
            inline_keyboard = []
            lang = self.user_model['lang']
            languages = services.getLanguages()
            langs = self.user_data.get('langs', [])
            for language in languages:
                if language['id'] not in langs:
                    inline_keyboard.append(
                        [InlineKeyboardButton(language[f'name_{lang}'],
                                              callback_data=f'add_resume_language_{language["id"]}')])

            if len(inline_keyboard) > 0:
                if len(langs) > 0:
                    inline_keyboard.append(
                        [
                            InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                                 callback_data="add_resume_language_back"),
                            InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang],
                                                 callback_data=f'add_resume_language_next')
                        ])
                if message_id:
                    self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_LANGUAGE'][lang],
                                      InlineKeyboardMarkup(inline_keyboard))
                else:
                    self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang],
                                    InlineKeyboardMarkup(inline_keyboard))
            else:
                if message_id:
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)
                else:
                    self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

        except Exception as e:
            print('nega error: ', str(e))

    def send_experience(self, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        experiences = services.getExperiences()
        for experience in experiences:
            inline_keyboard.append(
                [InlineKeyboardButton(experience[f'name_{lang}'],
                                      callback_data=f'add_resume_experience_{experience["id"]}')])
        inline_keyboard.append(
            [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data="add_resume_experience_back")])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_EXPERIENCE'][lang],
                              InlineKeyboardMarkup(inline_keyboard))

        else:
            self.go_message(self.user.id, Texts['TEXT_EXPERIENCE'][lang], InlineKeyboardMarkup(inline_keyboard))

    def send_genders(self, message_id=None, chat_id=None):
        try:
            lang = self.user_model['lang']
            inline_keyboard = []
            genders = [
                {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
            ]
            for gender in genders:
                inline_keyboard.append(
                    [InlineKeyboardButton(gender['name'],
                                          callback_data=f'add_resume_gender_{gender["id"]}')])
            inline_keyboard.append(
                [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data="add_resume_gender_back")])

            if message_id:
                self.edit_message(chat_id, message_id, Texts['TEXT_GENDER'][lang],
                                  InlineKeyboardMarkup(inline_keyboard))
            else:
                self.go_message(self.user.id, Texts['TEXT_GENDER'][lang],
                                InlineKeyboardMarkup(inline_keyboard))

        except Exception as e:
            print('nega error: ', str(e))

    def send_region(self, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        regions = services.getRegions()
        for region in regions:
            inline_keyboard.append(
                [InlineKeyboardButton(region[f'name_{lang}'], callback_data=f'add_resume_region_{region["id"]}')])
        inline_keyboard.append(
            [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data="add_resume_region_back")])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_SEND_REGION'][lang],
                              InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, self.send_trans('TEXT_SEND_REGION'), InlineKeyboardMarkup(inline_keyboard))

    def send_district(self, region_id, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        districts = services.getDistricts(region_id)
        for district in districts:
            inline_keyboard.append(
                [InlineKeyboardButton(district[f'name_{lang}'], callback_data=f'add_resume_district_{district["id"]}')])
        inline_keyboard.append(
            [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data="add_resume_district_back")])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_SEND_DISTRICT'][lang],
                              InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, self.send_trans('TEXT_SEND_DISTRICT'), InlineKeyboardMarkup(inline_keyboard))

    def preview(self):
        try:
            lang = self.user_model['lang']
            fio = self.user_data.get('fio', "-")
            phone_number = self.user_data.get('phone_number', "-")
            post = f"💼 {fio}️"
            post = "{}\n{} - {}".format(post, Texts['POSITION'][lang], self.user_data.get('position_name', '-'))
            salary_type = self.user_data.get('salary_type', 2)
            if salary_type == 1:
                salary = self.user_data.get('salary_amount', 0)
            else:
                salary = Texts['BTN_SALARY_NO'][lang]
            post = "{}\n{} - {}".format(post, Texts['SALARY'][lang], salary)

            schedule_id = self.user_data.get('schedule_id', 0)
            if schedule_id:
                schedule = services.schuduleByID(schedule_id)
                post = "{}\n{}  -{}".format(post, Texts['SCHEDULE'][lang], schedule[f'name_{lang}'])

            langs = self.user_data.get('langs', None)
            if langs:

                langs_str = str(", ".join(map(str, langs)))
                langs_db = services.getLanguagesByids(langs_str)

                p_langs = ''
                for lang_i in langs_db:
                    name = lang_i[f'name_{lang}']
                    if p_langs == '':
                        p_langs = name
                    else:
                        p_langs = "{}, {}".format(p_langs, name)

                post = "{}\n{} - {}".format(post, Texts['LANGS'][lang], p_langs)

            post = f"{post}\n{Texts['AGE'][lang]}-{self.user_data.get('age', '-')}️"

            experience_id = self.user_data.get('experience_id', 0)
            if experience_id:
                experience = services.getExperienceById(experience_id)
                post = "{}\n{} - {}".format(post, Texts['EXPERIENCE'][lang], experience[f'name_{lang}'])

            selected_gender = self.user_data.get('genders', None)
            if selected_gender:
                genders = [
                    {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                    {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
                ]
                p_gender = ''
                for gender in genders:
                    if gender['id'] == selected_gender:
                        p_gender = gender["name"]
                        break
                post = "{}\n{} - {}".format(post, Texts['GENDER'][lang], p_gender)

            region_id = self.user_data.get('region_id', 0)

            if region_id:

                region = services.getRegionById(region_id)
                p_region = region[f'name_{lang}']
                district_id = self.user_data.get('district_id', 0)
                if district_id:
                    district = services.getDistrictById(district_id)
                    p_region = "{}, {}".format(p_region, district[f'name_{lang}'])

                post = "{}\n{} - {}".format(post, Texts['REGION'][lang], p_region)
            post = "{}\n \n{}\n☎️ {}".format(post, Texts['PHONE_C'][lang], phone_number)

            return post
        except Exception as e:
            print('view error', str(e))

    def all_preview(self, rezume):
        try:
            lang = self.user_model['lang']
            fio = f"{rezume['firstname']} {rezume['lastname']} {rezume['middlename']}"
            phone_number = rezume["phone_number"]
            post = f"💼 {fio}️"
            post = "{}\n{} - {}".format(post, Texts['POSITION'][lang], rezume["position_name"])

            salary_types = json.loads(rezume.get('salary'))
            salary_type = salary_types.get('text')
            if salary_type is None:
                salary = Texts['BTN_SALARY_NO'][lang]
            else:
                salary = salary_types.get('text')
            post = "{}\n{} - {}".format(post, Texts['SALARY'][lang], salary)

            schedule = json.loads(rezume.get('schedule_name'))
            if schedule:
                post = "{}\n{} - {}".format(post, Texts['SCHEDULE'][lang], schedule[f'{change_lang_id(lang)}'])

            langs = rezume['langs']
            if langs:
                p_langs = ''
                for l_type in langs:
                    name = l_type.get('name')
                    p_langs += name[f'{change_lang_id(lang)}'] + ", "
                post = "{}\n{} - {}".format(post, Texts['LANGS'][lang], p_langs.strip(", "))

            post = f"{post}\n{Texts['AGE'][lang]} - {rezume['user_age']}️"

            experience = json.loads(rezume.get('experience_name'))
            if experience:
                post = "{}\n{} - {}".format(post, Texts['EXPERIENCE'][lang], experience[f'{change_lang_id(lang)}'])

            selected_gender = rezume["gender"]
            if selected_gender:
                genders = [
                    {'id': 1, 'name': Texts['BTN_SEND_MALE'][lang]},
                    {'id': 2, 'name': Texts['BTN_SEND_FEMALE'][lang]},
                ]
                p_gender = ''
                for gender in genders:
                    if gender['id'] == selected_gender:
                        p_gender = gender["name"]
                        break
                post = "{}\n{} - {}".format(post, Texts['GENDER'][lang], p_gender)

            region_id = rezume['re_id']
            if region_id:
                p_region = rezume[f'region_name_{lang}']
                district_id = rezume['dis_id']
                if district_id:
                    p_region = "{}, {}".format(p_region, rezume[f'district_name_{lang}'])

                post = "{}\n{} - {}".format(post, Texts['REGION'][lang], p_region)

            post = "{}\n \n{}\n☎️ {}".format(post, Texts['PHONE_C'][lang], phone_number)
            return post
        except Exception as e:
            print('view error all:', str(e))

    def send_publication(self):
        lang = self.user_model['lang']
        inline_keyboard = [[
            InlineKeyboardButton(Texts['BTN_SEND_YES'][lang], callback_data='add_resume_confirm_yes'),
            InlineKeyboardButton(Texts['BTN_SEND_NO'][lang], callback_data='add_resume_confirm_no'),
        ]]

        post = self.preview()
        full_text = "{}\n \n{}".format(self.send_trans('TEXT_SEND_PUBLICATION'), post)
        file_type = self.user_data.get('file_type', None)
        file_id = self.user_data.get('file_id', None)
        if file_type:
            if file_type == 'photo':
                self.send_photo(self.user.id, file_id, caption=post, reply_markup=InlineKeyboardMarkup(inline_keyboard))
            else:
                self.send_video(self.user.id, file_id, caption=post, reply_markup=InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, full_text, InlineKeyboardMarkup(inline_keyboard))

    def new_record(self):
        insertResume(self._bot, self.user_model['id'], self.user_data)
        self.go_message(self.user.id, self.send_trans('TEXT_SEND_MODERATION'), self.get_main_buttons())

    def send_salary_type(self, chat_id=None, message_id=None):
        print("salary", chat_id, message_id)
        inline_keyboard = [
            [
                InlineKeyboardButton(self.send_trans('BTN_SALARY_YES'), callback_data='add_vacancy_salary_yes'),
                InlineKeyboardButton(self.send_trans('BTN_SALARY_NO'), callback_data='add_vacancy_salary_no'), ],
            [InlineKeyboardButton(self.send_trans('BTN_SEND_BACK'), callback_data='add_vacancy_salary_back')]
        ]
        if chat_id and message_id:
            self.edit_message(chat_id, message_id, self.send_trans('TEXT_TYPE_SALARY'),
                              InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, self.send_trans('TEXT_TYPE_SALARY'), InlineKeyboardMarkup(inline_keyboard))

    def start_message(self):
        self.clear_state(10)
        self.go_message(self.user.id, self.send_trans('TEXT_HOMEPAGE'), self.get_main_buttons())

    def received_message(self, msg, txt):

        user_state = self.user_data.get('state', 0)

        try:
            if not self.user_model['first_name'] or self.user_model['first_name'] == '':
                first_name = self.user_data.get('first_name', None)

                # Employee ismini kiritish uchun
                if user_state == 5:
                    services.changeFirstName(self.user_model['id'], txt)
                    self.change_state({'state': 6, 'first_name': txt})
                    self.go_message(self.user.id, self.send_trans('TEXT_TERMS_REG'), ReplyKeyboardMarkup(
                        [[KeyboardButton(self.send_trans('BTN_SEND_TERMS'))]],
                        one_time_keyboard=True,
                        resize_keyboard=True))
                elif first_name is None:
                    self.go_message(self.user.id, self.send_trans('TEXT_START_FIO'))
                    self.change_state({'state': 5})
            else:
                if not self.user_model['is_terms']:
                    if msg == self.get_trans('BTN_SEND_TERMS'):
                        services.changeTerms(self.user_model['id'])
                        self.go_message(self.user.id, self.send_trans('TEXT_TERMS_OK'), self.get_main_buttons())
                    else:
                        self.go_message(self.user.id, self.send_trans('TEXT_TERMS_REG'), ReplyKeyboardMarkup(
                            [[KeyboardButton(self.send_trans('BTN_SEND_TERMS'))]],
                            one_time_keyboard=True,
                            resize_keyboard=True))
                else:
                    print(user_state)
                    if msg == self.get_trans('BTN_ADD_RESUME'):
                        self.clear_state(10)
                        self.sendCategoryParent()

                    elif msg == self.get_trans('BTN_RESUMES'):
                        vac = getMyResumies(self.user.id)
                        if vac:
                            for v in vac:
                                self.send_all_publication(v)
                        else:
                            print('no vocancy')
                    elif msg == self.get_trans('BTN_FIND_VACANCIES'):
                        print("A")
                        self.go_message(self.user.id, self.send_trans("TEXT_SEND_SEARCH_TITLE"),
                                        self.get_search_buttons())
                        print("B")
                    # ***********************************************************************************************
                    elif msg == self.get_trans('SEARCH_CATEGORY'):
                        self.send_search_category_parent()
                    # ***********************************************************************************************

                    elif msg == self.get_trans('BTN_SEND_BACK'):
                        if user_state == 12:
                            self.change_state({'state': 12, 'categories': []})
                            self.sendCategoryParent()
                        elif user_state == 13:
                            self.change_state({'state': 12})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_MEDIA'),
                                            self.get_main_buttons(True))
                        elif user_state == 14:
                            self.change_state({'state': 13, 'position_name': None})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)
                        elif user_state == 44:
                            self.change_state({'state': 14, 'salary_type': 0, 'salary_amount': None})
                            self.send_salary_type()
                            # self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)
                        elif user_state == 15:
                            self.change_state({'state': 14})
                            self.send_salary_type()
                        elif user_state == 16:
                            self.change_state({'state': 15, 'langs': []})
                            self.send_schedules()
                        elif user_state == 17:
                            # langs = self.user_data.get('langs', [])
                            self.change_state({'state': 17, 'langs': []})
                            self.send_languages()
                        elif user_state == 18:
                            self.change_state({'state': 17})
                            self.send_experience()
                        elif user_state == 88:
                            self.change_state({'state': 17})
                            self.send_experience()
                        elif user_state == 19:
                            self.change_state({'state': 88})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))
                        elif user_state == 20:
                            self.change_state({'state': 19})
                            self.send_genders()

                        elif user_state == 21:
                            self.change_state({'state': 20})
                            # self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)
                            self.send_region()

                        elif user_state == 23:
                            self.change_state({'state': 20})
                            self.send_region()

                        elif user_state == 24:
                            self.change_state({'state': 23})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_FIO'), self.get_main_buttons(True))

                        # ***********************************************************************************************

                        elif user_state == 101:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                        elif user_state == 102:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                        elif user_state == 106:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                        elif user_state == 110:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                        elif user_state == 111:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                        elif user_state == 112:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                    elif user_state == 13:
                        print(user_state)
                        self.change_state({'state': 14, 'position_name': txt})
                        self.send_salary_type()

                    elif user_state == 44:
                        self.change_state({'state': 15, 'salary_amount': txt})
                        self.send_schedules()
                    elif user_state == 88:
                        dt = self.check_birth_date(txt)
                        if dt:
                            self.change_state({'state': 19, 'age': txt, 'dt': str(dt)})
                            self.send_genders()
                            # self.send_experience()
                        else:
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))
                    elif user_state == 23:
                        if len(txt) > 100:
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_FIO'), self.get_main_buttons(True))
                        else:
                            self.change_state({'state': 24, 'fio': txt})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_CONTACT'), ReplyKeyboardMarkup(
                                [[KeyboardButton(self.send_trans('BTN_SEND_PHONE'), request_contact=True)],
                                 [KeyboardButton(self.send_trans('BTN_SEND_BACK'))]],
                                one_time_keyboard=True,
                                resize_keyboard=True))

                    elif user_state == 24:
                        if self.is_phone_number(txt):
                            self.change_state({'state': 25, 'phone_number': txt})
                            self.send_publication()
                        else:
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_CONTACT'), ReplyKeyboardMarkup(
                                [[KeyboardButton(self.send_trans('BTN_SEND_PHONE'), request_contact=True)]],
                                one_time_keyboard=True,
                                resize_keyboard=True))

                    # ***********************************************************************************************

                    elif user_state == 101:
                        resume_id = self.user_data.get('resume_id', 0)
                        change_full_name(resume_id, txt)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True)

                    elif user_state == 102:
                        resume_id = self.user_data.get('resume_id', 0)
                        self.change_state({'position_name': txt})
                        change_position(self.user_data)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True)

                    elif user_state == 106:
                        dt = self.check_birth_date(txt)
                        if dt:
                            self.change_state({'state': 106, 'age': txt, 'dt': str(dt)})
                            resume_id = self.user_data.get('resume_id', 0)
                            change_age(resume_id, self.user_data)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                        else:
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

                    elif user_state == 110:
                        print(txt)
                        self.change_state({'state': 110, 'phone_number': txt})
                        change_phone(self.user_data)
                        resume_id = self.user_data.get('resume_id', 0)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True)

                    elif user_state == 111:
                        resume_id = self.user_data.get('resume_id', 0)
                        change_photo(self._bot, self.user_model['id'], self.user_data)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True)

                    elif user_state == 112:
                        resume_id = self.user_data.get('resume_id', 0)
                        self.change_state({'salary_amount': txt})
                        change_salary(resume_id, self.user_data)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True)

                    # ***********************************************************************************************

        except Exception as e:
            print('employee received_message: %s' % str(e))

    def send_all_publication(self, resume, type_btn=False):
        post = self.all_preview(resume)
        full_text = "{}\n \n{}".format(self.send_trans('TEXT_SEND_PUBLICATION'), post)
        resume_id = self.user_data.get('resume_id', 0)
        file_type = resume['file_type']
        file_path = resume['file_path']
        print(file_type)
        path = get_file_path(file_path)
        if type_btn:
            inline_keyboard = self.get_main_inline_buttons(resume_id=resume_id)

        else:
            inline_keyboard = [
                [
                    InlineKeyboardButton("EDIT", callback_data=f'all_resume_edit_edit_{resume["resume_id"]}'),
                    InlineKeyboardButton('DELETE', callback_data=f'all_resume_edit_delete_{resume["resume_id"]}')
                ]
            ]
        if file_type == 1:
            file_type = 'photo'
        else:
            file_type = 'video'
        print(file_type)

        if file_type:
            if file_type == 'photo':
                self.send_photo(self.user.id, open(path, 'rb'), caption=post,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard))
            else:
                self.send_video(self.user.id, open(path, 'rb'), caption=post,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, full_text, InlineKeyboardMarkup(inline_keyboard))

    def inline_query(self, data_sp, message_id, chat_id):
        print(data_sp)
        lang = self.user_model['lang']
        if data_sp[0] == 'add':
            if data_sp[2] == 'category':
                category = services.categoryByID(int(data_sp[3]))
                category_id = category['id']
                self.change_state({'state': 10, 'category_id': category_id})
                self.sendChildCategories(category_id, message_id, chat_id)
            elif data_sp[2] == 'categorychild':
                if data_sp[3] == 'back':
                    self.clear_state(10)
                    self.sendCategoryParent(message_id, chat_id)
                elif data_sp[3] == 'next':
                    self.change_state({'state': 12})
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_MEDIA'][lang], None)
                else:
                    category = services.categoryByID(int(data_sp[3]))
                    cats = self.user_data.get('categories', [])
                    cats.append(category['id'])
                    self.change_state({'state': 12, 'categories': cats})
                    self.sendChildCategories(category['parent_id'], message_id, chat_id)
            elif data_sp[2] == 'salary':
                if data_sp[3] == 'yes':
                    self.change_state({'state': 44, 'salary_type': 1})
                    self.edit_message(chat_id, message_id, self.send_trans('TEXT_SEND_SALARY'), None)
                elif data_sp[3] == 'back':
                    print("Back")

                    self.change_state({'state': 13, })
                    self.delete_message_user(chat_id, message_id)
                    self.go_message(chat_id, self.send_trans('TEXT_SEND_POSITION'), None)
                else:
                    self.change_state({'state': 15, 'salary_type': 2})
                    self.send_schedules(message_id, chat_id)
            elif data_sp[2] == 'schedule':
                if data_sp[3] == 'back':
                    self.change_state({'state': 14})
                    self.send_salary_type(chat_id, message_id)
                else:
                    self.change_state({'state': 16, 'schedule_id': int(data_sp[3])})
                    self.send_languages(message_id, chat_id)

            elif data_sp[2] == 'language':
                if data_sp[3] == 'next':
                    self.change_state({'state': 17})
                    self.send_experience(message_id, chat_id)
                elif data_sp[3] == 'back':
                    self.change_state({'state': 15, 'langs': []})
                    self.send_schedules(message_id, chat_id)
                else:
                    langs = self.user_data.get('langs', [])
                    langs.append(int(data_sp[3]))
                    self.change_state({'state': 17, 'langs': langs})
                    self.send_languages(message_id, chat_id)

            elif data_sp[2] == 'experience':
                if data_sp[3] == 'back':
                    self.change_state({'state': 17, 'langs': []})
                    self.send_languages(message_id, chat_id)
                else:
                    self.change_state({'state': 88, 'experience_id': int(data_sp[3])})
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)

            elif data_sp[2] == 'gender':
                if data_sp[3] == 'back':
                    gen = self.change_state({'state': 88})
                    print(gen)
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)
                else:
                    self.change_state({'state': 20, 'gender': data_sp[3]})
                    self.change_state({'state': 20})
                    self.send_region(message_id, chat_id)
            elif data_sp[2] == 'region':
                if data_sp[3] == 'back':
                    self.change_state({'state': 19})
                    self.send_genders(message_id, chat_id)
                else:
                    region_id = int(data_sp[3])
                    self.change_state({'state': 21, 'region_id': region_id})
                    self.send_district(region_id, message_id, chat_id)
            elif data_sp[2] == 'district':
                if data_sp[3] == 'back':
                    self.change_state({'state': 20})
                    self.send_region(message_id, chat_id)
                else:
                    self.change_state({'state': 23, 'district_id': int(data_sp[3])})
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_FIO'][lang], None)

            elif data_sp[2] == 'confirm':
                if data_sp[3] == 'yes':
                    self.delete_message_user(chat_id, message_id)
                    self.new_record()
                    self.clear_state(10)
                else:
                    self.clear_state(10)
                    self.delete_message_user(chat_id, message_id)


        elif data_sp[0] == 'all':  # all_resume_confirm_edit
            if data_sp[1] == "resume":
                if data_sp[2] == "edit":
                    # inline edit_message
                    if data_sp[3] == "edit":
                        # self.delete_message_user(chat_id, message_id)
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[4]))
                        )

                    elif data_sp[3] == "salary":
                        if data_sp[4] == "yes":
                            self.change_state({"state": 112, "resume_id": data_sp[5], 'salary_type': 1})
                            self.delete_message_user(chat_id=chat_id, message_id=message_id)
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_SALARY'),
                                            self.get_main_buttons(True, edit="back"))

                        elif data_sp[4] == "no":
                            self.change_state({"state": 113, 'salary_type': 2})
                            change_salary(int(data_sp[5]), self.user_data)
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5]))
                            )
                        else:
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[4],
                                                                                               type_btn="salary"))
                            )

                    elif data_sp[3] == "exp":
                        if data_sp[4] == "choise":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="exp"))
                            )
                        else:
                            resume_id = int(data_sp[5])
                            self.change_state({"experience_id": data_sp[4]})
                            change_exp(resume_id, self.user_data)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                    elif data_sp[3] == "gender":

                        if data_sp[4] == "main":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="gender"))
                            )
                        else:

                            self.change_state({"gender": data_sp[4]})
                            change_gender(self.user_data, data_sp[5])
                            self.delete_message_user(chat_id, message_id)
                            resume_id = int(data_sp[5])
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                    elif data_sp[3] == "region":
                        if data_sp[4] == "district":
                            self.change_state({'district_id': int(data_sp[5])})
                            change_district(resume_id=int(data_sp[6]), user_data=self.user_data)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(int(data_sp[6]))
                            self.send_all_publication(res, type_btn=True)

                        elif data_sp[4] == "main":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="region"))
                            )
                        else:
                            self.change_state({'region_id': data_sp[4]})
                            change_region(resume_id=int(data_sp[5]), user_data=self.user_data)
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="district",
                                                                                               region_id=data_sp[4])))

                    elif data_sp[3] == "schedule":
                        if data_sp[4] == "choise":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="schedule")))
                        else:
                            resume_id = int(data_sp[5])
                            self.change_state({"schedule_id": data_sp[4]})
                            change_schedule(resume_id, self.user_data)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)

                    elif data_sp[3] == "lang":


                        if data_sp[4] == 'save':
                            resume_id = int(data_sp[5])

                            change_languages(resume_id, user_data=self.user_data)

                            self.clear_state(10)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True)
                        elif data_sp[4] == 'select':
                            resume_id = data_sp[5]
                            self.clear_state(10)
                            self.change_state({'state': 115})

                            inline_keyboard = []
                            lang = self.user_model['lang']
                            languages = services.getLanguages()
                            langs = self.user_data.get('langs', [])
                            for language in languages:
                                if language['id'] not in langs:
                                    inline_keyboard.append(
                                        [InlineKeyboardButton(
                                            language[f'name_{lang}'],
                                            callback_data=f'all_resume_edit_lang_{language["id"]}_{resume_id}')])

                            if len(inline_keyboard) > 0:
                                if len(langs) > 0:
                                    inline_keyboard.append(
                                        [
                                            InlineKeyboardButton('Yakunlash',
                                                                 callback_data="all_resume_edit_lang_save"),

                                        ])

                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard)
                            )
                            print('language')
                        else:
                            lang_id = data_sp[4]
                            langs = self.user_data.get('langs', [])
                            langs.append(int(lang_id))
                            self.change_state({'state': 17, 'langs': langs, 'vacancy_id': int(data_sp[5])})

                            inline_keyboard = []
                            languages = services.getLanguages()
                            for language in languages:
                                if language['id'] not in langs:
                                    inline_keyboard.append([
                                        InlineKeyboardButton(
                                            language[f'name_{lang}'],
                                            callback_data=f'all_resume_edit_lang_{language["id"]}_{data_sp[5]}')])

                            inline_keyboard.append(
                                [
                                    InlineKeyboardButton("Yakunlash",
                                                         callback_data=f'all_resume_edit_lang_save_{data_sp[5]}')
                                ])
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard)
                            )

                    elif data_sp[3] == "absolute":
                        if data_sp[4] == "back":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(data_sp[5]))
                            )
                    elif data_sp[3] == "back":
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(
                                self.get_main_inline_buttons(data_sp[4], type_btn="publication")))
                    elif data_sp[3] == "delete":
                        delete_resume(resume_id=data_sp[4], status=3)
                        self.delete_message_user(chat_id, message_id)

                    # go_message
                    elif data_sp[3] == "fio":
                        self.change_state({"state": 101, "resume_id": data_sp[4]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_FIO'),
                                        self.get_main_buttons(True, edit="back"))

                    elif data_sp[3] == "position":
                        self.change_state({"state": 102, "resume_id": data_sp[4]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'),
                                        self.get_main_buttons(True, edit="back"))
                    elif data_sp[3] == "age":
                        self.change_state({"state": 106, "resume_id": data_sp[4]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'),
                                        self.get_main_buttons(True, edit="back"))
                    elif data_sp[3] == "phone":
                        self.change_state({"state": 110, "resume_id": data_sp[4]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_CONTACT'),
                                        self.get_main_buttons(True, edit="contact"))
                    elif data_sp[3] == "photo":
                        self.change_state({"state": 111, "resume_id": data_sp[4]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_MEDIA'),
                                        self.get_main_buttons(True, edit="back"))

        elif data_sp[0] == "search":
            if data_sp[2] == 'category':
                category = services.categoryByID(int(data_sp[3]))
                category_id = category['id']
                self.change_state({'state': 200, 'category_id': category_id})
                self.send_search_child_categories(category_id, message_id, chat_id)
            elif data_sp[2] == 'categorychild':
                if data_sp[3] == 'back':
                    self.clear_state(200)
                    self.send_search_category_parent(message_id, chat_id)
                elif data_sp[3] == 'next':
                    # self.change_state({'state': 12})
                    self.edit_message(chat_id, message_id, "Hozircha hech qanday vakansiya yo'q", None)
                else:
                    category = services.categoryByID(int(data_sp[3]))
                    cats = self.user_data.get('categories', [])
                    cats.append(category['id'])
                    self.change_state({'state': 201, 'categories': cats})
                    self.send_search_child_categories(category['parent_id'], message_id, chat_id)

    def get_contact_value(self, phone_number):
        user_state = self.user_data.get('state', 0)
        if user_state == 110:
            print(phone_number)
            self.change_state({'state': 110, 'phone_number': phone_number})
            change_phone(self.user_data)
        else:
            self.change_state({'state': 25, 'phone_number': phone_number})
            self.send_publication()

    def get_media_photo(self, file_id, file_type):
        user_state = self.user_data.get('state', 0)
        if user_state == 12 or user_state == 10:
            self.change_state({'state': 13, 'file_id': file_id, 'file_type': file_type})
            self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), self.get_main_buttons(True))
        if user_state == 111:
            self.change_state({'state': 111, 'file_id': file_id, 'file_type': file_type})
            change_photo(self._bot, self.user_model['id'], self.user_data)

            resume_id = self.user_data.get('resume_id', 0)
            res = get_resume_one(resume_id)
            self.send_all_publication(res, type_btn=True)

# ********************************************************************************************************************

    def get_search_buttons(self):
        lang = self.user_model['lang']
        return ReplyKeyboardMarkup([
            [Texts['SEARCH_NAME'][lang], Texts['SEARCH_SALARY'][lang]],
            [Texts['SEARCH_CATEGORY'][lang], Texts['SEARCH_DESCRIPTION'][lang]],
            [Texts['SEARCH_CONTACT'][lang]], [Texts['SEARCH_BACK'][lang]],
        ], resize_keyboard=True, one_time_keyboard=True)

    def send_search_category_parent(self, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        inline_keyboard = []
        categories = services.getCategoryParent()
        for category in categories:
            inline_keyboard.append(
                [InlineKeyboardButton(category[f'name_{lang}'],
                                      callback_data=f'search_resume_category_{category["id"]}')])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY'][lang],
                              InlineKeyboardMarkup(inline_keyboard))
        else:
            self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang],
                            InlineKeyboardMarkup(inline_keyboard))

    def send_search_child_categories(self, parent_id, message_id, chat_id):
        lang = self.user_model['lang']
        inline_keyboard = []
        categories = services.getCategoryChild(parent_id)
        cats = self.user_data.get('categories', [])

        for category in categories:
            if category['id'] not in cats:
                inline_keyboard.append(
                    [InlineKeyboardButton(category[f'name_{lang}'],
                                          callback_data=f'search_resume_categorychild_{category["id"]}')])

        if len(inline_keyboard) > 0:
            if len(cats) > 0:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                             callback_data=f'search_resume_categorychild_back'),
                        InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang],
                                             callback_data=f'search_resume_categorychild_next')
                    ])
                self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY_CHILDS'][lang],
                                  InlineKeyboardMarkup(inline_keyboard))
            else:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                             callback_data=f'search_resume_categorychild_back')
                    ])
                self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY_CHILDS'][lang],
                                  InlineKeyboardMarkup(inline_keyboard))
        else:
            self.delete_message_user(chat_id, message_id)
            self.go_message(chat_id, "Hozircha hech qanday vakansiya yo'q", None)


# ********************************************************************************************************************

def change_lang_id(lang):
    if lang == 1:
        language = 'uz'
    elif lang == 2:
        language = 'ru'
    else:
        language = 'en'
    return language