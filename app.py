import logging
import db_manager
import datetime
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


DATE, MESSAGE  = range(2)


def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))


def alarm(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')

def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


#==============================================================================================
def clear(user_data):
    if 'data' in user_data:
        del user_data['data']
    user_data.clear()
#==========================------------------------------------
def timer_start(bot, update):
    user = update.message.from_user
    logger.info("Start received from %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Hello! Set up your countdown, please send me a date (dd/mm/yyyy)')
    return DATE
#==========================------------------------------------
def set_timer_date(bot, update,user_data):
    user = update.message.from_user
    logger.info("Countdown date from %s: %s", user.first_name, update.message.text)

    targetDate = datetime.datetime.strptime(update.message.text, '%d/%m/%Y')
    today = datetime.datetime.utcnow()

    if (today < targetDate):
        update.message.reply_text('Perfect! If you want you can set a message for this countdown!')
        user_data['data'] = update.message.text
        return MESSAGE
    else:
        clear(user_data)
        update.message.reply_text('Date not valid!')
        return ConversationHandler.END

#==========================------------------------------------
def set_timer_message(bot, update,user_data):
    set_countdown(update, update.message, user_data['data'])
    clear(user_data)
    return ConversationHandler.END
#==========================------------------------------------
def skip_timer_message(bot, update, user_data):
    set_countdown(update, None, user_data['data'])
    clear(user_data)
    return ConversationHandler.END

#==========================------------------------------------
def set_countdown(update, message, data):
    insertionMessage = db_manager.add(update.message.chat_id, update.message.from_user.first_name, message, data, 0)
    savedCountdown = db_manager.getSingle(update.message.chat_id, update.message.from_user.first_name, 0)

    update.message.reply_text("Countdown set. Bye!")


#==========================------------------------------------
def dismiss(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s dismissed the conversation.", user.first_name)
    update.message.reply_text('Dismissed. Bye!')

    clear(user_data)
    return ConversationHandler.END

#==============================================================================================
def show_countdowns(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("Message from %s: %s", user.first_name, update.message.text)

    countdowns=db_manager.getAll(chat_id,user.first_name)
    message=""
    for countdown in countdowns:
        message+=str(countdown["date"])+"_"+countdown["message"]+"\n"

    update.message.reply_text('LIST:('+ message +')')

#==============================================================================================

def openshiftStart():
    updater = Updater('541177999:AAE3-K_4-pj7WMMLnjS4PPnG1NeHdMiqVa4')
    dispatcher = updater.dispatcher

    # ==============================================================================================
    # Add conversation handler with the states DATE and MESSAGE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', timer_start)],
        states={
            DATE: [
                RegexHandler('^([0]?[1-9]|[1|2][0-9]|[3][0|1])[/]([0]?[1-9]|[1][0-2])[/]([0-9]{4}|[0-9]{2})$', set_timer_date,pass_user_data=True)
            ],
            MESSAGE: [
                MessageHandler(Filters.text, set_timer_message,pass_user_data=True),
                RegexHandler('^([/]skip)$', skip_timer_message,pass_user_data=True)
            ]
        },
        fallbacks=[
            #CommandHandler('dismiss', dismiss,pass_user_data=True),
            RegexHandler('^([/]dismiss)$', dismiss,pass_user_data=True)
        ]
    )
    dispatcher.add_handler(conv_handler)
    # ==============================================================================================

    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler('show', show_countdowns))

    dispatcher.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dispatcher.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dispatcher.add_error_handler(error)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    updater.start_polling()
    updater.idle()








def localTesting():
    message=db_manager.add(30,"test123","testing message","05/02/2018",0)
    print(message)
    message=db_manager.edit(30,"test123","test345","06/03/2019",0)
    print(message)
    message=db_manager.getSingle(30,"test123",0)
    print(message)

    record=db_manager.getAll(30,"test123")
    for doc in record:
        print(doc)



openshiftStart()
#localTesting()