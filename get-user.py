import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("user")

response = table.get_item(
    Key = {
        'username' : 'Khanh',
        'last_name' : 'Dang'
    }
)
item = response['Item']
print(item)