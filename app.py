from telegram.ext import Updater, CommandHandler
import logging
import db_manager
import datetime
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))


def start(bot, update):
    db_manager.add()
    savedMessage=db_manager.get()

    string="_FromDB: "+savedMessage+"_"
    string+="_ChatID: "+str(update.message.chat_id)+"_"
    string+="_Name: "+str(update.message.from_user.first_name)
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!"+string)

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


def openshiftStart():
    updater = Updater('541177999:AAE3-K_4-pj7WMMLnjS4PPnG1NeHdMiqVa4')
    dispatcher = updater.dispatcher
    #queue = updater.job_queue

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('hello', hello))

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
    message=db_manager.get(31,"test123",0)
    print(message)



#openshiftStart()
localTesting()