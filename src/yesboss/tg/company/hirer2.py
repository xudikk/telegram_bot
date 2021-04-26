import json
from telegram import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)

from ...company.models import Companies
from ..user_data import UserData
from . import hirer_service as services
from .vacancy import insertVacancies, get_file_path, change_position, change_age, change_languages, change_media, change_schedule, change_vacancy_gender, change_experience, change_salary, change_region, change_district, delete_vacancy
from .hirer_trans import Texts
from .hirer_service import getMyVacancies, get_vacancies_one, getLanguages
from ..globals import Texts as Global




class Hirer(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]

    def get_trans(self, txt):
        try:
            result = Texts[txt][self.user_model['lang']].encode('utf-8')
        except Exception as e:
            result = Texts[txt][self.user_model['lang']]
        return result

    def get_trans_global(self, txt):
        try:
            result = Global[txt][self.user_model['lang']].encode('utf-8')
        except Exception as e:
            result = Global[txt][self.user_model['lang']]
        return result

    def get_main_buttons(self, back_btn=False, type_btn=None):

        lang = self.user_model['lang']
        buttons = []
        if back_btn:
            buttons.append([Texts['BTN_BACK'][lang]])
        elif type_btn == 'salary':
            buttons.append([Texts['BTN_SALARY_YES'][lang], Texts['BTN_SALARY_NO'][lang]])
            buttons.append([Texts['BTN_BACK'][lang]])
        elif type_btn == 'back':
            buttons.append([Texts['BTN_BACK'][lang]])
        elif type_btn == 'settings':
            buttons.append([Texts['TEXT_NAME_COMPANY'][lang]])
            buttons.append([Texts['TEXT_PHONE_COMPANY'][lang]])
            buttons.append([Texts['TEXT_LANGUAGE_COMPANY'][lang]])
            buttons.append([Texts['BTN_BACK'][lang]])

        else:
            buttons.append([Texts['BTN_ADD_VACANT'][lang], Texts['BTN_FIND_RESUME'][lang]])
            buttons.append([Texts['BTN_REPLY'][lang], Texts['BTN_VACANTS'][lang]])
            buttons.append([Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]])

        return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

    def get_search_buttons(self, back_btn=False):

        lang = self.user_model['lang']
        buttons = []
        if back_btn:
            buttons.append([Texts['BTN_BACK'][lang]])

        buttons.append([Texts['TEXT_SEND_SEARCH_CATEGORY'][lang], Texts['TEXT_SEND_SEARCH_GENDER'][lang]])
        buttons.append([Texts['TEXT_SEND_SEARCH_MAIN'][lang]])


        return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

    def _check_company(self):
        print('_check_company')
        company = services.getCompanyByUserId(self.user.id)
        return company

    def _getCompanyByUser(self):
        try:
            model = Companies.objects.filter(user_id=self.user_model['id']).order_by('id')[0:1].get()
        except Exception:
            model = None
        return model

    def sendCategoryParent(self, message_id=None, chat_id=None):
        print('sendCategoryParent')
        lang = self.user_model['lang']
        keyboards = []
        categories = services.getCategoryParent()
        for category in categories:
            keyboards.append([category[f'name_{lang}']])

        self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=True))

    def send_CategoryParent(self):
        lang = self.user_model['lang']
        buttons = []

        buttons.append([Texts['BTN_ADD_VACANT'][lang], Texts['BTN_FIND_RESUME'][lang]])
        buttons.append([Texts['BTN_REPLY'][lang], Texts['BTN_VACANTS'][lang]])
        buttons.append([Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]])

        return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

    def sendChildCategories(self, parent_id, message_id, chat_id):

        lang = self.user_model['lang']
        inline_keyboard = []
        categories = services.getCategoryChild(parent_id)
        cats = self.user_data.get('categories', [])

        for category in categories:
            if category['id'] not in cats:
                inline_keyboard.append(
                    [InlineKeyboardButton(category[f'name_{lang}'], callback_data=f'add_vacancy_categorychild_{category["id"]}')])

        if len(inline_keyboard) > 0:
            if len(cats) > 0:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data=f'add_vacancy_categorychild_back'),
                        InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang], callback_data=f'add_vacancy_categorychild_next')
                    ])
                self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY_CHILDS'][lang],
                             InlineKeyboardMarkup(inline_keyboard))
            else:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data=f'add_vacancy_categorychild_back')
                    ])
                self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_CATEGORY_CHILDS'][lang],
                             InlineKeyboardMarkup(inline_keyboard))
        else:
            self.delete_message_user(chat_id, message_id)
            self.go_message(chat_id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))

    def send_schedules(self, message_id=None, chat_id=None):
            lang = self.user_model['lang']
            reply_markup = []
            schedules = services.getSchedules()
            for schedule in schedules:
                reply_markup.append(
                    [schedule[f'name_{lang}']])
            reply_markup.append(
                [Global['BTN_SEND_BACK'][lang]])

            self.go_message(self.user.id, Texts['TEXT_SELECT_SCHEDULE'][lang], ReplyKeyboardMarkup(reply_markup,
                                                                                                   resize_keyboard=True))
    def send_languages(self, message_id=None, chat_id=None):
        print('send_languages')
        try:
            lang = self.user_model['lang']
            inline_keyboard = []
            languages = services.getLanguages()
            langs = self.user_data.get('langs', [])
            for language in languages:
                if language['id'] not in langs:
                    inline_keyboard.append(
                        [InlineKeyboardButton(language[f'name_{lang}'],
                                              callback_data=f'add_vacancy_language_{language["id"]}')])

            inline_keyboard.append(
                [
                    InlineKeyboardButton(Texts['BTN_BACK'][lang], callback_data='add_vacancy_language_back')
                ])

            if len(inline_keyboard) > 0:
                if len(langs) > 0:
                    inline_keyboard.append(
                        [
                            InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang], callback_data=f'add_vacancy_language_next')
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
                    self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'))

        except Exception as e:
            print('nega error: ', str(e))

    def send_experience(self, message_id=None, chat_id=None):
        lang = self.user_model['lang']
        keyboard = []
        experiences = services.getExperiences()
        for experience in experiences:
            keyboard.append(
                [experience[f'name_{lang}']])
        keyboard.append(
            [Texts['BTN_SEND_BACK'][lang]])
        if message_id:
            self.edit_message(chat_id, message_id, Texts['TEXT_EXPERIENCE'][lang],
                              ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

        else:
            self.go_message(self.user.id, Texts['TEXT_EXPERIENCE'][lang],
                            ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    def send_genders(self, message_id=None, chat_id=None):
        print('send_genders')
        try:
            lang = self.user_model['lang']
            keyboard = []
            genders = [
                    {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                    {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
                    ]
            selected_genders = self.user_data.get('genders', [])
            for gender in genders:
                if gender['id'] not in selected_genders:
                    keyboard.append(
                        [gender['name']])
            if len(keyboard) > 0:
                if len(selected_genders) > 0:
                    keyboard.append(
                        [self.send_trans('BTN_BACK'),

                            Texts['BTN_SEND_DALE'][lang]
                        ])
                self.go_message(self.user.id, Texts['TEXT_GENDER'][lang],
                                ReplyKeyboardMarkup(keyboard))
            else:
                return self.send_region(self.user.id)

        except Exception as e:
            print('nega error: ', str(e))

    def send_region(self, message_id=None, chat_id=None):
        print('sendCategoryParent')
        lang = self.user_model['lang']
        keyboards = []
        categories = services.getRegions()
        for category in categories:
            keyboards.append([category[f'name_{lang}']])

        self.go_message(self.user.id, Texts['TEXT_SEND_REGION'][lang],
                        ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=True))

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

            company_model = self._getCompanyByUser()
            post = f"💼 {company_model.company_name}️"

            post = "{}\n{}-{}".format(post, Texts['POSITION'][lang], self.user_data.get('position_name', '-'))

            salary_type = self.user_data.get('salary_type', 2)
            if salary_type == 1:
                salary = self.user_data.get('salary_amount', 0)
            else:
                salary = Texts['BTN_SALARY_NO'][lang]

            post = "{}\n{}-{}".format(post, Texts['SALARY'][lang], salary)

            schedule_id = self.user_data.get('schedule_id', 0)
            if schedule_id:
                schedule = services.schuduleByID(schedule_id)
                post = "{}\n{}-{}".format(post, Texts['SCHEDULE'][lang], schedule[f'name_{lang}'])

            langs = self.user_data.get('langs', None)
            if langs:

                langs_str = str(", ".join(map(str, langs)))
                langs_db = services.getLanguagesByids(langs_str)

                p_langs = ''
                for lang_i in langs_db:
                    name = lang_i[f'name_{lang}']
                    if p_langs == '':
                        p_langs = name
                        print('p_langs: ',p_langs)
                    else:
                        p_langs = "{}, {}".format(p_langs, name)


                post = "{}\n{}-{}".format(post, Texts['LANGS'][lang], p_langs)

            post = f"{post}\n{Texts['AGE'][lang]}-{self.user_data.get('age', '-')}️"

            experience_id = self.user_data.get('experience_id', 0)
            if experience_id:
                experience = services.getExperienceById(experience_id)
                post = "{}\n{}-{}".format(post, Texts['EXPERIENCE'][lang], experience[f'name_{lang}'])

            selected_genders = self.user_data.get('genders', [])
            if selected_genders:
                genders = [
                    {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                    {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},

                ]
                p_gender = ''
                for gender in genders:
                    if gender['id'] in selected_genders:
                        if p_gender == '':
                            p_gender = gender["name"]
                        else:
                            p_gender = f'{p_gender}, {gender["name"]}'
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang], p_gender)

            region_id = self.user_data.get('region_id', 0)
            if region_id:

                region = services.getRegionById(region_id)
                p_region = region[f'name_{lang}']
                district_id = self.user_data.get('district_id', 0)
                if district_id:
                    district = services.getDistrictById(district_id)
                    p_region = "{}, {}".format(p_region, district[f'name_{lang}'])

                post = "{}\n{}-{}".format(post, Texts['REGION'][lang], p_region)
            post = "{}\n \n{}\n☎️ {}".format(post, Texts['PHONE_C'][lang], company_model.phone_number)

            return post
        except Exception as e:
            print('view error 222', str(e))

    def preview_vacancy(self, vacancy):
        try:
            lang = self.user_model['lang']
            user_id = self.user_model['id']
            company_model = self._getCompanyByUser()
            post = f"💼 {company_model.company_name}️"
            post = "{}\n{}-{}".format(post, Texts['POSITION'][lang], vacancy.get('position_name', '-'))
            salary_types = json.loads(vacancy.get('salary'))
            salary_type = salary_types.get('text')
            if salary_type == None:
                salary = Texts['BTN_SALARY_NO'][lang]
            else:
                salary = salary_types.get('text')
            post = "{}\n{}-{}".format(post, Texts['SALARY'][lang], salary)
            schedule = json.loads(vacancy.get('schedule_name'))

            if schedule:
                post = "{}\n{}-{}".format(post, Texts['SCHEDULE'][lang], schedule[f'{change_lang_id(lang)}'])

            # langs = json.loads(vacancy.get('langs'))
            langs = vacancy.get('langs')
            if langs:
                p_langs = ''
                for lang_i in langs:
                    name = lang_i['name']['ru']
                    p_langs += name + ', '

                post = "{}\n{}-{}".format(post, Texts['LANGS'][lang], p_langs)

            age = json.loads(vacancy.get('vacancy_age'))
            post = f"{post}\n{Texts['AGE'][lang]}-{age.get('text', '-')}️"

            experience = json.loads(vacancy.get('experience_name'))
            if experience:
                post = "{}\n{}-{}".format(post, Texts['EXPERIENCE'][lang], experience[f'{change_lang_id(lang)}'])
            # langs = vacancy['langs']

            selected_gender = vacancy.get('gender', [])
            print('selected_gender: ', selected_gender)

            if selected_gender == 1:
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang], Texts['BTN_SEND_MALE'][lang])
            elif selected_gender == 2:
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang], Texts['BTN_SEND_FEMALE'][lang])
            elif selected_gender == 3:
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang], Texts['BTN_SEND_MALE'][lang] + ', ' +Texts['BTN_SEND_FEMALE'][lang])


            region = vacancy.get(f'region_name_{change_lang_id(lang)}')
            district = vacancy.get(f'district_name_{change_lang_id(lang)}')
            if region and district:
                post = "{}\n{}-{}".format(post, Texts['REGION'][lang], region + ", " + district)

            post = "{}\n \n{}\n☎️ {}".format(post, Texts['PHONE_C'][lang], company_model.phone_number)

            return post
        except Exception as e:
            print('view error 333', str(e))

    def send_publication(self):
        lang = self.user_model['lang']
        inline_keyboard = [[
                InlineKeyboardButton(Texts['BTN_SEND_YES'][lang], callback_data='add_vacancy_confirm_yes'),
                InlineKeyboardButton(Texts['BTN_SEND_NO'][lang], callback_data='add_vacancy_confirm_no')
            ]]
        inline_keyboard.append(
            [InlineKeyboardButton(self.send_trans('BTN_BACK'), callback_data='add_vacancy_confirm_back')]
        )
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

    def send_vacancy_publication(self, vacancy):
        print('send_vacancy_publication')

        try:
            lang = self.user_model['lang']
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans("BTN_EDIT"), callback_data=f'vacancy_edit_show_{vacancy["vacancy_id"]}'),
                    InlineKeyboardButton(self.send_trans("BTN_DELETE"), callback_data=f'vacancy_delete_show_{vacancy["vacancy_id"]}')
                ]
            ]
            post = self.preview_vacancy(vacancy)
            file_type = vacancy['file_type']
            file_path = vacancy['file_path']
            if file_type and file_path:
                path = get_file_path(file_path)
                if file_type == 1:
                    self.send_photo(self.user.id, open(path, 'rb'), caption=post, reply_markup=InlineKeyboardMarkup(inline_keyboard))
                else:
                    self.send_video(self.user.id, open(path, 'rb'), caption=post, reply_markup=InlineKeyboardMarkup(inline_keyboard))
            else:
                self.go_message(self.user.id, post, InlineKeyboardMarkup(inline_keyboard))



        except Exception as e:
            print('pub error: ', str(e))

    def send_edit_vacancy_inline(self, vacancy_id, type_btn=None, region_id=None):
        lang = self.user_model['lang']

        inline_keyboard = []
        if type_btn == None:
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans('POSITION'), callback_data=f'vacancy_edit_position_{vacancy_id}'),
                    InlineKeyboardButton(self.send_trans('SALARY'), callback_data=f'vacancy_edit_salary_{vacancy_id}'),
                ],
                [
                    InlineKeyboardButton(self.send_trans('SCHEDULE'), callback_data=f'vacancy_edit_schedule_select_{vacancy_id}'),
                    InlineKeyboardButton(self.send_trans('LANGS'), callback_data=f'vacancy_edit_langs_select_{vacancy_id}'),
                ],
                [
                    InlineKeyboardButton(self.send_trans('AGE'), callback_data=f'vacancy_edit_age_{vacancy_id}'),
                    InlineKeyboardButton(self.send_trans('EXPERIENCE'), callback_data=f'vacancy_edit_experience_select_{vacancy_id}'),
                ],
                [
                    InlineKeyboardButton(self.send_trans('GENDER'), callback_data=f'vacancy_edit_genders_select_{vacancy_id}'),

                    InlineKeyboardButton(self.send_trans('REGION'), callback_data=f'vacancy_edit_region_select_{vacancy_id}'),
                ],
                [
                    InlineKeyboardButton(self.send_trans('EDITED_MEDIA'), callback_data=f'vacancy_edit_media_{vacancy_id}'),
                ],
                [
                    InlineKeyboardButton(self.send_trans('EDITED_SAVED'), callback_data=f'vacancy_edited_{vacancy_id}'),
                ],
            ]
        elif type_btn == 'salary':
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans('BTN_SALARY_YES'), callback_data=f'vacancy_edit_salary_yes_{vacancy_id}'),
                    InlineKeyboardButton(self.send_trans('BTN_SALARY_NO'), callback_data=f'vacancy_edit_salary_no_{vacancy_id}')
                ]
            ]
        elif type_btn == 'schedule':
            schedules = services.getSchedules()
            for schedule in schedules:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(schedule[f'name_{lang}'],
                                             callback_data=f'vacancy_edit_schedule_{schedule["id"]}_{vacancy_id}')
                    ]
                )
        elif type_btn == 'langs':
            languages = services.getLanguages()
            for language in languages:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(language[f'name_{lang}'],
                                             callback_data=f'vacancy_edit_langs_{language["id"]}_{vacancy_id}')
                    ]
                )


        elif type_btn == 'genders':
            genders = [
                {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
            ]
            for gender in genders:
                inline_keyboard.append(
                    [InlineKeyboardButton(gender['name'],
                                          callback_data=f'vacancy_edit_genders_{gender["id"]}_{vacancy_id}')])
        elif type_btn == "experience":
            experiences = services.getExperiences()
            for experience in experiences:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(experience[f'name_{lang}'],
                                             callback_data=f'vacancy_edit_experience_{experience["id"]}_{vacancy_id}')
                    ]
                )
        elif type_btn == 'region':
            regions = services.getRegions()
            for region in regions:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(region[f'name_{lang}'],
                                             callback_data=f'vacancy_edit_region_{region["id"]}_{vacancy_id}')
                    ]
                )
        elif type_btn == 'district':
            districts = services.getDistricts(region_id)
            for district in districts:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(district[f'name_{lang}'],
                                             callback_data=f'vacancy_edit_region_district_{district["id"]}_{vacancy_id}')
                    ]
                )

        inline_keyboard.append(
            [
                InlineKeyboardButton(Texts['BTN_BACK'][lang], callback_data=f'vacancy_edit_back_{vacancy_id}')
            ]
        )


        return inline_keyboard

    def new_record(self):
        company_model = self._getCompanyByUser()
        insertVacancies(self._bot, self.user_model['id'], company_model, self.user_data)
        self.go_message(self.user.id, self.send_trans('TEXT_SEND_MODERATION'), None)

    def send_salary_type(self, chat_id=None, message_id=None):
        print('send_salary_type')
        if chat_id and message_id:
            self.go_message(chat_id,  self.get_trans('TEXT_TYPE_SALARY'),
                              self.get_main_buttons(type_btn="salary"))
        else:
            self.go_message(self.user.id, self.send_trans('TEXT_TYPE_SALARY'), self.get_main_buttons(type_btn="salary"))

    def send_salary_vacancy_type(self, chat_id=None, message_id=None):
        lang = self.user_model['lang']
        inline_keyboard = [
            [
                InlineKeyboardButton(self.send_trans('BTN_SALARY_YES'), callback_data='vacancy_edit_salary_yes'),
                InlineKeyboardButton(self.send_trans('BTN_SALARY_NO'), callback_data='vacancy_edit_salary_no')
            ],
            [
                InlineKeyboardButton(self.send_trans('BTN_BACK'), callback_data='vacancy_edit_salary_back')
            ]
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
        print('user_state: ', user_state)
        company_model = self._getCompanyByUser()
        lang = self.user_model['lang']
        if not company_model:
            company_name = self.user_data.get('company_name', None)

            # kompaniya nomini kiritish uchun
            if user_state == 5:
                self.change_state({'state': 6, 'company_name': txt})
                self.go_message(self.user.id, self.send_trans('TEXT_START_CONTACT'), ReplyKeyboardMarkup(
                    [[KeyboardButton(self.send_trans('BTN_SEND_PHONE'), request_contact=True)]], one_time_keyboard=True,
                    resize_keyboard=True))
            elif company_name == None:
                self.go_message(self.user.id, self.send_trans('TEXT_START_NAME'))
                self.change_state({'state': 5})

            # kompaniya contactni kiritish uchun
            elif user_state == 6:
                if self.is_phone_number(txt):
                    self.change_state({'state': 7, 'phone_number': txt})
                    services.createCompany(self.user_model['id'], self.user_data)
                    self.go_message(self.user.id, self.send_trans('TEXT_SUCCESS_REG'))

                    self.go_message(self.user.id, self.send_trans('TEXT_TERMS_REG'), ReplyKeyboardMarkup(
                        [[KeyboardButton(self.send_trans('BTN_SEND_TERMS'))]],
                        one_time_keyboard=True,
                        resize_keyboard=True))

                else:
                    self.go_message(self.user.id, self.send_trans('TEXT_START_CONTACT'), ReplyKeyboardMarkup(
                        [[KeyboardButton(self.send_trans('BTN_SEND_PHONE'), request_contact=True)]],
                        one_time_keyboard=True,
                        resize_keyboard=True))
        else:
            if not company_model.is_terms:
                if msg == self.get_trans('BTN_SEND_TERMS'):
                    company_model.is_terms = True
                    company_model.save()
                    self.go_message(self.user.id, self.send_trans('TEXT_TERMS_OK'), self.get_main_buttons())
                else:
                    self.go_message(self.user.id, self.send_trans('TEXT_TERMS_REG'), ReplyKeyboardMarkup(
                        [[KeyboardButton(self.send_trans('BTN_SEND_TERMS'))]],
                        one_time_keyboard=True,
                        resize_keyboard=True))
            else:
                if msg == self.get_trans_global('BTN_HOME'):
                    self.clear_state(8)
                    keyboard = self.get_main_buttons()
                    self.go_message(self.user.id, Global['TEXT_HOME'][lang], keyboard)

                elif msg == self.get_trans('BTN_ADD_VACANT'):
                    self.clear_state(8)
                    categories = self.getListCategory()
                    keyboard = self.formatCategoryButtons(lang, categories)
                    self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)

                elif msg == self.get_trans('BTN_SALARY_YES'):
                    print('BTN_SALARY_YES')
                    self.change_state({'state': 55})
                    self.go_message(self.user.id, Texts['TEXT_SEND_SALARY'][lang], self.get_main_buttons())

                elif msg == self.get_trans('BTN_SALARY_NO'):
                    print('BTN_SALARY_NO')
                    self.change_state({'state': 57})
                    self.send_schedules()

                elif msg == self.get_trans('BTN_VACANTS'):
                    user_id = self.user_model['id']
                    self.go_message(self.user.id, 'MY', self.get_main_buttons())
                    vac = getMyVacancies(user_id, )
                    if vac:
                        for v in vac:
                            # text = self.preview_vacancy(v)
                            photo = self.send_vacancy_publication(v)
                            # self.go_message(self.user.id, text, photo)
                    else:
                        print('no vocancy')

                elif msg == self.get_trans('BTN_FIND_RESUME'):
                    self.change_state({'state': 200})
                    self.go_message(self.user.id, self.send_trans('TEXT_SEND_SEARCH_TITLE'), self.get_search_buttons(True))

                elif msg == self.get_trans('TEXT_SEND_SEARCH_CATEGORY'):
                    self.change_state({'state': 201})
                    self.sendCategoryParent()

                elif msg == self.get_trans('TEXT_SEND_SEARCH_GENDER'):
                    self.change_state({'state': 202})
                    self.send_genders()

                elif msg == self.get_trans('TEXT_SEND_SEARCH_MAIN'):
                    self.change_state({'state': 203})
                    self.go_message(self.user.id, self.send_trans('TEXT_HOMEPAGE'), self.get_main_buttons(True))

                # elif msg == self.get_trans('BTN_BACK'):
                #     if user_state == 12 or user_state == 10:
                #         self.change_state({'state': 10})
                #         self.sendCategoryParent()
                #     elif user_state == 13:
                #         self.change_state({'state': 12})
                #         self.go_message(self.user.id, self.send_trans('TEXT_SEND_MEDIA'), self.get_main_buttons(True))
                #
                #     elif user_state == 14:
                #         self.change_state({'state': 13, 'position_name': None})
                #         self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)
                #     elif user_state == 44:
                #         self.change_state({'state': 14, 'salary_amount': None, 'salary_type': 0})
                #         self.send_salary_type()
                #     elif user_state == 15:
                #         self.change_state({'state': 14, 'position_name': txt})
                #         self.send_salary_type()
                #     elif user_state == 16:
                #         self.change_state({'state': 15, })
                #         self.send_schedules()
                #     elif user_state == 17:
                #         self.change_state({'state': 17, 'langs': []})
                #         self.send_languages()
                #     elif user_state == 18:
                #         self.change_state({'state': 17})
                #         self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), None)
                #     elif user_state == 19:
                #         self.change_state({'state': 18})
                #         self.send_experience()
                #     elif user_state == 20:
                #         self.change_state({'state': 19})
                #         self.send_genders()
                #     elif user_state == 21:
                #         self.change_state({'state': 20})
                #         self.send_region()
                #     elif user_state == 22:
                #         self.change_state({'state': 21})
                #         self.send_region()
                #
                # #     edited
                #
                #     elif user_state == 102:
                #         self.change_state({'state': 100})
                #         vacancy_id = self.user_data.get('vacancy_id', 0)
                #         vac = get_vacancies_one(vacancy_id)
                #         self.send_vacancy_publication(vac)
                #
                #     elif user_state == 105:
                #         self.change_state({'state': 100})
                #         vacancy_id = self.user_data.get('vacancy_id', 0)
                #         vac = get_vacancies_one(vacancy_id)
                #         self.send_vacancy_publication(vac)
                #
                #     elif user_state == 200:
                #         self.change_state({'state': 222})
                #         self.go_message(self.user.id, self.send_trans('TEXT_SEND_SEARCH_TITLE'),
                #                         self.get_search_buttons(True))

                # BACK BUTTONS
                # SCHEDULE BACK

                elif msg == self.get_trans_global('BTN_SEND_BACK'):
                    print('hello')
                    self.change_state({'state': 14})
                    self.send_salary_type()

                # END SCHEDULE BACK
                elif msg == self.get_trans('BTN_BACK'):
                    if user_state == 12:
                        self.change_state({'state': 8})
                        categories = self.getListCategory()
                        keyboard = self.formatCategoryButtons(lang, categories)
                        self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)
                    elif user_state == 13:
                        self.change_state({'state': 12})
                        categories = self.getListCategory()
                        keyboard = self.formatCategoryButtons(lang, categories)
                        self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)
                    elif user_state == 14:
                        self.change_state({'state': 13})
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)
                    elif user_state == 55:
                        self.change_state({'state': 14})
                        self.send_salary_type()


                # SETTINGS

                elif msg == self.get_trans('BTN_PROFILE'):
                    self.change_state({'state': 400})
                    self.go_message(self.user.id, Texts['TEXT_SETTINGS'][lang],
                                    self.get_main_buttons(type_btn='settings'))

                elif msg == self.get_trans('TEXT_NAME_COMPANY'):
                    self.change_state({'state': 401})
                    self.go_message(self.user.id, Global['TEXT_ENTER_COMPANY_NAME'][lang])

                elif msg == self.get_trans('TEXT_PHONE_COMPANY'):
                    self.change_state({'state': 402})
                    self.go_message(self.user.id, Global['BTN_CHANGE_NUMBER'][lang])

                elif msg == self.get_trans('TEXT_LANGUAGE_COMPANY'):
                    self.change_state({'state': 403})
                    self.go_message(self.user.id, Global['BTN_SELECT_LANG'][lang])

                # END SETTING

                else:
                    if user_state == 8:
                        if msg == self.get_trans_global('BTN_SEND_BACK'):
                            self.clear_state(8)
                            categories = self.getListCategory()
                            keyboard = self.formatCategoryButtons(lang, categories)
                            self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)

                        elif msg == self.get_trans_global('BTN_SEND_DALE'):
                                self.change_state({'state': 12})
                                self.go_message(self.user.id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))
                        else:
                            parent_id = self.user_data.get('parent_category', None)
                            category = self.findCategory(txt, parent_id)
                            is_parent = False
                            if category:
                                if not parent_id:
                                    parent_id = category['id']
                                    is_parent = True
                                    self.change_state({'state': 8, 'parent_category': parent_id})
                                cats = self.user_data.get('categories', [])
                                cats.append(category['id'])
                                self.change_state({'state': 8, 'categories': cats})
                                childs = self.getCategoryChilds(parent_id, cats)
                                if childs:
                                    keyboard = self.formatCategoryButtons(lang, childs, is_parent)
                                    self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)
                                else:
                                    self.change_state({'state': 12})
                                    self.go_message(self.user.id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))

                    elif user_state == 13:
                        self.change_state({'state': 14, 'position_name': txt})
                        self.send_salary_type()

                    elif user_state == 44:
                        self.change_state({'state': 15, 'salary_amount': txt, 'salary_type': 1})
                        self.send_schedules()

                    elif user_state == 17:
                        self.change_state({'state': 18, 'age': txt})
                        self.send_experience()

                    elif user_state == 55:
                        self.change_state({'state': 57, 'salary_type': txt})
                        self.send_schedules()

                    elif user_state == 57:
                        self.change_state({'state': 58, 'langs': []})
                        langs = self.getLanguages([])

                        if langs:
                            buttons = self.format_language_buttons(lang, langs)
                            self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang], buttons)

                    elif user_state == 58:
                        if msg == self.get_trans_global('BTN_SEND_BACK'):
                            self.clear_state(8)
                            self.change_state({'state': 57})
                            self.send_schedules()

                        elif msg == self.get_trans_global('BTN_SEND_DALE'):
                            self.change_state({'state': 59})
                            self.send_experience()
                        else:
                            old_languages = self.user_data.get('langs', [])
                            select_lang = self.get_language_by_name(txt)
                            if select_lang:
                                old_languages.append(select_lang['id'])
                                self.change_state({'state': 58, 'langs': old_languages})
                                langs = self.getLanguages(old_languages)
                                if langs:
                                    buttons = self.format_language_buttons(lang, langs)
                                    self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang], buttons)
                                else:
                                    self.change_state({'state': 59, 'langs': langs})
                                    self.send_experience()

                    elif user_state == 59:
                        print('user_state == 59')
                        langs = self.user_data.get('langs', [])
                        exp = self.get_exp(txt)
                        self.change_state({'state': 60, 'experience_id': exp['id']})
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

                    elif user_state == 60:
                        self.change_state({'state': 61, "age": txt, 'genders': []})
                        genders = self.getGenders(lang, [])
                        if genders:
                            buttons = self.format_gender_buttons(lang, genders)
                            self.go_message(self.user.id, Texts['TEXT_GENDER'][lang], buttons)

                    elif user_state == 61:
                        if msg == self.get_trans_global('BTN_SEND_BACK'):
                            self.change_state({'state': 59, 'genders': []})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

                        elif msg == self.get_trans_global('BTN_SEND_DALE'):
                            self.change_state({'state': 70})
                            regions = self.get_list_region()
                            keyboard = self.format_region_buttons(lang, regions)
                            self.go_message(self.user.id, Texts['TEXT_SEND_REGION'][lang], keyboard)


                        else:
                            old_genders = self.user_data.get('genders', [])
                            if msg == self.get_trans_global('BTN_SEND_MALE'):
                                old_genders.append('male')

                            elif msg == self.get_trans_global('BTN_SEND_FEMALE'):
                                old_genders.append('female')

                            genders = self.getGenders(lang, old_genders)
                            if genders and len(genders) > 0:
                                buttons = self.format_gender_buttons(lang, genders)
                                self.change_state({'state': 61, 'genders': old_genders})
                                self.go_message(self.user.id, Texts['TEXT_GENDER'][lang], buttons)
                            else:
                                self.change_state({'state': 70, 'genders': old_genders})
                                regions = self.get_list_region()
                                keyboard = self.format_region_buttons(lang, regions)
                                self.go_message(self.user.id, Texts['TEXT_SEND_REGION'][lang], keyboard)

                    elif user_state == 70:
                        print('user_state == 70')
                        if msg == self.get_trans_global('BTN_SEND_BACK'):

                            self.change_state({"state": 71})
                            regions = self.get_list_region()
                            keyboard = self.format_region_buttons(lang, regions)
                            self.go_message(self.user.id, Texts['TEXT_SEND_REGION'][lang], keyboard)

                        else:
                            region_id = self.user_data.get('region', 0)
                            region = self.find_region(txt, region_id)
                            print(region)
                            if region:
                                self.change_state({'state': 71, 'region_id': region['id'], 'district': 0})
                                districts = self.getDistric(region['id'])

                                if districts:
                                    keyboard = self.format_region_buttons(lang, districts)
                                    self.go_message(self.user.id, Texts['TEXT_SEND_DISTRICT'][lang], keyboard)

                    elif user_state == 71:
                        district_id = self.get_district(txt)
                        self.change_state({'state': 73, 'district_id': district_id['id']})
                        self.get_main_buttons(True)
                        self.send_publication()

                    #         edited

                    elif user_state == 101:
                        self.change_state({'state': 100})
                        vacancy_id = self.user_data.get('vacancy_id', 0)
                        vacancy = change_position(vacancy_id, txt)
                    elif user_state == 105:
                        self.change_state({'state': 100})
                        vacancy_id = self.user_data.get('vacancy_id', 0)
                        change_age(vacancy_id, txt)
                        vac = get_vacancies_one(vacancy_id)
                        self.send_vacancy_publication(vac)
                    elif user_state == 102:
                        vacancy_id = self.user_data.get('vacancy_id', 0)
                        self.change_state({'salary_amount': txt})
                        change_salary(vacancy_id, self.user_data)
                        vac = get_vacancies_one(vacancy_id)
                        self.send_vacancy_publication(vac)
                    elif user_state == 200:
                        self.change_state({'state': 222})
                        self.go_message(self.user.id, self.send_trans('TEXT_HOMEPAGE'), self.get_main_buttons(True))

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
                    self.sendCategoryParent(message_id, chat_id)
                elif data_sp[3] == 'next':
                    self.change_state({'state': 12})
                    self.delete_message_user(chat_id, message_id)
                    self.go_message(chat_id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))
                else:
                    category = services.categoryByID(int(data_sp[3]))
                    cats = self.user_data.get('categories', [])
                    cats.append(category['id'])
                    self.change_state({'state': 12, 'categories': cats})
                    self.sendChildCategories(category['parent_id'], message_id, chat_id)
            elif data_sp[2] == 'salary':
                print('salary')
                if data_sp[3] == 'yes':
                    self.change_state({'state': 44})
                    self.edit_message(chat_id, message_id, self.send_trans('TEXT_SEND_SALARY'), None)
                elif data_sp[3] == 'back':
                    self.change_state({'state': 13, })
                    self.delete_message_user(chat_id, message_id)
                    self.go_message(chat_id, self.send_trans('TEXT_SEND_POSITION'), None)
                else:
                    print('salary no')
                    self.change_state({'state': 15, 'salary_type': 2})
                    self.send_schedules(message_id, chat_id)


            elif data_sp[2] == 'schedule':
                print('schedule')
                if data_sp[3] == 'back':
                    self.change_state({'state': 14})
                    self.send_salary_type(chat_id, message_id)
                else:
                    self.change_state({'state': 16, 'schedule_id': int(data_sp[3])})
                    self.send_languages(message_id, chat_id)
            elif data_sp[2] == 'language':
                if data_sp[3] == 'next':
                    self.change_state({'state': 17})
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)
                elif data_sp[3] == 'back':
                    print('back')
                    self.change_state({'state': 15, 'langs': []})
                    self.send_schedules(message_id, chat_id)
                else:
                    print('else')
                    langs = self.user_data.get('langs', [])
                    langs.append(int(data_sp[3]))
                    self.change_state({'state': 17, 'langs': langs})
                    self.send_languages(message_id, chat_id)
            elif data_sp[2] == 'experience':
                print('experience')
                user_state = self.user_data.get('state', 0)
                if data_sp[3] == 'back':
                    self.change_state({'state': 17,})
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)
                else:
                    self.change_state({'state': 19, 'experience_id': int(data_sp[3]),'genders': []})
                    self.send_genders(message_id, chat_id)

            elif data_sp[2] == 'genders':
                print('gender')
                if data_sp[3] == 'next':
                    self.change_state({'state': 70})
                    self.send_region(message_id, chat_id)
                elif data_sp[3] == 'back':
                    self.change_state({'state': 17})
                    self.send_experience(message_id, chat_id)

                else:
                    genders = self.user_data.get('genders', [])
                    genders.append(data_sp[3])
                    self.change_state({'state': 20, 'genders': genders})
                    self.send_genders(message_id, chat_id)
            elif data_sp[2] == 'region':
                print('region')
                if data_sp[3] == 'back':
                    self.change_state({'state': 19, 'genders': []})
                    self.send_genders(message_id, chat_id)
                region_id = int(data_sp[3])
                self.change_state({'state': 21, 'region_id': region_id})
                self.send_district(region_id, message_id, chat_id)
            elif data_sp[2] == 'district':
                print('district')
                if data_sp[3] == 'back':
                    self.change_state({'state': 20})
                    self.send_region(message_id, chat_id)
                self.change_state({'state': 23, 'district_id': int(data_sp[3])})
                self.delete_message_user(chat_id, message_id)
                self.send_publication()
            elif data_sp[2] == 'confirm':
                print('confirm')
                if data_sp[3] == 'yes':
                    self.delete_message_user(chat_id, message_id)
                    self.new_record()
                    self.clear_state(10)
                elif data_sp[3] == 'back':
                    self.change_state({'state': 21})
                    self.delete_message_user(chat_id, message_id)
                    self.send_district(region_id=self.user_data.get('region_id', None), chat_id=chat_id)
                else:
                    self.clear_state(10)
                    self.delete_message_user(chat_id, message_id)

        # edited

        elif data_sp[0] == 'vacancy':
            if data_sp[1] == 'edit':
                if data_sp[2] == 'show':
                    self._bot.edit_message_reply_markup(
                        chat_id=chat_id, message_id=message_id,
                        reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(vacancy_id=data_sp[3]))
                    )
                if data_sp[2] == 'position':
                    self.change_state({'state': 101, 'vacancy_id': data_sp[3]})
                    self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)
                    print('position')

                elif data_sp[2] == 'salary':
                    if data_sp[3] == 'yes':
                        self.change_state({'state': 102, 'vacancy_id': data_sp[4], 'salary_type': 1})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_SALARY'),
                                        self.get_main_buttons(True))
                    elif data_sp[3] == 'no':
                        self.change_state({'state': 112, 'vacancy_id': data_sp[4], 'salary_type': 2})
                        vacancy = change_salary(int(data_sp[4]), self.user_data)
                        vacancy_id = int(data_sp[4])
                        vac = get_vacancies_one(vacancy_id)
                        self.send_vacancy_publication(vac)
                    else:
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(data_sp[3], 'salary'))
                        )

                elif data_sp[2] == 'schedule':
                    if data_sp[3] == 'select':
                        self.clear_state(10)
                        self.change_state({'state': 110})
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(data_sp[4], 'schedule', ))
                        )
                    else:
                        vacancy_id = int(data_sp[4])
                        if data_sp[3]:
                            vacancy = change_schedule(vacancy_id, int(data_sp[3]))
                            self.delete_message_user(chat_id, message_id)
                            vac = get_vacancies_one(vacancy_id)
                            self.send_vacancy_publication(vac)

                elif data_sp[2] == 'langs':
                    print('langs')
                    if data_sp[3] == 'save':
                        print('save')
                        vacancy_id = int(data_sp[4])
                        langs = self.user_data.get('langs', [])
                        vacancy = change_languages(vacancy_id, langs)
                        self.clear_state(10)
                        self.delete_message_user(chat_id, message_id)
                        vac = get_vacancies_one(vacancy_id)
                        self.send_vacancy_publication(vac)

                    elif data_sp[3] == 'select':
                        print('select')
                        self.clear_state(10)
                        self.change_state({'state': 104})
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(data_sp[4], 'langs', ))
                        )
                    else:
                        print('else')
                        lang_id = data_sp[3]
                        langs = self.user_data.get('langs', [])
                        langs.append(int(lang_id))
                        self.change_state({'state': 17, 'langs': langs, 'vacancy_id': int(data_sp[4])})

                        inline_keyboard = []
                        languages = services.getLanguages()
                        for language in languages:
                            if language['id'] not in langs:
                                inline_keyboard.append(
                                    [InlineKeyboardButton(language[f'name_{lang}'],
                                                          callback_data=f'vacancy_edit_langs_{language["id"]}_{data_sp[4]}')])

                        inline_keyboard.append(
                            [
                                InlineKeyboardButton("Yakunlash", callback_data=f'vacancy_edit_langs_save_{data_sp[4]}')
                            ])
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard)
                        )

                elif data_sp[2] == 'age':
                    self.change_state({'state': 105, 'vacancy_id':  data_sp[3]})
                    self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))
                    self.delete_message_user(chat_id, message_id)

                elif data_sp[2] == 'experience':
                    if data_sp[3] == "select":
                        print('910')
                        self.clear_state(10)
                        self.change_state({'state': 112})
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(data_sp[4], "experience")))
                    else:
                        vacancy_id = int(data_sp[4])
                        change_experience(vacancy_id, int(data_sp[3]))
                        self.delete_message_user(chat_id, message_id)
                        vac = get_vacancies_one(vacancy_id)
                        self.send_vacancy_publication(vac)

                elif data_sp[2] == 'genders':
                    print('genders')
                    if data_sp[3] == 'save':
                        print('save')
                        vacancy_id = int(data_sp[4])
                        genders = self.user_data.get('genders', [])
                        if 'male' in genders and 'female' in genders:
                            change_vacancy_gender(vacancy_id, 3)
                        elif 'male' in genders:
                            change_vacancy_gender(vacancy_id, 1)
                        else:
                            change_vacancy_gender(vacancy_id, 2)

                        self.clear_state(10)
                        self.delete_message_user(chat_id, message_id)
                        vac = get_vacancies_one(vacancy_id)
                        self.send_vacancy_publication(vac)

                    elif data_sp[3] == 'select':
                        print('select')
                        self.clear_state(10)
                        self.change_state({'state': 107})
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(data_sp[4], 'genders', ))
                        )
                    else:
                        print('else')
                        gender_id = data_sp[3]
                        genders = self.user_data.get('genders', [])
                        genders.append(gender_id)
                        self.change_state({'state': 17, 'genders': genders, 'vacancy_id': int(data_sp[4])})

                        inline_keyboard = []

                        all_genders = [
                            {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                            {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
                        ]
                        for gender in all_genders:
                            if gender['id'] not in genders:
                                inline_keyboard.append(
                                    [InlineKeyboardButton(gender[f'name'],
                                                          callback_data=f'vacancy_edit_genders_{gender["id"]}_{data_sp[4]}')])

                        inline_keyboard.append(
                            [
                                InlineKeyboardButton("Yakunlash", callback_data=f'vacancy_edit_genders_save_{data_sp[4]}')
                            ])

                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard)
                        )

                elif data_sp[2] == 'region':
                    if data_sp[3] == 'district':
                        self.change_state({'district_id': data_sp[4]})
                        change_district(data_sp[5], user_data=self.user_data)
                        self.delete_message_user(chat_id, message_id)
                        vac = get_vacancies_one(int(data_sp[5]))
                        self.send_vacancy_publication(vac)
                    elif data_sp[3] == 'select':
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(data_sp[4], 'region'))
                        )
                    else:
                        self.change_state({'region_id': data_sp[3]})
                        change_region(data_sp[4], user_data=self.user_data)
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.send_edit_vacancy_inline(vacancy_id=data_sp[4],
                                                                                            type_btn='district',
                                                                                            region_id=data_sp[3]))
                        )


                elif data_sp[2] == 'media':
                    self.change_state({'state': 109, 'vacancy_id': data_sp[3]})
                    self.delete_message_user(chat_id=chat_id, message_id=message_id)
                    self.go_message(chat_id, Texts['TEXT_SEND_MEDIA'][lang], self.get_main_buttons(True))
                    print('media')

                elif data_sp[2] == 'back':
                    print('come back')
                    self.delete_message_user(chat_id, message_id)
                    vac = get_vacancies_one(int(data_sp[3]))
                    self.send_vacancy_publication(vac)

            elif data_sp[1] == 'delete':
                vacancy_id = data_sp[3]
                status_id = 3
                delete_vacancy(vacancy_id, status_id)
                self.delete_message_user(chat_id, message_id)

    def get_contact_value(self, phone_number):
        self.change_state({'state': 7, 'phone_number': phone_number})
        services.createCompany(self.user_model['id'], self.user_data)
        self.go_message(self.user.id, self.send_trans('TEXT_SUCCESS_REG'))

        self.go_message(self.user.id, self.send_trans('TEXT_TERMS_REG'), ReplyKeyboardMarkup(
            [[KeyboardButton(self.send_trans('BTN_SEND_TERMS'))]],
            one_time_keyboard=True,
            resize_keyboard=True))

    def get_media_photo(self, file_id, file_type,):
        user_state = self.user_data.get('state', 0)
        print('user_state: ', user_state)
        if user_state == 12 or user_state == 8:
            print('comeaaa')
            self.change_state({'state': 13, 'file_id': file_id, 'file_type': file_type})
            self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)
        elif user_state == 109:
            print('come')
            self.change_state({'state': 100, 'file_id': file_id, 'file_type': file_type})
            change_media(self._bot, self.user_model['id'], self.user_data)
            vacancy_id = self.user_data.get('vacancy_id', 0)
            vac = get_vacancies_one(vacancy_id)
            self.send_vacancy_publication(vac)

def change_lang_id(lang):
    l = ''
    if lang == 1:
        l = 'uz'
    elif lang == 2:
        l = 'ru'
    else:
        l = 'en'
    return l

