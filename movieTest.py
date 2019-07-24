import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

#DELETE
# event = {
#     "action":"delete",
#     "key":{
#         "year": 2013,
#         "title":"The Family"
#     }
# }

# CREATE
# event = {
#     "action" : "create",
#     "item" : {
#         'year': 2019,
#         'title': "Avengers: End Game",
#         'info': {
#             'plot':"Thanos",
#             'rating': 5
#             }
#     }
# }

# GET
# event = {
#     "action":"get",
#     "key":{
#         "year": 2013,
#         "title":"Gravity"
#     }
# }

# UPDATE
# event = {
# "action":"update",
# "key":{
#     "year": 2019,
#     "title":"Avengers: End Game"
# },
# 'updateExpression' : "set info.rating = :r, info.plot=:p, info.actors=:a",
# 'expressionAttributeValues' : {
#     ':r': 7,
#     ':p': "Everything happens all at once.",
#     ':a': ["Larry", "Moe", "Curly"]
# }
# }

#GET ALL
# event = {
#     "action":"read",
#     "key":{
#         "year": 2013,
#         "title":"Gravity"
#     }
# }

event = {
    "action":"read",
}

    

def lambda_handler(event, context):
    
    action = event.get("action")
    dynamodb = boto3.resource("dynamodb")  
    table = dynamodb.Table("Movies")    
    
    if action == "delete":
        deleteResult = delete_movie(event, table)
        print(deleteResult)
        return(deleteResult)

    elif action == "create":
        insertResult = insert_movie(event, table)
        print(insertResult)
        return(insertResult)

    elif action == "read":
        readResult = read_movie(event, table)
        print(readResult)
        return readResult
    elif action == "update":
        updateResult = update_movie(event, table)
        print(updateResult)
        return(updateResult)

def delete_movie(event, table):
    try:
        response = table.delete_item(
            Key = event['key']
        )
        return response
    except KeyError :
        return False
    
def insert_movie(event, table):
    response = table.put_item(
        Item = event['item']
    )
    return response

def read_movie(event, table):
    if event.get('key') is None:
       response = table.scan()
    else:
        response = table.get_item(
            Key = event['key']
        )
    return response

def update_movie(event, table):
    response = table.update_item(
        Key = event['key'],
        UpdateExpression = event['updateExpression'],
        ExpressionAttributeValues = event['expressionAttributeValues'],
        ReturnValues = "UPDATED_NEW"
    )
    return response

lambda_handler(event, None)