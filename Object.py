from Event import Event
from structlinks.DataStructures import LinkedList
class Object:
    def __init__(self,cod,objectCode,expectedDate,category,description,imported, events):
        self.cod = cod
        self.objectCode = objectCode
        self.expectedDate = expectedDate
        self.category = category
        self.description = description
        self.imported = imported
        self.events = []

    def addEvents(self,description,dateTime,city,uf,typee,destCity,destUf,destType):
        event = Event(description,dateTime,city,uf,typee,destCity,destUf,destType)
        self.events.append(event)

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
    