import logging
from tkinter.filedialog import test
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import db
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
cod={'id':''}
RASTREAR,OPTION, CADASTRAR, BIO = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.effective_user
    reply_keyboard = [['Rastrear', 'Cadastrar', 'Sobre']]
    update.message.reply_text(
        'Olá seja bem vindo ao seu bot de rastreamento. '
        'Selecione a opção desejada, ou digite Rastrear, Ajuda ou Sobre',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return OPTION

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def OpcRastreio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("OPCAO DE RASTREIO %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Por favor digite o seu Codigo de rastreio.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return RASTREAR

def rastreiaEncomenda(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    url = "http://127.0.0.1:5000/rastrear?id="+update.message.text
    r = requests.get(url)
    data = r.json()

    if(data['cod'] == "200"):
        str = '📦 ' + data['category'] + ' 📦'
        update.message.reply_text(fr"{str}")
        event = ''
        for x in reversed(data['events']):
            if(x['destCity'] is None):
                if(x['description'] == 'Objeto saiu para entrega ao destinatário'):
                    event += '🥳🎊 '+ x['description'] + ' 🎊🥳\n🚛 De ' + x['type'] + ', ' + x['city'] + ' - ' + x['uf'] + '\n⏰ ' + x['dateTime'] + '\n\n'
                elif(x['description'] == 'Objeto entregue ao destinatário'):
                    event += '🏁 '+ x['description'] + ' 🏁' + '\n⏱️ ' + x['dateTime'] + '\n\n'
                else:
                    event += x['description'] + '\nDe ' + x['type'] + ', ' + x['city'] + ' - ' + x['uf'] + '\n' + x['dateTime'] + '\n\n'
                #update.message.reply_markdown_v2(fr"{str}")
            else:
                event += x['description'] + '\n🚚 De ' + x['type'] + ', ' + x['city'] + ' - ' + x['uf'] + '\n🚩 Para ' + x['destType'] + ', ' + x['destCity'] + ' - ' + x['destUf'] + '\n⏰ ' + x['dateTime'] + '\n\n'
        update.message.reply_text(fr"{event}")

    else:
        update.message.reply_text(
            data['mensagem']
        )

    return ConversationHandler.END

def OpcCadastro(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("OPCAO DE CADASTRO %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Por favor digite o seu Codigo de rastreio.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return CADASTRAR

def cadastrarUsuario(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    jsonUpdate = db.findOne("_id",user.id)
    text = "Codigo cadastrado com sucesso!"
    user = update.message.from_user
    if(jsonUpdate is None):
        db.insertOne(user.id, user.first_name, update.message.text)
        logger.info("InsertOne REALIZADO %s: %s", user.first_name, update.message.text)
    else:
        jsonUpdate = db.findOne("user_tracking_number",update.message.text)
        if(jsonUpdate is None):
            db.updateOne(user.id, update.message.text)
            logger.info("updateOne REALIZADO %s: %s", user.first_name, update.message.text)
        else:
            text = "Não foi possivel cadastrar, codigo já cadastrado!"
            logger.info("InsertOne FALHOU %s: %s", user.first_name, update.message.text)
            
            
    update.message.reply_text(fr"{text}")
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

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OPTION: [MessageHandler(Filters.regex('^(Rastrear)$'), OpcRastreio),
                     MessageHandler(Filters.regex('^(Cadastrar)$'), OpcCadastro)],
            RASTREAR: [MessageHandler(Filters.text, rastreiaEncomenda)],
            CADASTRAR: [MessageHandler(Filters.text, cadastrarUsuario)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, rastreiaEncomenda))    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
