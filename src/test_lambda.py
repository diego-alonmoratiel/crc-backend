import json
import pytest
from moto import mock_aws
import boto3
from decimal import Decimal

# Import lambda for testing
import lambda_function 


@mock_aws
def test_lambda_handler_updates_visitors():
    os.environ['AWS_DEFAULT_REGION'] = 'eu-north-1'
    # 1. Create a simulation of DynamoDB table
    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
    table = dynamodb.create_table(
        TableName="visitors-count-crc",
        KeySchema=[
            {"AttributeName": "name", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "name", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    # Insert initial value
    table.put_item(Item={"name": "visitors-count", "nvisitors": 0})

    # 2. Execute Lambda
    event = {}
    context = {}
    response = lambda_function.lambda_handler(event, context)

    # 3. Validate exit
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert "nvisitors" in body
    assert isinstance(body["nvisitors"], int)
    assert body["nvisitors"] == 1  
