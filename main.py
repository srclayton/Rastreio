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
        print("\nCategoria de entrega:", self.category,
        "\nDescrição:", self.description,
        "\nData prevista para entrega:", self.expectedDate, "\n\n"
        )
        for i in self.events:
            try:
                i.printList()
            except:
                i[0].printList()



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
        if(self.destCity is None or self.destUf is None or self.destType is None):
            print(self.description,
            "\nPela" ,self.type,
            ",",self.city,
            "-",self.uf,
            "\n",self.dateTime, "\n------------------------------------------------"
            )
        else:
            print(self.description,
            "\nde",self.type,
            ",",self.city,
            "-",self.uf,
            "\npara",self.destType,
            ",",self.destCity ,
            "-",self.destUf,
            "\n",self.dateTime,"\n------------------------------------------------")
def initializeObject(data):
    try:
        object = Object(data['objetos'][0]['codObjeto'],
            None,
            data['objetos'][0]['tipoPostal']['categoria'],
            data['objetos'][0]['tipoPostal']['descricao'],
            None
        )
    except:
        object = Object(data['objetos'][0]['codObjeto'],
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
    data = getJsonRequest("QI608436875BR")
    object = initializeObject(data)
    addAllEvents(data, object)
    object.printList()

main()
