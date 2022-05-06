import requests
import json
import datetime
import locale
#from flask import Flask, request
from Object import Object
from Event import Event
#from waitress import serve

#app = Flask(__name__)

def initializeObject(data):
    #(cod,objectCode,expectedDate,category,description,imported, events):
    try:
        object = Object("200",data['objetos'][0]['codObjeto'],
            data['objetos'][0]['dtPrevista'],
            data['objetos'][0]['tipoPostal']['categoria'],
            data['objetos'][0]['tipoPostal']['descricao'],
            data['objetos'][0]['modalidade'],
            None
        )
    except:
        object = Object("200",data['objetos'][0]['codObjeto'],
            None,
            data['objetos'][0]['tipoPostal']['categoria'],
            data['objetos'][0]['tipoPostal']['descricao'],
            data['objetos'][0]['modalidade'],
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
    #(description,dateTime,city,uf,type,destCity, destUf, destType)
    i = 0
    for x in data['objetos'][0]['eventos']:
        #object.printList()
        #print(i,"\n")
        i=i+1
        formattedDate = datetime.datetime.strptime(x['dtHrCriado'],'%Y-%m-%dT%H:%M:%S')
        if(data['objetos'][0]['tipoPostal']['sigla'] == "LB" or data['objetos'][0]['tipoPostal']['sigla'] == "NX"):
            #print(x,"\n")
            if(x['codigo'] != "PO" and x['codigo'] != "OEC" and x['codigo'] != "BDE"and x['codigo'] != "PAR"):
                try:
                    object.addEvents(
                        x['descricao'],
                        formattedDate.strftime("%A, %d. %B %Y %I:%M%p").capitalize(),
                        x['unidade']['tipo'],
                        None,
                        x['unidade']['nome'],
                        x['unidadeDestino']['tipo'],
                        x['unidadeDestino']['endereco']['uf'],
                        x['unidadeDestino']['nome'])
                except:
                    object.addEvents(
                    x['descricao'],
                        formattedDate.strftime("%A, %d. %B %Y %I:%M%p").capitalize(),
                        x['unidade']['endereco']['cidade'],
                        x['unidade']['endereco']['uf'],
                        x['unidade']['tipo'],
                        x['unidadeDestino']['endereco']['cidade'],
                        x['unidadeDestino']['endereco']['uf'],
                        x['unidadeDestino']['tipo'])
                print("\n\neu sei que passou aqui")
            elif(x['codigo'] == "PAR"):
                #print("par?")
        #elif(data['objetos'][0]['modalidade'] == "V" and x['codigo'] == "PAR"):
                object.addEvents(
                    x['descricao'],
                    formattedDate.strftime("%A, %d. %B %Y %I:%M%p").capitalize(),
                    x['unidade']['endereco']['cidade'],
                    x['unidade']['endereco']['uf'],
                    x['unidade']['tipo'],
                    None,
                    None,
                    None)
            else:    
                #print("?????")
        #elif(data['objetos'][0]['modalidade'] == "V"):
                object.addEvents(
                    x['descricao'],
                    formattedDate.strftime("%A, %d. %B %Y %I:%M%p").capitalize(),
                    x['unidade']['tipo'],
                    None,
                    x['unidade']['nome'],
                    None,
                    None,
                    None)            
        else:
            #print("n faz sentido mas passei aqui")
            if(x['codigo'] != "PO" and x['codigo'] != "OEC" and x['codigo'] != "BDE"):
            #(data['objetos'][0]['modalidade'] != "V" and x['codigo'] != "PO" and x['codigo'] != "OEC" and x['codigo'] != "BDE"):
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

#@app.route("/rastrear", methods=["GET"])
def rastreio(id):
    # f = open("data.json",encoding='utf8')
    # data = json.load(f)
    # return data
    #id = request.args.get("id")
    locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
    data = getJsonRequest(id)
    try:
        object = initializeObject(data)
        addAllEvents(data, object)
        #object.events.invert()
        #object.printList()
        #exportJson(object)
        return json.dumps(object,ensure_ascii=False,default=lambda o: o.__dict__)
    except:
       return json.dumps({"cod":"404","mensagem":" SRO-019: Objeto inválido"},ensure_ascii=False,default=lambda o: o.__dict__)

#if __name__ == '__main__':
   # app.run()
    #serve(app, port=8080, host="0.0.0.0")