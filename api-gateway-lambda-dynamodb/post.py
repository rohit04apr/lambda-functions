import json
import boto3
import botocore

dynamodb = boto3.resource('dynamodb')
table_name = 'data'
table = dynamodb.Table(table_name)
client = boto3.client('dynamodb')


def lambda_handler(event, context):

    try:
        checkTable(table_name)
        table.put_item(Item=event)

        return {'statusCode': 200, 'body': 'data inserted sucessfully'}
    except botocore.exceptions.ClientError as error:
        print(error)


def checkTable(table_name):
    try:
        response = client.list_tables()

        if table_name in response['TableNames']:
            table_found = True
        else:
            table_found = False

            response = client.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    },
                ],

                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            table.meta.client.get_waiter(
                'table_exists').wait(TableName=table_name)

    except botocore.exceptions.ClientError as error:
        print(error)

    return table_found

