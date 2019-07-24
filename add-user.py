import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("users")

table.put_item(
   Item={
        'username': 'phuc',
        'first_name': 'Phuc',
        'last_name': 'Nguyen',
        'age': 22,
        'account_type': 'admin',
    }
)