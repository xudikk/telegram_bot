import re
from telegram import bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (messagequeue as mq)
import logging
from .globals import Texts
from . import services
from .company.hirer import Hirer
from .employee.employee import Employee

phone_regex = re.compile(r'^\+?1?\d{9,12}$')

class MQBot(bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)

    @mq.queuedmessage
    def forward_message(self, *args, **kwargs):
        return super(MQBot, self).forward_message(*args, **kwargs)

    @mq.queuedmessage
    def delete_message(self, chat_id, message_id, timeout=None, **kwargs):
        return super(MQBot, self).delete_message(chat_id, message_id, timeout, **kwargs)

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_photo(*args, **kwargs)

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_video(*args, **kwargs)

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_audio(*args, **kwargs)

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_document(*args, **kwargs)

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_voice(*args, **kwargs)


def text_translate(message):
    try:
        result = message.encode('utf-8')
    except AttributeError:
        result = message
    return result


def delete_message_user(context, chat_id, message_id):
    context.bot.delete_message(chat_id, message_id)


def go_message(context, user_id, message, reply_markup):
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                             disable_web_page_preview=True)


def go_message_md(context, user_id, message, reply_markup, delete=True):

    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='Markdown',
                             disable_web_page_preview=True)


def go_reply(context, user_id, message, reply_id):
    context.bot.send_message(chat_id=user_id, text=message, reply_to_message_id=reply_id, parse_mode='HTML',
                             disable_web_page_preview=True)


def go_reply_video(context, user_id, message, reply_id):
    context.bot.send_video(chat_id=user_id, text=message, reply_to_message_id=reply_id, parse_mode='HTML')


def edit_message(context, chat_id, message_id, message, reply_markup):
    try:
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message, reply_markup=reply_markup,
                                  parse_mode='HTML')
    except Exception as e:
        print('ERROR edit message: ', str(e))


def send_photo(context, user_id, photo, caption=None, reply_markup=None):
    context.bot.send_photo(user_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML')


def send_video(context, user_id, video, caption=None, reply_markup=None):
    context.bot.send_video(user_id, video=video, caption=caption, reply_markup=reply_markup, parse_mode='HTML')


def send_audio(context, user_id, audio, caption=None, reply_markup=None):
    context.bot.send_audio(user_id, audio=audio, caption=caption, reply_markup=reply_markup, parse_mode='HTML')


def send_document(context, user_id, document, caption=None, reply_markup=None):
    context.bot.send_document(user_id, document=document, caption=caption, reply_markup=reply_markup, parse_mode='HTML')


def send_voice(context, user_id, voice, caption=None, reply_markup=None):
    context.bot.send_voice(user_id, voice=voice, caption=caption, reply_markup=reply_markup, parse_mode='HTML')




def sendLangMessage(context, user_id):
    go_message(context, user_id, Texts['TEXT_START'], ReplyKeyboardMarkup([
        [Texts['BTN_LANG'][1]], [Texts['BTN_LANG'][2]]], one_time_keyboard=True, resize_keyboard=True))


def sendTypeMessage(context, user_id, lang):
    go_message(context, user_id, Texts['TEXT_TYPE'][lang], ReplyKeyboardMarkup([
        [Texts['BTN_EMPLOYER'][lang]], [Texts['BTN_CANDIDATE'][lang]]], one_time_keyboard=True, resize_keyboard=True))


def sendMainCompanyMessage(context, user_id, lang):
    go_message(context, user_id, Texts['TEXT_WELCOME'][lang], ReplyKeyboardMarkup([
        [Texts['BTN_ADD_VACANT'][lang], Texts['BTN_FIND_RESUME'][lang]],
        [Texts['BTN_REPLY'][lang], Texts['BTN_VACANTS'][lang]],
        [Texts['BTN_BALANCE'][lang], Texts['BTN_PROFILE'][lang]],
    ], one_time_keyboard=True, resize_keyboard=True))


def sendMainUserMessage(context, user_id, lang):
    go_message(context, user_id, Texts['TEXT_WELCOME_USER'][lang], ReplyKeyboardMarkup([
        [Texts['BTN_ADD_RESUME'][lang], Texts['BTN_FIND_VACANT'][lang]],
        [Texts['BTN_REPLY_USER'][lang], Texts['BTN_RESUME'][lang]],
        [Texts['BTN_REFERAL'][lang], Texts['BTN_PROFILE_USER'][lang]],
    ], one_time_keyboard=True, resize_keyboard=True))


def sendNextUserMessage(context, user_id, lang):
    go_message(context, user_id, Texts['TEXT_CONTACT_NEXT'][lang], ReplyKeyboardMarkup([
        [Texts['BTN_ADD_RESUME'][lang], Texts['BTN_FIND_VACANT'][lang]],
        [Texts['BTN_REPLY_USER'][lang], Texts['BTN_RESUME'][lang]],
        [Texts['BTN_REFERAL'][lang], Texts['BTN_PROFILE_USER'][lang]],
    ], one_time_keyboard=True, resize_keyboard=True))


def sendPhoneMessage(context, user_id, lang):
    go_message(context, user_id, Texts['TEXT_SEND_PHONE'][lang], ReplyKeyboardMarkup([
        [KeyboardButton(Texts['BTN_SEND_PHONE'][lang], request_contact=True)]], one_time_keyboard=True, resize_keyboard=True))



def parse_salary(message):
    # p = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", message)
    st = message.replace(' ', '')
    st = st.replace('.', '')
    st = st.replace(',', '')
    p = re.findall("[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+", st)
    if not p or len(p) == 0:
        return None, None
    else:
        if len(p) > 1:
            b = int(p[1])
        else:
            b = 0
        return int(p[0]), b





def start(update, context):
    user = update.message.from_user
    user_model = services.userByID(user.id)
    if user_model:
        if user_model['types_id'] == 3:
            employee = Hirer(context.bot, update, user_model)
            employee.start_message()
            return 1

        else:
            employee = Employee(context.bot, update, user_model)
            employee.start_message()
            return 1
    else:
        tg_model = services.tgUserByID(user.id)
        if not tg_model:
            tg_model = services.createTgUser(user.id, user.first_name, user.username)

        if not tg_model['lang']:
            sendLangMessage(context, user.id)
            return 1
        elif tg_model['user_type_id'] == 3:
            sendMainCompanyMessage(context, user.id, tg_model['lang'])

        else:
            sendNextUserMessage(context, user.id, tg_model['lang'])

def received_message(update, context):
    if not update.message:
        return 1
    try:
        msg = update.message.text.encode("utf-8")
    except:
        msg = update.message.text
    if update.message.chat.type == 'group' or update.message.chat.type == 'supergroup':
        return 1
    try:
        user = update.message.from_user
        user_model = services.userByID(user.id)
        if not user_model:

            tg_model = services.tgUserByID(user.id)
            if not tg_model:
                tg_model = services.createTgUser(user.id, user.first_name, user.username)
            if msg == text_translate(Texts['BTN_LANG'][1]):
                services.tgChangeLang(user.id, 1)
                tg_model = services.tgUserByID(user.id)
            elif msg == text_translate(Texts['BTN_LANG'][2]):
                services.tgChangeLang(user.id, 2)
                tg_model = services.tgUserByID(user.id)
            if msg == text_translate(Texts['BTN_EMPLOYER'][1]) or msg == text_translate(Texts['BTN_EMPLOYER'][2]) or msg == text_translate(Texts['BTN_CANDIDATE'][1]) or msg == text_translate(Texts['BTN_CANDIDATE'][2]):
                if tg_model['user_type_id']:
                    if tg_model['user_type_id'] == 3:
                        employee = Hirer(context.bot, update, user_model)
                        employee.received_message(msg, update.message.text)
                    else:
                        sendMainUserMessage(context, user.id, tg_model['lang'])
                elif msg == text_translate(Texts['BTN_EMPLOYER'][1]) or msg == text_translate(Texts['BTN_EMPLOYER'][2]):
                    services.tgChangeType(user.id, 3, tg_model)
                    user_model = services.userByID(user.id)
                    employee = Hirer(context.bot, update, user_model)
                    employee.received_message(msg, update.message.text)
                else:
                    services.tgChangeType(user.id, 2, tg_model)
                    user_model = services.userByID(user.id)
                    employee = Employee(context.bot, update, user_model)
                    employee.received_message(msg, update.message.text)
                return 1

            if not tg_model['user_type_id']:
                sendTypeMessage(context, user.id, tg_model['lang'])
                return 1

        else:
            if user_model['types_id'] == 3:
                employee = Hirer(context.bot, update, user_model)
                employee.received_message(msg, update.message.text)
                return 1
            else:
                employee = Employee(context.bot, update, user_model)
                employee.received_message(msg, update.message.text)
                return 1

        
    except Exception as e:
        print('error: ', str(e))
        # logging.warning(logging.ERROR, 'received_message error: %s' % str(e))


def inline_query(update, context):
    try:
        query = update.callback_query
        user = query.from_user
        data_sp = query.data.split("_")
        user_model = services.userByID(user.id)
        message_id = update.callback_query.message.message_id
        chat_id = update.callback_query.message.chat_id
        if user_model['types_id'] == 3:
            employer = Hirer(context.bot, update, user_model)
            employer.inline_query(data_sp, message_id, chat_id, query.id)
        else:
            employee = Employee(context.bot, update, user_model)
            employee.inline_query(data_sp, message_id, chat_id, query.id)
        return 1

    except Exception as e:
        logging.warning(logging.ERROR, 'inline_query error: %s' % str(e))

def get_contact_value(update, context):

    user_id = update.message.from_user.id
    try:
        contact = update.message.contact
        phone_number = contact.phone_number
        user_model = services.userByID(user_id)
        if user_model:
            if user_model['types_id'] == 3:
                employer = Hirer(context.bot, update, user_model)
                employer.get_contact_value(phone_number)
                return 1
            elif user_model['types_id'] == 2:
                employee = Employee(context.bot, update, user_model)
                employee.get_contact_value(phone_number)
                return 1
    except Exception as e:
        logging.warning('get_contact_value:%s' % str(e))


def received_document(update, context):
    if not update.message:
        return 1
    user = update.message.from_user
    user_model = services.userByID(user.id)

    try:
        context.user_data['file_id'] = update.message.document['file_id']
        if update.message.document['mime_type'] == 'image/jpeg' or update.message.document['mime_type'] == 'image/jpg' or update.message.document['mime_type'] == 'image/png':
            context.user_data['file_type'] = 'photo'
            context.user_data['state'] = 6
            if user_model['types_id'] == 3:
                employer = Hirer(context.bot, update, user_model)
                employer.get_media_photo(update.message.photo[0]['file_id'], 'photo')
            else:
                employee = Employee(context.bot, update, user_model)
                employee.get_media_photo(update.message.photo[0]['file_id'], 'photo')


        elif update.message.document['mime_type'] == 'video/mp4':
            if user_model['types_id'] == 3:
                employer = Hirer(context.bot, update, user_model)
                employer.get_media_photo(update.message.photo[0]['file_id'], 'video')
            else:
                employee = Employee(context.bot, update, user_model)
                employee.get_media_photo(update.message.photo[0]['file_id'], 'video')
    except Exception as e:
        logging.warning('received_document:%s' % str(e))


def received_photo(update, context):
    if not update.message:
        return 1
    user = update.message.from_user
    user_model = services.userByID(user.id)

    try:
        context.user_data['file_id'] = update.message.photo[0]['file_id']
        context.user_data['file_type'] = 'photo'

        if user_model['types_id'] == 2:
            employee = Employee(context.bot, update, user_model)
            employee.get_media_photo(update.message.photo[0]['file_id'], 'photo')
        elif user_model['types_id'] == 3:
            employer = Hirer(context.bot, update, user_model)
            employer.get_media_photo(update.message.photo[0]['file_id'], 'photo')
    except Exception as e:
        logging.warning('received_photo:%s' % str(e))


def received_video(update, context):
    if not update.message:
        return 1
    user = update.message.from_user
    user_model = services.userByID(user.id)

    context.user_data['file_id'] = update.message.video['file_id']
    context.user_data['file_type'] = 'video'
    try:
        if user_model['types_id'] == 2:
            employee = Employee(context.bot, update, user_model)
            employee.get_media_photo(update.message.video['file_id'], 'video')
        elif user_model['types_id'] == 3:
            employer = Hirer(context.bot, update, user_model)
            employer.get_media_photo(update.message.video['file_id'], 'video')
    except Exception as e:
        logging.warning('received_video:%s' % str(e))

