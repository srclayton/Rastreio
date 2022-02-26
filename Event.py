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
            "\n",self.dateTime,"\n------------------------------------------------"
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