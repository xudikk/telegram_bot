import os.path
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, messagequeue as mq, InlineQueryHandler, )
from telegram.utils.request import Request

from ...views import (MQBot, start, received_message, get_contact_value, inline_query, received_document,
                      received_photo, received_video)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
        request = Request(con_pool_size=36)
        testbot = MQBot(settings.TOKEN_KEY, request=request, mqueue=q)
        updater = Updater(bot=testbot, use_context=True, workers=32)
        # updater = Updater(TOKEN_KEY, use_context=True, workers=8,)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, received_message))
        dispatcher.add_handler(MessageHandler(Filters.contact, get_contact_value))
        dispatcher.add_handler(CallbackQueryHandler(inline_query))
        dispatcher.add_handler(MessageHandler(Filters.document, received_document))
        dispatcher.add_handler(MessageHandler(Filters.photo, received_photo))
        dispatcher.add_handler(MessageHandler(Filters.video, received_video))

        updater.start_polling()
        updater.idle()
