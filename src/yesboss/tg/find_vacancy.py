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


def delete_message_user(context, chat_id, message_id):
    context.bot.delete_message(chat_id, message_id)


def sendFilterCategories(context, chat_id, lang, message_id=None):
    inline_keyboard = []
    categories = services.getCategoryParent()
    for category in categories:
        inline_keyboard.append(
            [InlineKeyboardButton(category[f'name_{lang}'], callback_data=f'filterV_category_{category["id"]}')])
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
                [InlineKeyboardButton(category[f'name_{lang}'], callback_data=f'filterV_child_{category["id"]}')])

    if len(inline_keyboard) > 0:
        if len(cats) > 0:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data=f'filterV_child_back'),
                    InlineKeyboardButton(Texts['BTN_SEND_DALE'][lang], callback_data=f'filterV_child_next')
                ])
            edit_message(context, chat_id, message_id, Texts['TEXT_RESUME_SEND_CATEGORY_MORE'][lang], InlineKeyboardMarkup(inline_keyboard))
        else:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(Texts['BTN_SEND_BACK'][lang], callback_data=f'filterV_child_back')
                ])
            edit_message(context, chat_id, message_id, Texts['TEXT_RESUME_SEND_CATEGORY'][lang],
                         InlineKeyboardMarkup(inline_keyboard))
    else:
        if context.user_data.get('filter_state', 0) == 1:
            delete_message_user(context, user.id, message_id)
        else:
            sendFilterTypeSalary(context, chat_id, lang, message_id)


def sendFilterTypeSalary(context, user_id, lang, message_id=None):
    inline_keyboard = [
        [
            InlineKeyboardButton(Texts['BTN_SALARY_YES'][lang], callback_data='filterV_salary_yes'),
            InlineKeyboardButton(Texts['BTN_SALARY_NO'][lang], callback_data='filterV_salary_no')
        ]
    ]
    if message_id:
        edit_message(context, user_id, message_id, Texts['TEXT_TYPE_SALARY'][lang],
                     InlineKeyboardMarkup(inline_keyboard))
    else:
        go_message(context, user_id, Texts['TEXT_TYPE_SALARY'][lang],
                   InlineKeyboardMarkup(inline_keyboard))


def sendSchedules(context, user_id, lang, message_id=None):
    inline_keyboard = []
    schedules = services.getSchedules()
    for schedule in schedules:

        inline_keyboard.append(
            [InlineKeyboardButton(schedule[f'name_{lang}'], callback_data=f'filterV_schedule_{schedule["id"]}')])
    if message_id:
        edit_message(context, user_id, message_id, Texts['TEXT_SELECT_SCHEDULE'][lang], InlineKeyboardMarkup(inline_keyboard))
    else:
        go_message(context, user_id, Texts['TEXT_SELECT_SCHEDULE'][lang], InlineKeyboardMarkup(inline_keyboard))


def sendSearchResultMenu(context, use_id, message, lang):
    buttons = [
        [KeyboardButton(text=Texts['BTN_SHOW_MORE_VACANCY'][lang])],
        [KeyboardButton(text=Texts['BTN_CHANGE_REQUEST'][lang])],
        # [KeyboardButton(text=Texts['BTN_SUBSCRIBE_RESUME'][lang])],
        [KeyboardButton(text=Texts['BTN_MAIN_MENU'][lang])],
    ]
    go_message(context, use_id, message, ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))


def sendSearchEditMenu(context, use_id, message, lang):
    buttons = [
        [KeyboardButton(text=Texts['BTN_FILTER_EDIT_CATEGORY'][lang]), KeyboardButton(text=Texts['BTN_FILTER_EDIT_SALARY'][lang])],
        [KeyboardButton(text=Texts['BTN_FILTER_EDIT_SCHEDULE'][lang]), KeyboardButton(text=Texts['BTN_SHOW_VACANCIES'][lang])],
        [KeyboardButton(text=Texts['BTN_MAIN_MENU'][lang])],
    ]
    go_message(context, use_id, message, ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
