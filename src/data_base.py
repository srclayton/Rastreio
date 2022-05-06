import requests
import json
a = open("C:\\Users\\pcc\\Rastreio\\keys\\mongodbKey.txt","r")
apiKey = a.read()
a.close()
headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': apiKey
    }
url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/"

def insertOne(userId, userName, userTrackingNumber):
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/insertOne"
    payload = json.dumps({
        "dataSource": "RochaESilvaDB",
        "database": "Distribuidora",
        "collection": "dboUsuario",
        "document": {
            "_id": userId, 
            "user_name": userName,
            "user_tracking_number": [userTrackingNumber],
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)

def findOne(field, value):
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/findOne"
    
    if(field == "user_tracking_number"):
        payload = json.dumps({
            "collection": "dboUsuario",
            "database": "Distribuidora",
            "dataSource": "RochaESilvaDB",
            "filter": {
                "_id":value[1],
                field: value[0]
            }
        })
    else:    
        payload = json.dumps({
            "collection": "dboUsuario",
            "database": "Distribuidora",
            "dataSource": "RochaESilvaDB",
            "filter": {
                field: value
            }
        })
    response = requests.request("POST", url, headers=headers, data=payload)
    resp = response.json()
    if(resp["document"] is None):
        return None
    else:
        return resp["document"]

def updateOne(userId: int, userTrackingNumber: int):
    jsonUpdate = findOne("_id",userId)
    jsonUpdate["user_tracking_number"].append(userTrackingNumber)
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/updateOne"

    payload = json.dumps({
    "collection": "dboUsuario",
    "database": "Distribuidora",
    "dataSource": "RochaESilvaDB",
    "filter": {"_id": userId},
    "update": {
          "$set": {
              "user_tracking_number": jsonUpdate["user_tracking_number"],
          }
      }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    resp = response.json()    
    return resp

def deleteOne(userId: int, userTrackingNumber:int):
    jsonUpdate = findOne("_id",userId)
    if(jsonUpdate is None):
        return False
    i = 0
    for x in jsonUpdate["user_tracking_number"]:
         if(x == userTrackingNumber):
            del(jsonUpdate["user_tracking_number"][i])
         i += 1
    print(jsonUpdate["user_tracking_number"])
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/updateOne"

    payload = json.dumps({
    "collection": "dboUsuario",
    "database": "Distribuidora",
    "dataSource": "RochaESilvaDB",
    "filter": {"_id": userId},
    "update": {
          "$set": {
              "user_tracking_number": jsonUpdate["user_tracking_number"],
          }
      }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    resp = response.json()   
    print(resp) 
    return resp

def insertLog(id, userName, content):
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/insertOne"
    payload = json.dumps({
        "dataSource": "RochaESilvaDB",
        "database": "Distribuidora",
        "collection": "dboLogs",
        "document": {
            "_id": id, 
            "user_name": userName,
            "log":content,
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)