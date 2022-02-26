class Object:
    def __init__(self,cod,objectCode,expectedDate,category,description, events):
        self.cod = cod
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
    