import requests
import json
a = open("apiKey.txt","r")
apiKey = a.read()
a.close()
headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': apiKey
    }

def insertOne(userId, userName, userTrackingNumber):
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/insertOne"
    payload = json.dumps({
        "dataSource": "RochaESilvaDB",
        "database": "Distribuidora",
        "collection": "dboUsuario",
        "document": {
            "_id": userId, 
            "user_name": userName,
            "user_tracking_number": userTrackingNumber,
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def findOne(field, value):
    url = "https://data.mongodb-api.com/app/data-guzuj/endpoint/data/beta/action/find"

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
    try:
        return resp["documents"][0]
    except:
        return None

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
