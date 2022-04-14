import logging
from tkinter.filedialog import test
from xml.dom.expatbuilder import parseString
from xml.etree.ElementTree import tostring
from xml.sax import parse
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
import json
import data_base
import get_json_request
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
cod={'id':''}
RASTREAR,OPTION, CADASTRAR, LISTAR = range(4)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.effective_user
    reply_keyboard = [['Rastrear', 'Cadastrar', 'Listar']]
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
    #url = "http://127.0.0.1:5000/rastrear?id="+update.message.text
    #r = requests.get(url)
    #data = r.json()
    #print(url)
    data = json.loads(get_json_request.rastreio(update.message.text))
    if(data['cod'] == "200"):
        str = '📦 ' + data['category'] + ' 📦'
        update.message.reply_text(fr"{str}")
        event = ''
        for x in reversed(data['events']):
            try:
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
            except:
                if(x['destCity'] is None):
                    event += x['description'] + '\nDe ' + x['city'] + ', ' + x['type']  + '\n' + x['dateTime'] + '\n\n'
                #update.message.reply_markdown_v2(fr"{str}")
                else:
                    event += x['description'] + '\n🚚 De ' + x['city'] + ' - ' + x['type'] + '\n🚩 Para ' + x['destType'] + ', ' + x['destCity'] + ' - ' + x['destUf'] + '\n⏰ ' + x['dateTime'] + '\n\n'
        update.message.reply_text(fr"{event}")
        logger.info("CODIGO RASTREADO COM SUCESSO %s: %s", user.first_name, update.message.text)

    else:
        logger.info("CODIGO NAO RASTREADO %s: %s", user.first_name, update.message.text)
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
    jsonUpdate = data_base.findOne("_id",user.id)
    text = "Codigo cadastrado com sucesso!"
    user = update.message.from_user
    if(jsonUpdate is None):
        data_base.insertOne(user.id, user.first_name, update.message.text)
        logger.info("InsertOne REALIZADO %s: %s", user.first_name, update.message.text)
    else:
        jsonUpdate = data_base.findOne("user_tracking_number",[update.message.text, user.id])
        if(jsonUpdate is None):
            data_base.updateOne(user.id, update.message.text)
            logger.info("updateOne REALIZADO %s: %s", user.first_name, update.message.text)
        else:
            text = "Não foi possivel cadastrar, codigo já cadastrado!"
            logger.info("updateOne FALHOU %s: %s", user.first_name, update.message.text)
            
            
    update.message.reply_text(fr"{text}")
    return ConversationHandler.END

def OpcListar(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("OPCAO DE LISTAR CODIGOS %s: %s", user.first_name, update.message.text)
    data = []
    reply_keyboard = []
    update.message.reply_text(
        'Lista de Codigos:',
        reply_markup=ReplyKeyboardRemove(),
    )
    jsonData = data_base.findOne("_id", user.id)
    if(jsonData is None):
        text="Lista vazia!"
    else:
        text=""
        for x in jsonData["user_tracking_number"]:
            text += x + '\n'
            data.append(x)
        reply_keyboard.append(data)
    update.message.reply_text(
        fr"{text}",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )
    
    

    ##return ConversationHandler.END