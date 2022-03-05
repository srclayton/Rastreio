import requests
import json
import structlinks
import datetime
import locale
from flask import Flask, request
from Object import Object
from Event import Event
app = Flask("Rastreio")

def initializeObject(data):
    try:
        object = Object("200",data['objetos'][0]['codObjeto'],
            None,
            data['objetos'][0]['tipoPostal']['categoria'],
            data['objetos'][0]['tipoPostal']['descricao'],
            None
        )
    except:
        object = Object(200,data['objetos'][0]['codObjeto'],
            data['objetos'][0]['dtPrevista'],
            data['objetos'][0]['tipoPostal']['categoria'],
            data['objetos'][0]['tipoPostal']['descricao'],
            None
        )
    return object



def getJsonRequest(key):
    url = "https://proxyapp.correios.com.br/v1/sro-rastro/"
    url += key
    r = requests.get(url)
    data = r.json()
    return data

def addAllEvents(data, object):
    for x in data['objetos'][0]['eventos']:
        formattedDate = datetime.datetime.strptime(x['dtHrCriado'],'%Y-%m-%dT%H:%M:%S')
        if(x['codigo'] != "PO" and x['codigo'] != "OEC" and x['codigo'] != "BDE"):
            object.addEvents(
                x['descricao'],
                formattedDate.strftime("%A, %d. %B %Y %I:%M%p").capitalize(),
                x['unidade']['endereco']['cidade'],
                x['unidade']['endereco']['uf'],
                x['unidade']['tipo'],
                x['unidadeDestino']['endereco']['cidade'],
                x['unidadeDestino']['endereco']['uf'],
                x['unidadeDestino']['tipo'])
        else:
            object.addEvents(
                x['descricao'],
                formattedDate.strftime("%A, %d. %B %Y %I:%M%p").capitalize(),
                x['unidade']['endereco']['cidade'],
                x['unidade']['endereco']['uf'],
                x['unidade']['tipo'],
                None,
                None,
                None)

def exportJson(object):
    with open('data.json', 'w',encoding='utf8') as f:
        json.dump(object,f,ensure_ascii=False,default=lambda o: o.__dict__)


@app.route("/rastrear", methods=["GET"])
def main():
    # f = open("data.json",encoding='utf8')
    # data = json.load(f)
    # return data
    id = request.args.get("id")
    locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
    data = getJsonRequest(id)
    try:
        object = initializeObject(data)
        addAllEvents(data, object)
        #object.events.invert()
        object.printList()
        #exportJson(object)
        return json.dumps(object,ensure_ascii=False,default=lambda o: o.__dict__)
    except:
        return {"cod":"404","mensagem":" SRO-019: Objeto inválido"}

app.run()
