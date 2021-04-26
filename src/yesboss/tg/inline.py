import os.path
from queue import Queue
from threading import Thread
from telegram import bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, MessageHandler, Filters, messagequeue as mq)

from telegram.utils.request import Request

from telegram import Update
from telegram.ext import Dispatcher
from telegram.error import TelegramError
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .globals import Texts, TOKEN_KEY
from . import services

def inline_query(update, context):
    try:
        query = update.callback_query
        user = query.from_user
        data_sp = query.data.split("_")
    except Exception as e:
        state[update.callback_query.from_user.id] = 1
        logging.warning(logging.ERROR, 'get_value error: %s' % str(e))