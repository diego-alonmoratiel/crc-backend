import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
table = dynamodb.Table("visitors-count-crc")
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)  
    raise TypeError

def lambda_handler(event, context):
    response = table.update_item(
    Key={
        'name': "visitors-count"
    },
    UpdateExpression="ADD nvisitors :increase",
    ExpressionAttributeValues={
        ':increase': 1
    },
    ReturnValues="UPDATED_NEW"
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response['Attributes'], default=decimal_default)
    }
