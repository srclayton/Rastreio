import logging
from tkinter import N
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
    encoding='utf-8', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
cod={'id':''}
RASTREAR,OPTION, CADASTRAR, LISTAR, DELETAR = range(5)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    ConversationHandler.END
    user = update.effective_user
    reply_keyboard = [['Rastrear', 'Cadastrar', 'Listar', 'Deletar']]
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
        update.message.reply_text(fr"{str}",None)
        event = ''
        for x in reversed(data['events']):
            try:
                if(x['destCity'] is None):
                    if(x['description'] == 'Objeto saiu para entrega ao destinatário'):
                        event += '🥳🎊 '+ x['description'] + ' 🎊🥳\n🚛 De ' + x['type'] + ', ' + x['city'] + ' - ' + x['uf'] + '\n⏰ ' + x['dateTime'] + '\n\n'
                    elif(x['description'] == 'Objeto entregue ao destinatário'):
                        event += '🏁 '+ x['description'] + ' 🏁' + '\n⏱️ ' + x['dateTime'] + '\n\n'
                    else:
                        event += x['description'] + '\nNa ' + x['type'] + ', ' + x['city'] + ' - ' + x['uf'] + '\n' + x['dateTime'] + '\n\n'
                    #update.message.reply_markdown_v2(fr"{str}")
                else:
                    event += x['description'] + '\n🚚 De ' + x['type'] + ', ' + x['city'] + ' - ' + x['uf'] + '\n🚩 Para ' + x['destType'] + ', ' + x['destCity'] + ' - ' + x['destUf'] + '\n⏰ ' + x['dateTime'] + '\n\n'
            except:
                if(x['destCity'] is None):
                    event += x['description'] + '\nDo ' + x['city'] + ', ' + x['type']  + '\n' + x['dateTime'] + '\n\n'
                #update.message.reply_markdown_v2(fr"{str}")
                else:
                    event += x['description'] + '\n🚚 Do ' + x['city'] + ' - ' + x['type'] + '\n🚩 Para ' + x['destType'] + ', ' + x['destCity'] + ' - ' + x['destUf'] + '\n⏰ ' + x['dateTime'] + '\n\n'
        update.message.reply_text(fr"{event}",None)
        logger.info("CODIGO RASTREADO COM SUCESSO %s: %s", user.first_name, update.message.text)

    else:
        logger.error("CODIGO NÃO RASTREAVEL %s: %s", user.first_name, update.message.text)
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
            logger.error("updateOne FALHOU %s: %s", user.first_name, update.message.text)
            
            
    update.message.reply_text(fr"{text}")
    return ConversationHandler.END

def OpcListar(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("OPCAO DE LISTAR CODIGOS %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Lista de Codigos:',
        reply_markup=ReplyKeyboardRemove(),
    )
    data = []
    reply_keyboard = []
    jsonData = data_base.findOne("_id", user.id)
    if(jsonData is None):
        text="Lista vazia!"
        logger.error("LISTAR VAZIA %s: %s", user.first_name, update.message.text)

    else:
        text=""
        for x in jsonData["user_tracking_number"]:
            reply_keyboard.append([x])
            text += x + '\n'
    update.message.reply_text(
        fr"{text}",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )
    logger.info("LISTAR DE CODIGOS %s: %s", user.first_name, update.message.text)

    #return LISTAR
    
def OpcDeletar(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    jsonData = data_base.findOne("_id", user.id)
    reply_keyboard = []
    for x in jsonData["user_tracking_number"]:
            reply_keyboard.append([x])
    update.message.reply_text(
        'Por favor digite o Codigo de rastreio.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )
    return DELETAR

def deletaCodigo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = "Codigo deletado!"
    if(data_base.findOne("_id", user.id)):
        logger.info("OPCAO DE DELETAR CODIGO %s %s: %s", user.id, user.first_name, update.message.text)
        if(data_base.deleteOne(user.id, update.message.text)['modifiedCount'] == 0):
            logger.error("OPCAO DE DELETAR CODIGO %s %s: %s", user.id, user.first_name, update.message.text)
            text = "Não foi possivel deletar o codigo!"
    else:
        update.message.reply_text("Codigo Invalido.")
        logger.error("OPCAO DE DELETAR CODIGO %s %s: %s", user.id, user.first_name, update.message.text)
        text = "Não foi possivel deletar o codigo!"
    update.message.reply_text(fr"{text}", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END