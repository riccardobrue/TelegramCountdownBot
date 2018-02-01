from telegram.ext import Updater, CommandHandler
import logging

def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))


def start(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!"+update.message.chat_id)


updater = Updater('543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc')
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


updater.start_polling()
updater.idle()