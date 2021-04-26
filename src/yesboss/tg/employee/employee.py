from telegram import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from ..user_data import UserData
from . import employee_service as services
from .employee_trans import Texts
from .resume import *
from .employee_service import *
import json
from ..globals import Texts as Global
from ...company.models import Companies



class Employee(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]

    def _getCompanyByUser(self):
        try:
            model = Companies.objects.filter(user_id=self.user_model['id']).order_by('id')[0:1].get()
        except Exception:
            model = None
        return model

    def get_trans(self, txt):
        try:
            result = Texts[txt][self.user_model['lang']].encode('utf-8')

        except:
            result = Texts[txt][self.user_model['lang']]
        return result

    def get_trans_global(self, txt):
        try:
            result = Global[txt][self.user_model['lang']].encode('utf-8')

        except:
            result = Global[txt][self.user_model['lang']]
        return result

    def get_main_buttons(self, changed_lang=None, btn_back=False, edit=None, profile=False, profile_lang=False):
        if changed_lang:
            lang = changed_lang
        else:
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
        elif profile:
            if profile_lang:
                return ReplyKeyboardMarkup(
                    [
                        [KeyboardButton(self.send_trans("BTN_SELECT_LANGUAGE_UZ")),
                         KeyboardButton(self.send_trans("BTN_SELECT_LANGUAGE_RU"))],
                        [KeyboardButton(Global['BTN_HOME'][lang])]
                    ], resize_keyboard=True
                )
            else:
                return ReplyKeyboardMarkup(
                    [
                        [KeyboardButton(self.send_trans("CHANGE_LANG"))],
                        [KeyboardButton(Global['BTN_HOME'][lang])]

                    ], resize_keyboard=True
                )
        else:
            return ReplyKeyboardMarkup([
                [Texts['BTN_ADD_RESUME'][lang], Texts['BTN_FIND_VACANCIES'][lang]],
                [Texts['BTN_REPLY'][lang], Texts['BTN_RESUMES'][lang]],
                [Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]]
            ], resize_keyboard=True, one_time_keyboard=True)

    def get_main_inline_buttons(self, resume_id, type_btn=None, region_id=None, number=1, cnt=1):
        lang = self.user_model['lang']
        inline_keyboard = []
        if type_btn == "salary":
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans('BTN_SALARY_YES'),
                                         callback_data=f'all_resume_edit_salary_yes_{resume_id}_{number}_{cnt}'),
                    InlineKeyboardButton(self.send_trans('BTN_SALARY_NO'),
                                         callback_data=f'all_resume_edit_salary_no_{resume_id}_{number}_{cnt}')],
            ]

        if type_btn == "exp":
            experiences = services.getExperiences()
            for experience in experiences:
                inline_keyboard.append(
                    [InlineKeyboardButton(experience[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_exp_{experience["id"]}_{resume_id}_{number}_{cnt}')])

        if type_btn == "gender":
            genders = [
                {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
            ]
            for gender in genders:
                inline_keyboard.append(
                    [InlineKeyboardButton(gender['name'],
                                          callback_data=f'all_resume_edit_gender_{gender["id"]}_{resume_id}_{number}_{cnt}')])

        if type_btn == "region":
            regions = services.getRegions()
            for region in regions:
                inline_keyboard.append(
                    [InlineKeyboardButton(region[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_region_{region["id"]}_{resume_id}_{number}_{cnt}')])

        if type_btn == "district":
            districts = services.getDistricts(region_id)
            for district in districts:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            district[f'name_{lang}'],
                            callback_data=f'all_resume_edit_region_district_{district["id"]}_{resume_id}_{number}_{cnt}'
                        )
                    ])

        if type_btn == "schedule":
            schedules = services.getSchedules()
            for schedule in schedules:
                inline_keyboard.append(
                    [InlineKeyboardButton(schedule[f'name_{lang}'],
                                          callback_data=f'all_resume_edit_schedule_{schedule["id"]}_{resume_id}_{number}_{cnt}')])

        if type_btn == "language":
            languages = services.getLanguages()
            langs = self.user_data.get('langs', [])
            for language in languages:
                if language['id'] not in langs:
                    inline_keyboard.append(
                        [InlineKeyboardButton(language[f'name_{lang}'],
                                              callback_data=f'add_resume_edit_language_{language["id"]}_{resume_id}_{number}_{cnt}')])

        inline_keyboard.append(
            [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                  callback_data=f"all_resume_edit_absolute_back_{resume_id}_{number}_{cnt}")])
        if type_btn == "publication":
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans("BTN_EDIT"),
                                         callback_data=f'all_resume_edit_edit_{resume_id}_{number}_{cnt}'),
                    InlineKeyboardButton(self.send_trans("BTN_DELETE"),
                                         callback_data=f'all_resume_edit_delete_{resume_id}_{number}_{cnt}')
                ]
            ]
            if int(number) == 1 and int(number) == int(cnt):
                inline_keyboard.append([
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'search_not')]
                )
            elif int(number) == 1:
                inline_keyboard.append([
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'all_not'),
                    InlineKeyboardButton('▶️',
                                         callback_data=f'all_next_{resume_id}_{number}_{cnt}')
                ])
            elif int(number) == int(cnt):
                inline_keyboard.append([
                    InlineKeyboardButton('◀️',
                                         callback_data=f'all_prev_{resume_id}_{number}_{cnt}'),
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'all_not')]
                )

            else:
                inline_keyboard.append([
                    InlineKeyboardButton('◀️',
                                         callback_data=f'all_prev_{resume_id}_{number}_{cnt}'),
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'all_not'),
                    InlineKeyboardButton('▶️',
                                         callback_data=f'all_next_{resume_id}_{number}_{cnt}')
                ])
        if type_btn is None:
            lang = self.user_model['lang']
            inline_keyboard = [
                [InlineKeyboardButton(Texts['BTN_EDIT_FIO'][lang],
                                      callback_data=f'all_resume_edit_fio_{resume_id}_{number}_{cnt}'),
                 InlineKeyboardButton(Texts['POSITION'][lang],
                                      callback_data=f'all_resume_edit_position_{resume_id}_{number}_{cnt}')],
                [InlineKeyboardButton(Texts['SALARY'][lang],
                                      callback_data=f'all_resume_edit_salary_{resume_id}_{number}_{cnt}'),
                 InlineKeyboardButton(Texts['SCHEDULE'][lang],
                                      callback_data=f'all_resume_edit_schedule_choise_{resume_id}_{number}_{cnt}')],
                [InlineKeyboardButton(Texts['LANGS'][lang],
                                      callback_data=f'all_resume_edit_lang_select_{resume_id}_{number}_{cnt}'),
                 InlineKeyboardButton(Texts['AGE'][lang],
                                      callback_data=f'all_resume_edit_age_{resume_id}_{number}_{cnt}')],
                [InlineKeyboardButton(Texts['EXPERIENCE'][lang],
                                      callback_data=f'all_resume_edit_exp_choise_{resume_id}_{number}_{cnt}'),
                 InlineKeyboardButton(Texts['GENDER'][lang],
                                      callback_data=f'all_resume_edit_gender_main_{resume_id}_{number}_{cnt}')],
                [InlineKeyboardButton(Texts['REGION'][lang],
                                      callback_data=f'all_resume_edit_region_main_{resume_id}_{number}_{cnt}'),
                 InlineKeyboardButton(Texts['BTN_SEND_PHONE'][lang],
                                      callback_data=f'all_resume_edit_phone_{resume_id}_{number}_{cnt}')],
                [InlineKeyboardButton(Texts['BTN_CHANGE_PHOTO'][lang],
                                      callback_data=f'all_resume_edit_photo_{resume_id}_{number}_{cnt}')],
                [InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang],
                                      callback_data=f'all_resume_edit_back_{resume_id}_{number}_{cnt}')]
            ]

        return inline_keyboard

    def sendCategoryParent(self, message_id=None, chat_id=None):
        print('sendCategoryParent')
        lang = self.user_model['lang']
        keyboards = []
        categories = services.getCategoryParent()
        for category in categories:
            keyboards.append([category[f'name_{lang}']])

        self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang],
                        ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=True))

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

    def send_schedules(self):
        lang = self.user_model['lang']
        reply_markup = []
        schedules = services.getSchedules()
        for schedule in schedules:
            reply_markup.append(
                [schedule[f'name_{lang}']])
        reply_markup.append(
            [Texts['BTN_SEND_BACK'][lang], Global['BTN_HOME'][lang]])

        self.go_message(self.user.id, Texts['TEXT_SELECT_SCHEDULE'][lang], ReplyKeyboardMarkup(reply_markup,
                                                                                               resize_keyboard=True))

    def send_languages(self, message_id=None, chat_id=None):
        try:
            keyboard = []
            lang = self.user_model['lang']
            languages = services.getLanguages()
            langs = self.user_data.get('langs', [])
            for language in languages:
                if language['id'] not in langs:
                    keyboard.append(
                        [language[f'name_{lang}']])

            if len(keyboard) > 0:
                print("A", langs)
                if len(langs) > 0:
                    keyboard.append(
                        [
                            [Texts['BTN_SEND_BACK'][lang],
                             Texts['BTN_SEND_DALE'][lang]]
                        ])
                if message_id:
                    self.edit_message(chat_id, message_id, Texts['TEXT_SELECT_LANGUAGE'][lang],
                                      ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
                else:
                    self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang],
                                    ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            else:
                print("B")
                if message_id:
                    self.edit_message(chat_id, message_id, Texts['TEXT_SEND_AGE'][lang], None)
                else:
                    self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

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
        try:
            lang = self.user_model['lang']
            keyboard = []
            genders = [
                {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
            ]
            for gender in genders:
                keyboard.append(
                    [gender['name']])
            keyboard.append(
                [Texts['BTN_SEND_BACK'][lang]])

            if message_id:
                self.go_message(chat_id, Texts['TEXT_GENDER'][lang],
                                ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            else:
                self.go_message(self.user.id, Texts['TEXT_GENDER'][lang],
                                ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

        except Exception as e:
            print('nega error: ', str(e))

    def send_region(self):
        print('sendCategoryParent')
        lang = self.user_model['lang']
        keyboards = []
        regions = services.getRegions()
        for region in regions:
            keyboards.append([region[f'name_{lang}']])

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
            # ****************************************************

            schedule_id = self.user_data.get('schedule_id', 0)
            print("schedule_id: ", schedule_id)
            if schedule_id:
                schedule = services.schuduleByID(schedule_id)
                print(schedule)
                post = "{}\n{}  -{}".format(post, Texts['SCHEDULE'][lang], schedule[f'name_{lang}'])
            # ****************************************************

            langs = self.user_data.get('langs', None)
            print("langs: ", langs)
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
            # ****************************************************
            experience_id = self.user_data.get('experience_id', 0)
            if experience_id:
                experience = services.getExperienceById(experience_id)
                post = "{}\n{} - {}".format(post, Texts['EXPERIENCE'][lang], experience[f'name_{lang}'])
            # ****************************************************

            selected_gender = self.user_data.get('gender', None)
            print("selected_gender: ", selected_gender)
            if selected_gender:
                genders = [
                    {'id': 'male', 'name': Texts['BTN_SEND_MALE'][lang]},
                    {'id': 'female', 'name': Texts['BTN_SEND_FEMALE'][lang]},
                ]
                p_gender = ''
                for gender in genders:
                    print("gender: ", gender)
                    if gender['name'] == selected_gender:
                        self.change_state({"gender": gender["id"]})
                        p_gender = gender["name"]
                        break
                post = "{}\n{} - {}".format(post, Texts['GENDER'][lang], p_gender)
            # ****************************************************

            region_id = self.user_data.get('region_id', 0)
            if region_id:
                region = services.getRegionById(region_id)
                p_region = region[f'name_{lang}']
                district_id = self.user_data.get('district_id', 0)
                if district_id:
                    district = services.getDistrictById(district_id)
                    print("district: ", district)
                    p_region = "{}, {}".format(p_region, district[f'name_{lang}'])
                post = "{}\n{} - {}".format(post, Texts['REGION'][lang], p_region)
            post = "{}\n \n{}\n☎️ {}".format(post, Texts['PHONE_C'][lang], phone_number)
            # ****************************************************

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
        keyboard = [[
            (InlineKeyboardButton(Texts['BTN_SEND_YES'][lang], callback_data="add_resume_confirm_yes")),
            (InlineKeyboardButton(Texts['BTN_SEND_NO'][lang], callback_data="add_resume_confirm_no")),
        ]]

        post = self.preview()
        full_text = "{}\n \n{}".format(self.send_trans('TEXT_SEND_PUBLICATION'), post)
        file_type = self.user_data.get('file_type', None)
        file_id = self.user_data.get('file_id', None)
        if file_type:
            if file_type == 'photo':
                self.send_photo(self.user.id, file_id, caption=post,
                                reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                self.send_video(self.user.id, file_id, caption=post,
                                reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            self.go_message(self.user.id, full_text, InlineKeyboardMarkup(keyboard))

    def new_record(self):
        insertResume(self._bot, self.user_model['id'], self.user_data)
        self.go_message(self.user.id, self.send_trans('TEXT_SEND_MODERATION'), self.get_main_buttons())

    def send_salary_type(self):
        lang = self.user_model['lang']
        inline_keyboard = ReplyKeyboardMarkup([
            [
                (self.send_trans('BTN_SALARY_YES')),
                (self.send_trans('BTN_SALARY_NO'))],
            [(self.send_trans('BTN_SEND_BACK'))],
            [Global['BTN_HOME'][lang]]
        ], resize_keyboard=True, one_time_keyboard=True
        )
        self.change_state({'state': 14, 'salary_type': 0, 'salary_amount': None})
        self.go_message(self.user.id, self.send_trans('TEXT_TYPE_SALARY'), inline_keyboard)

    def start_message(self):
        self.clear_state(10)
        self.go_message(self.user.id, self.send_trans('TEXT_HOMEPAGE'), self.get_main_buttons())

    def received_message(self, msg, txt):
        cnt = self.user_data.get("cnt", 1)
        number = self.user_data.get("number", 1)
        search_state = self.user_data.get('search_state', 0)
        user_state = self.user_data.get('state', 0)
        lang = self.user_model['lang']
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
                        self.clear_state(8)
                        categories = self.getListCategory()
                        keyboard = self.formatCategoryButtons(lang, categories)
                        self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)

                    elif msg == self.get_trans_global('BTN_HOME'):
                        self.clear_state(8)
                        keyboard = self.get_main_buttons()
                        self.go_message(self.user.id, Global['TEXT_HOME'][lang], keyboard)

                    elif msg == self.get_trans('BTN_RESUMES'):
                        resume, cnt = getMyResumies(self.user.id, 1), get_cnt_res(self.user.id)
                        self.send_all_publication(resume=resume, number=1, cnt=cnt["cnt"])

                    elif msg == self.get_trans('BTN_FIND_VACANCIES'):

                        self.go_message(self.user.id, self.send_trans("TEXT_SEND_SEARCH_TITLE"),
                                        self.get_search_buttons())

                    elif msg == self.get_trans('SEARCH_CATEGORY'):
                        self.clear_state(8)
                        self.change_state({"search_state": 2})
                        categories = self.getListCategory()
                        keyboard = self.formatCategoryButtons(lang, categories, btn_back=False)
                        self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)

                    elif msg == self.get_trans('BTN_PROFILE'):
                        self.change_state({"state": 'all'})
                        self.go_message(self.user.id, self.send_trans("PROFILE_BTN"),
                                        self.get_main_buttons(profile=True))

                    elif user_state == "all":
                        self.change_state({"state": 'lang1'})
                        self.go_message(self.user.id, Global['BTN_SELECT_LANG'][lang],
                                        self.get_main_buttons(profile=True, profile_lang=True))

                    elif user_state == "lang1":
                        if msg == self.get_trans('BTN_SELECT_LANGUAGE_UZ'):
                            self.clear_state(8)
                            self.change_profile_language(self.user_model['id'], 1)
                            self.user_model['lang'] = 1
                            keyboard = self.get_main_buttons()
                            self.go_message(self.user.id, Global['TEXT_HOME'][lang], keyboard)
                        elif msg == self.get_trans('BTN_SELECT_LANGUAGE_RU'):
                            self.clear_state(8)
                            self.change_profile_language(self.user_model['id'], 2)
                            self.user_model['lang'] = 2
                            keyboard = self.get_main_buttons()
                            self.go_message(self.user.id, Global['TEXT_HOME'][lang], keyboard)

                    elif search_state == 1:
                        vac, cnt = self.get_find_vacansies(txt), self.get_cnt_vac(txt)
                        print("vac: ", vac, "\n", "cnt: ", cnt)
                        self.send_search_publication(vacancy=vac, number=1, cnt=cnt["cnt"], keyword=txt)

                    elif search_state == 2:
                        vac, cnt = self.get_find_vacansies(txt), self.get_cnt_vac(txt)
                        print("vac: ", vac, "\n", "cnt: ", cnt)
                        self.send_search_publication(vacancy=vac, number=1, cnt=cnt["cnt"], keyword=txt)

                    elif msg == self.get_trans('BTN_SEND_BACK'):
                        if user_state == 12:
                            self.clear_state(8)
                            categories = self.getListCategory()
                            keyboard = self.formatCategoryButtons(lang, categories)
                            self.go_message(self.user.id, Texts['TEXT_SELECT_CATEGORY'][lang], keyboard)
                        elif user_state == 13:
                            self.change_state({'state': 8})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_MEDIA'),
                                            self.get_main_buttons(True))
                        elif user_state == 14:
                            self.change_state({'state': 13, 'position_name': None})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), None)

                        elif user_state == 44:
                            self.change_state({'state': 14, 'salary_type': 0, 'salary_amount': None})
                            self.send_salary_type()

                        elif user_state == 15:
                            self.change_state({'state': 14})
                            self.send_salary_type()
                        elif user_state == 16:
                            self.change_state({'state': 15, 'langs': []})
                            self.send_schedules()

                        elif user_state == 17:
                            self.change_state({'state': 16, 'langs': []})
                            langs = self.getLanguages([])
                            if langs:
                                buttons = self.format_language_buttons(lang, langs)
                                self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang], buttons)

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
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                        elif user_state == 102:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                        elif user_state == 106:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                        elif user_state == 110:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                        elif user_state == 111:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                        elif user_state == 112:
                            self.change_state({"state": 100})
                            resume_id = self.user_data.get('resume_id', 0)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                    elif user_state == 8:
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
                                    self.go_message(self.user.id, Texts['TEXT_SEND_MEDIA'][lang],
                                                    self.get_main_buttons(True))

                    elif user_state == 20:
                        if msg == self.get_trans_global('BTN_SEND_BACK'):
                            self.change_state({"state": 20})
                            print("A")
                            regions = self.get_list_region()
                            keyboard = self.format_region_buttons(lang, regions)
                            self.go_message(self.user.id, Texts['TEXT_SEND_REGION'][lang], keyboard)
                        else:
                            print("B")
                            region_id = self.user_data.get('region', 0)
                            region = self.find_region(txt, region_id)
                            if region:
                                self.change_state({'state': 21, 'region_id': region['id'], 'district_id': 0})
                                districts = self.getDistric(region['id'])
                                if districts:
                                    keyboard = self.format_region_buttons(lang, districts)
                                    self.go_message(self.user.id, Texts['TEXT_SEND_DISTRICT'][lang], keyboard)

                    elif user_state == 13:
                        self.change_state({'state': 14, 'position_name': txt})
                        self.send_salary_type()

                    elif user_state == 14:
                        if txt == self.send_trans('BTN_SALARY_YES'):
                            self.change_state({'state': 44, 'salary_type': 1})
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_SALARY'), None)
                        else:
                            self.change_state({'state': 15, 'salary_type': 2})
                            self.send_schedules()

                    elif user_state == 44:
                        self.change_state({'state': 15, 'salary_amount': txt, 'salary_type': 1})
                        self.send_schedules()

                    elif user_state == 15:
                        schedule = self.get_schedule(txt)
                        print("schedule: ", schedule)
                        self.change_state({'state': 16, 'schedule_id': schedule['id'], 'langs': []})
                        langs = self.getLanguages([])
                        if langs:
                            buttons = self.format_language_buttons(lang, langs)
                            self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang], buttons)
                    elif user_state == 16:
                        old_languages = self.user_data.get('langs', [])
                        select_lang = self.get_language_by_name(txt)
                        if msg == self.get_trans_global('BTN_SEND_BACK'):
                            self.change_state({'state': 15})
                            self.send_schedules()

                        elif msg == self.get_trans_global('BTN_SEND_DALE'):
                            self.change_state({'state': 17, 'langs': old_languages})
                            self.send_experience()
                        else:
                            print('select_lang: ', select_lang)
                            if select_lang:
                                old_languages.append(select_lang['id'])
                                self.change_state({'state': 16, 'langs': old_languages})
                                langs = self.getLanguages(old_languages)
                                print("langs A: ", old_languages)

                                if langs:
                                    buttons = self.format_language_buttons(lang, langs)
                                    self.go_message(self.user.id, Texts['TEXT_SELECT_LANGUAGE'][lang], buttons)
                                else:
                                    print("langs B: ", old_languages)
                                    self.change_state({'state': 17, 'langs': old_languages})
                                    self.send_experience()

                    elif user_state == 17:
                        exp_id = self.get_exp(txt)
                        self.change_state({'state': 88, 'experience_id': exp_id['id']})
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

                    elif user_state == 88:
                        dt = self.check_birth_date(txt)
                        if dt:
                            self.change_state({'state': 19, 'age': txt, 'dt': str(dt)})
                            self.send_genders()
                        else:
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

                    elif user_state == 19:
                        self.change_state({'state': 20, 'gender': txt})
                        self.send_region()

                    elif user_state == 21:
                        district_id = self.get_district(txt)
                        self.change_state({'state': 23, 'district_id': district_id['id']})
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_FIO'), self.get_main_buttons(True))

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

                    elif user_state == 101:
                        resume_id = self.user_data.get('resume_id', 0)
                        change_full_name(resume_id, txt)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                    elif user_state == 102:
                        resume_id = self.user_data.get('resume_id', 0)
                        self.change_state({'position_name': txt})
                        change_position(self.user_data)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                    elif user_state == 106:
                        dt = self.check_birth_date(txt)
                        if dt:
                            self.change_state({'state': 106, 'age': txt, 'dt': str(dt)})
                            resume_id = self.user_data.get('resume_id', 0)
                            change_age(resume_id, self.user_data)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                        else:
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'), self.get_main_buttons(True))

                    elif user_state == 110:
                        print(txt)
                        self.change_state({'state': 110, 'phone_number': txt})
                        change_phone(self.user_data)
                        resume_id = self.user_data.get('resume_id', 0)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                    elif user_state == 111:
                        resume_id = self.user_data.get('resume_id', 0)
                        change_photo(self._bot, self.user_model['id'], self.user_data)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)

                    elif user_state == 112:
                        resume_id = self.user_data.get('resume_id', 0)
                        self.change_state({'salary_amount': txt})
                        change_salary(resume_id, self.user_data)
                        res = get_resume_one(resume_id)
                        self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)


        except Exception as e:
            print('employee received_message: %s' % str(e))

    def send_all_publication(self, resume, number, cnt, type_btn=False):
        print("B")

        post = self.all_preview(resume)
        full_text = "{}\n \n{}".format(self.send_trans('TEXT_SEND_PUBLICATION'), post)
        file_type = resume['file_type']
        file_path = resume['file_path']
        path = get_file_path(file_path)
        if type_btn:
            inline_keyboard = self.get_main_inline_buttons(resume_id=resume["resume_id"], number=number, cnt=cnt)

        else:
            inline_keyboard = [
                [
                    InlineKeyboardButton(self.send_trans("BTN_EDIT"),
                                         callback_data=f'all_resume_edit_edit_{resume["resume_id"]}_{number}_{cnt}'),
                    InlineKeyboardButton(self.send_trans("BTN_DELETE"),
                                         callback_data=f'all_resume_edit_delete_{resume["resume_id"]}_{number}_{cnt}')
                ]
            ]
            if int(number) == 1 and int(number) == int(cnt):
                inline_keyboard.append([
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'search_not')]
                )
            elif int(number) == 1:
                inline_keyboard.append([
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'all_not'),
                    InlineKeyboardButton('▶️',
                                         callback_data=f'all_next_{resume["resume_id"]}_{number}_{cnt}')
                ])
            elif int(number) == int(cnt):
                inline_keyboard.append([
                    InlineKeyboardButton('◀️',
                                         callback_data=f'all_prev_{resume["resume_id"]}_{number}_{cnt}'),
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'all_not')]
                )

            else:
                inline_keyboard.append([
                    InlineKeyboardButton('◀️',
                                         callback_data=f'all_prev_{resume["resume_id"]}_{number}_{cnt}'),
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'all_not'),
                    InlineKeyboardButton('▶️',
                                         callback_data=f'all_next_{resume["resume_id"]}_{number}_{cnt}')
                ])

        if file_type == 1:
            file_type = 'photo'
        else:
            file_type = 'video'
        print(file_type)

        if file_type:
            if file_type == 'photo':
                print("assalom: ", self.user.id, path)
                self.send_photo(self.user.id, open(path, 'rb'), caption=post,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard))
                # print(inline_keyboard)
            else:
                self.send_video(self.user.id, open(path, 'rb'), caption=post,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard))
        else:
            print("bb")
            self.go_message(self.user.id, full_text, InlineKeyboardMarkup(inline_keyboard))

    def search_preview(self, vacancy):
        try:
            lang = self.user_model['lang']
            user_id = self.user_model['id']
            company_model = self._getCompanyByUser()
            post = f"💼 {vacancy['company_name']}️"
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

            selected_gender = vacancy.get('gender', [])
            print('selected_gender: ', selected_gender)

            if selected_gender == 1:
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang], Texts['BTN_SEND_MALE'][lang])
            elif selected_gender == 2:
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang], Texts['BTN_SEND_FEMALE'][lang])
            elif selected_gender == 3:
                post = "{}\n{}-{}".format(post, Texts['GENDER'][lang],
                                          Texts['BTN_SEND_MALE'][lang] + ', ' + Texts['BTN_SEND_FEMALE'][lang])

            region = vacancy.get(f'region_name_{change_lang_id(lang)}')
            district = vacancy.get(f'district_name_{change_lang_id(lang)}')
            if region and district:
                post = "{}\n{}-{}".format(post, Texts['REGION'][lang], region + ", " + district)

            return post
        except Exception as e:
            print('view error 333', str(e))

    def send_search_publication(self, vacancy, cnt, number, keyword):
        try:
            lang = self.user_model['lang']

            post = self.search_preview(vacancy)
            file_type = vacancy['file_type']
            file_path = vacancy['file_path']
            inline_keyboard = []
            if int(number) == 1 and int(number) == int(cnt):
                inline_keyboard.append([
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'search_not')]
                )
            elif int(number) == 1:
                inline_keyboard.append([
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'search_not'),
                    InlineKeyboardButton('▶️',
                                         callback_data=f'search_next_{vacancy["vacancy_id"]}_{number}_{cnt}_{keyword}')
                ])
            elif int(number) == (cnt):
                inline_keyboard.append([
                    InlineKeyboardButton('◀️',
                                         callback_data=f'search_prev_{vacancy["vacancy_id"]}_{number}_{cnt}_{keyword}'),
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'search_not')]
                )


            else:
                inline_keyboard.append([
                    InlineKeyboardButton('◀️',
                                         callback_data=f'search_prev_{vacancy["vacancy_id"]}_{number}_{cnt}_{keyword}'),
                    InlineKeyboardButton(f'{number}/{cnt}', callback_data=f'search_not'),
                    InlineKeyboardButton('▶️',
                                         callback_data=f'search_next_{vacancy["vacancy_id"]}_{number}_{cnt}_{keyword}')]
                )
            inline_keyboard.append([
                InlineKeyboardButton('Номер телефона',
                                     callback_data=f'contact_vacancy_{vacancy["vacancy_id"]}')
            ])

            if file_type and file_path:
                path = get_file_path(file_path)
                if file_type == 1:
                    self.send_photo(self.user.id, open(path, 'rb'), caption=post,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard))
                else:
                    self.send_video(self.user.id, open(path, 'rb'), caption=post,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard))
            else:
                self.go_message(self.user.id, post, reply_markup=InlineKeyboardMarkup(inline_keyboard))
            # ************

        except Exception as e:
            print('pub error: ', str(e))

    def inline_query(self, data_sp, message_id, chat_id, query_id):
        print(data_sp)
        lang = self.user_model['lang']

        if data_sp[0] == 'add':  # add_resume_confirm_yes
            if data_sp[2] == 'confirm':
                if data_sp[3] == 'yes':
                    self.delete_message_user(chat_id, message_id)
                    self.new_record()
                    self.clear_state(8)
                else:
                    self.clear_state(8)
                    self.delete_message_user(chat_id, message_id)
                    self.go_message(self.user.id, self.send_trans('MAIN_MENU'), reply_markup=self.get_main_buttons())
        elif data_sp[0] == "search":
            if data_sp[1] == "next":
                vac = self.get_find_vacansies(keyword=data_sp[5], count=int(data_sp[3]) + 1)
                self.send_search_publication(vacancy=vac, number=int(data_sp[3]) + 1, cnt=int(data_sp[4]),
                                             keyword=data_sp[5])
                self.delete_message_user(chat_id, message_id)
            elif data_sp[1] == "prev":
                vac = self.get_find_vacansies(keyword=data_sp[5], count=int(data_sp[3]) - 1)
                self.send_search_publication(vacancy=vac, number=int(data_sp[3]) - 1, cnt=int(data_sp[4]),
                                             keyword=data_sp[5])
                self.delete_message_user(chat_id, message_id)
        elif data_sp[0] == "show":
            if data_sp[1] == "resume":
                phone_number = self.get_resume_phone(int(data_sp[3]))
                print(phone_number)
                self.answer_callback_query(query_id,
                            f'{phone_number["firstname"]} {phone_number["lastname"]} {phone_number["middlename"]} \n{phone_number["phone_number"]}')
            elif data_sp[1] == "vacancy":
                phone_number = self.get_vac_phone(data_sp[3])
                print(phone_number)
                self.answer_callback_query(query_id, f'{phone_number["comp_name"]} \n{phone_number["phone_number"]}')

        elif data_sp[0] == "contact":
            phone_number = self.get_vac_phone(data_sp[2])
            self.answer_callback_query(query_id, phone_number["phone_number"])

        elif data_sp[0] == 'all':  # all_resume_confirm_edit
            if data_sp[1] == "next":
                resume, cnt = getMyResumies(self.user.id, int(data_sp[3]) + 1), get_cnt_res(self.user.id)
                self.send_all_publication(resume=resume, number=int(data_sp[3]) + 1, cnt=cnt["cnt"])

                self.delete_message_user(chat_id, message_id)
            elif data_sp[1] == "prev":
                resume, cnt = getMyResumies(self.user.id, int(data_sp[3]) - 1), get_cnt_res(self.user.id)
                self.send_all_publication(resume=resume, number=int(data_sp[3]) - 1, cnt=cnt["cnt"])
                self.delete_message_user(chat_id, message_id)

            elif data_sp[1] == "resume":
                if data_sp[2] == "edit":
                    # inline edit_message
                    if data_sp[3] == "edit":
                        cnt = get_cnt_res(self.user.id)
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[4],
                                                                                           number=data_sp[-2],
                                                                                           cnt=cnt["cnt"]))
                        )

                    elif data_sp[3] == "salary":
                        if data_sp[4] == "yes":
                            self.change_state({"state": 112, "resume_id": data_sp[5], 'salary_type': 1,
                                               "number": data_sp[-2],
                                               "cnt": data_sp[-1]})
                            self.delete_message_user(chat_id=chat_id, message_id=message_id)
                            self.go_message(self.user.id, self.send_trans('TEXT_SEND_SALARY'),
                                            self.get_main_buttons(True, edit="back"))

                        elif data_sp[4] == "no":
                            self.change_state({"state": 113, 'salary_type': 2})
                            change_salary(int(data_sp[5]), self.user_data)
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1]))
                            )
                        else:
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[4],
                                                                                               type_btn="salary",
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1]))
                            )

                    elif data_sp[3] == "exp":
                        if data_sp[4] == "choise":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="exp",
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1]))
                            )
                        else:
                            resume_id = int(data_sp[5])
                            self.change_state({"experience_id": data_sp[4]})
                            change_exp(resume_id, self.user_data)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=data_sp[-2], cnt=data_sp[-1])

                    elif data_sp[3] == "gender":

                        if data_sp[4] == "main":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="gender",
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1]))
                            )
                        else:
                            self.change_state({"gender": data_sp[4]})
                            change_gender(self.user_data, data_sp[5])
                            self.delete_message_user(chat_id, message_id)
                            resume_id = int(data_sp[5])
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=data_sp[-2], cnt=data_sp[-1])

                    elif data_sp[3] == "region":
                        if data_sp[4] == "district":
                            self.change_state({'district_id': int(data_sp[5])})
                            change_district(resume_id=int(data_sp[6]), user_data=self.user_data)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(int(data_sp[6]))
                            self.send_all_publication(res, type_btn=True, number=data_sp[-2], cnt=data_sp[-1])

                        elif data_sp[4] == "main":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="region",
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1]))
                            )
                        else:
                            self.change_state({'region_id': data_sp[4]})
                            change_region(resume_id=int(data_sp[5]), user_data=self.user_data)
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="district",
                                                                                               region_id=data_sp[4],
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1])))

                    elif data_sp[3] == "schedule":
                        if data_sp[4] == "choise":
                            self._bot.edit_message_reply_markup(
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(resume_id=data_sp[5],
                                                                                               type_btn="schedule",
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1])))
                        else:
                            resume_id = int(data_sp[5])
                            self.change_state({"schedule_id": data_sp[4]})
                            change_schedule(resume_id, self.user_data)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=data_sp[-2], cnt=data_sp[-1])

                    elif data_sp[3] == "lang":
                        # all_resume_edit_lang_save
                        if data_sp[4] == 'save':
                            resume_id = int(data_sp[5])

                            change_languages(resume_id, user_data=self.user_data)

                            self.clear_state(10)
                            self.delete_message_user(chat_id, message_id)
                            res = get_resume_one(resume_id)
                            self.send_all_publication(res, type_btn=True, number=data_sp[-2], cnt=data_sp[-1])
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
                                                                 callback_data=f"all_resume_edit_lang_save_{resume_id}")

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
                            self.change_state({'state': 17, 'langs': langs, 'resume_id': int(data_sp[5])})

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
                                reply_markup=InlineKeyboardMarkup(self.get_main_inline_buttons(data_sp[5],
                                                                                               number=data_sp[-2],
                                                                                               cnt=data_sp[-1]))
                            )
                    elif data_sp[3] == "back":
                        self._bot.edit_message_reply_markup(
                            chat_id=chat_id, message_id=message_id,
                            reply_markup=InlineKeyboardMarkup(
                                self.get_main_inline_buttons(data_sp[4], type_btn="publication",
                                                             number=data_sp[-2],
                                                             cnt=data_sp[-1])))
                    elif data_sp[3] == "delete":
                        delete_resume(resume_id=data_sp[4], status=3)
                        self.delete_message_user(chat_id, message_id)

                    # go_message
                    elif data_sp[3] == "fio":
                        self.change_state({"state": 101, "resume_id": data_sp[4], "number": data_sp[-2],
                                           "cnt": data_sp[-1]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_FIO'),
                                        self.get_main_buttons(True, edit="back"))

                    elif data_sp[3] == "position":
                        self.change_state({"state": 102, "resume_id": data_sp[4], "number": data_sp[-2],
                                           "cnt": data_sp[-1]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'),
                                        self.get_main_buttons(True, edit="back"))
                    elif data_sp[3] == "age":
                        self.change_state({"state": 106, "resume_id": data_sp[4], "number": data_sp[-2],
                                           "cnt": data_sp[-1]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_AGE'),
                                        self.get_main_buttons(True, edit="back"))
                    elif data_sp[3] == "phone":
                        self.change_state({"state": 110, "resume_id": data_sp[4], "number": data_sp[-2],
                                           "cnt": data_sp[-1]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_CONTACT'),
                                        self.get_main_buttons(True, edit="contact"))
                    elif data_sp[3] == "photo":
                        self.change_state({"state": 111, "resume_id": data_sp[4], "number": data_sp[-2],
                                           "cnt": data_sp[-1]})
                        self.delete_message_user(chat_id=chat_id, message_id=message_id)
                        self.go_message(self.user.id, self.send_trans('TEXT_SEND_MEDIA'),
                                        self.get_main_buttons(True, edit="back"))

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
        cnt = self.user_data.get("cnt", 0)
        number = self.user_data.get("number", 0)
        if user_state == 12 or user_state == 8:
            self.change_state({'state': 13, 'file_id': file_id, 'file_type': file_type})
            self.go_message(self.user.id, self.send_trans('TEXT_SEND_POSITION'), self.get_main_buttons(True))
        if user_state == 111:
            self.change_state({'state': 111, 'file_id': file_id, 'file_type': file_type})
            change_photo(self._bot, self.user_model['id'], self.user_data)
            resume_id = self.user_data.get('resume_id', 0)
            res = get_resume_one(resume_id)
            self.send_all_publication(res, type_btn=True, number=number, cnt=cnt)



    def get_search_buttons(self):
        self.change_state({"search_state": 1, "state": 500})
        lang = self.user_model['lang']
        return ReplyKeyboardMarkup([
            [Texts['SEARCH_CATEGORY'][lang]], [Global['BTN_HOME'][lang]],
        ], resize_keyboard=True, one_time_keyboard=True)

    # ********************************************************************************************************************



def change_lang_id(lang):
    if lang == 1:
        language = 'uz'
    elif lang == 2:
        language = 'ru'
    else:
        language = 'en'
    return language
