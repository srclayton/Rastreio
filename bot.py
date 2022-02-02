import logging
import json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
cod={'id':''}
RASTREAR,OPTION, LOCATION, BIO = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Rastrear', 'Ajuda', 'Sobre']]

    update.message.reply_text(
        'Olá seja bem vindo ao seu bot de rastreamento. '
        'Selecione a opção desejada, ou digite Rastrear, Ajuda ou Sobre',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return OPTION


def rastreio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Codigo de rastreio %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Por favor digite o seu Codigo de rastreio.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return RASTREAR


def exportCod(update: Update, context: CallbackContext) -> int:
    cod['id'] = update.message.text
    with open('cod.json', 'w',encoding='utf8') as f:
        json.dump(cod,f,ensure_ascii=False,default=lambda o: o.__dict__)

    #return LOCATION



def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    a = open("token.txt","r")
    token = a.read()
    a.close()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OPTION: [MessageHandler(Filters.regex('^(Rastrear|Ajuda|Sobre)$'), rastreio)],
            RASTREAR: [MessageHandler(Filters.text, exportCod)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
