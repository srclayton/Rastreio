import requests
import json
import structlinks
from structlinks.DataStructures import LinkedList



class Object:
    def __init__(self,objectCode,expectedDate,category,description, events):
        self.objectCode = objectCode
        self.expectedDate = expectedDate
        self.category = category
        self.description = description
        self.events = events

    def addEvents(self,description,dateTime,city,uf,type,destCity,destUf,destType):
        event = Event(description,dateTime,city,uf,type,destCity,destUf,destType)
        if(self.events is None):
            self.events = LinkedList([event])
        else:
            self.events.append([event])
    def printList(self):
        print(self.expectedDate,
        self.category,
        self.description ,
        self.events)

class Event:
    def __init__(self,description,dateTime,city,uf,type,destCity, destUf, destType):
        self.description = description
        self.dateTime = dateTime
        self.city = city
        self.uf = uf
        self.type = type
        self.destCity = destCity
        self.destUf = destUf
        self.destType = destType

    def printList(self):
        print(self.description,
        self.dateTime,
        self.city,
        self.uf,
        self.type,
        self.destCity ,
        self.destUf,
        self.destType)

def initializeObject(data, object):
    object = Object(data['objetos'][0]['codObjeto'],
        data['objetos'][0]['dtPrevista'],
        data['objetos'][0]['tipoPostal']['categoria'],
        data['objetos'][0]['tipoPostal']['descricao'],
        None
    )




def getJsonRequest(key):
    url = "https://proxyapp.correios.com.br/v1/sro-rastro/"
    url += key
    r = requests.get(url)
    data = r.json()
    return data

def addAllEvents(data, object):
    for x in data['objetos'][0]['eventos']:
        if(x['codigo'] != "PO" and x['codigo'] != "OEC" and x['codigo'] != "BDE"):
            object.addEvents(
                x['descricao'],
                x['dtHrCriado'],
                x['unidade']['endereco']['cidade'],
                x['unidade']['endereco']['uf'],
                x['unidade']['tipo'],
                x['unidadeDestino']['endereco']['cidade'],
                x['unidadeDestino']['endereco']['uf'],
                x['unidadeDestino']['tipo'])
        else:
            object.addEvents(
                x['descricao'],
                x['dtHrCriado'],
                x['unidade']['endereco']['cidade'],
                x['unidade']['endereco']['uf'],
                x['unidade']['tipo'],
                None,
                None,
                None)


def main():
    data = getJsonRequest("QC144617315BR")
    object = None
    initializeObject(data,object)
    addAllEvents(data, object)
    object.printList()



main()
