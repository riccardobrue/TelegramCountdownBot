from django.http import HttpResponse
import requests
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

import logging
logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def bot_response(request, bot_response_id):
    response_id=str(bot_response_id);
    string = "Hello, I am a bot response."+response_id;

    # imposto l'URL per inviare i messaggi indietro al bot
    URL='https://api.telegram.org/bot' + "543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc" + '/sendMessage'

    # invio indietro alla chat ID il messaggio ricevuto
    richiesta = requests.get(URL, verify=False, data={'chat_id': bot_response_id, 'text': string})

    return HttpResponse(richiesta)





# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    #bot.sendMessage(update.message.chat_id, text='Hi!')

    string = "Hello, I am a bot response."

    # imposto l'URL per inviare i messaggi indietro al bot
    URL='https://api.telegram.org/bot' + "543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc" + '/sendMessage'

    # invio indietro alla chat ID il messaggio ricevuto
    richiesta = requests.get(URL, verify=False, data={'chat_id': update.message.chat_id, 'text': string})


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)
