from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from .globals import Texts
from . import services


def go_message(context, user_id, message, reply_markup):
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                             disable_web_page_preview=True)


def edit_message(context, chat_id, message_id, message, reply_markup):
    try:
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message, reply_markup=reply_markup,
                                  parse_mode='HTML')
    except Exception as e:
        print('ERROR edit message: ', str(e))


def sendFilterCategories(context, chat_id, lang, message_id=None):
    inline_keyboard = []
    categories = services.getCategoryParent()
    for category in categories:
        inline_keyboard.append(
            [InlineKeyboardButton(category[f'name_{lang}'], callback_data=f'filterR_category_{category["id"]}')])
    if message_id:
        edit_message(context, chat_id, message_id, Texts['TEXT_RESUME_SEND_SPECIAL'][lang], InlineKeyboardMarkup(inline_keyboard))
    else:
        go_message(context, chat_id, Texts['TEXT_RESUME_SEND_SPECIAL'][lang], InlineKeyboardMarkup(inline_keyboard))


def sendFilterSubCategories(context, chat_id, lang, parent_id, message_id):
    inline_keyboard = []
    categories = services.getCategoryChild(parent_id)
    cats = context.user_data['filter_data'].get('sub_cats', [])
    for category in categories:
        if category['id'] not in cats:
            inline_keyboard.append(
                [InlineKeyboardButton(category[f'name_{lang}'], callback_data=f'filterR_child_{category["id"]}')])

    if len(inline_keyboard) > 0:
        if len(cats) > 0:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data=f'filterR_child_back'),
                    InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang], callback_data=f'filterR_child_next')
                ])
            edit_message(context, chat_id, message_id, Texts['TEXT_RESUME_SEND_CATEGORY_MORE'][lang], InlineKeyboardMarkup(inline_keyboard))
        else:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data=f'filterR_child_back')
                ])
            edit_message(context, chat_id, message_id, Texts['TEXT_RESUME_SEND_CATEGORY'][lang],
                         InlineKeyboardMarkup(inline_keyboard))
    else:
        sendFilterGender(context, chat_id, lang, message_id)


def sendFilterGender(context, user_id, lang, message_id=None):

    if lang == 1:
        both_gender = Texts['BTN_SEND_MALE'][lang] + " va " + Texts['BTN_SEND_FEMALE'][lang]
    else:
        both_gender = Texts['BTN_SEND_MALE'][lang] + " и " + Texts['BTN_SEND_FEMALE'][lang]

    inline_keyboard = [
        [
            InlineKeyboardButton(Texts['BTN_SEND_MALE'][lang], callback_data='filterR_gender_man'),
            InlineKeyboardButton(Texts['BTN_SEND_FEMALE'][lang], callback_data='filterR_gender_women')
        ],
        [
            InlineKeyboardButton(both_gender, callback_data='filterR_gender_both'),
        ]
    ]
    if message_id:
        edit_message(context, user_id, message_id, Texts['TEXT_VACANCY_GENDER'][lang], InlineKeyboardMarkup(inline_keyboard))
    else:
        go_message(context, user_id, Texts['TEXT_VACANCY_GENDER'][lang], InlineKeyboardMarkup(inline_keyboard))


def sendFilterLanguages(context, chat_id, lang, message_id=None):
    inline_keyboard = []
    languages = services.getLanguages()
    langs = context.user_data['filter_data'].get('langs', [])
    for language in languages:
        if language['id'] not in langs:
            inline_keyboard.append(
                [InlineKeyboardButton(language[f'name_{lang}'], callback_data=f'filterR_language_{language["id"]}')])

    if len(inline_keyboard) > 0:
        if len(langs) > 0:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang], callback_data=f'filterR_language_next')
                ])
        if message_id:
            edit_message(context, chat_id, message_id, Texts['TEXT_SELECT_LANGUAGE'][lang], InlineKeyboardMarkup(inline_keyboard))
        else:
            go_message(context, chat_id, Texts['TEXT_SELECT_LANGUAGE'][lang], InlineKeyboardMarkup(inline_keyboard))
    else:
        if context.user_data.get('filter_state', 0) == 3:
            pass
        else:
            sendFilterExperience(context, chat_id, lang, message_id)


def sendFilterExperience(context, chat_id, lang, message_id=None):
    inline_keyboard = []
    experiences = services.getExperiences()
    for experience in experiences:

        inline_keyboard.append(
            [InlineKeyboardButton(experience[f'name_{lang}'], callback_data=f'filterR_experience_{experience["id"]}')])
    if message_id:
        edit_message(context, chat_id, message_id, Texts['TEXT_SELECT_EXPERIENCE'][lang], InlineKeyboardMarkup(inline_keyboard))
    else:
        go_message(context, chat_id, Texts['TEXT_SELECT_EXPERIENCE'][lang], InlineKeyboardMarkup(inline_keyboard))


def sendSearchResultMenu(context, use_id, message, lang):
    buttons = [
        [KeyboardButton(text=Texts['BTN_SHOW_MORE_RESUME'][lang])],
        [KeyboardButton(text=Texts['BTN_CHANGE_REQUEST'][lang])],
        # [KeyboardButton(text=Texts['BTN_SUBSCRIBE_RESUME'][lang])],
        [KeyboardButton(text=Texts['BTN_MAIN_MENU'][lang])],
    ]
    go_message(context, use_id, message, ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

def sendSearchEditMenu(context, use_id, message, lang):
    buttons = [
        [KeyboardButton(text=Texts['BTN_FILTER_EDIT_CATEGORY'][lang]), KeyboardButton(text=Texts['BTN_FILTER_EDIT_GENDER'][lang])],
        [KeyboardButton(text=Texts['BTN_FILTER_EDIT_LANGUAGE'][lang]), KeyboardButton(text=Texts['BTN_FILTER_EDIT_EXPERIENCE'][lang])],
        [KeyboardButton(text=Texts['BTN_SHOW_RESUMES'][lang])],
        [KeyboardButton(text=Texts['BTN_MAIN_MENU'][lang])],
    ]
    go_message(context, use_id, message, ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))