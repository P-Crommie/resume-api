import unittest
from unittest.mock import patch, MagicMock
from moto import mock_dynamodb2
import boto3
import json
import os

# Import the lambda function from api.py
from api import lambda_handler, table_name, resume_id

@mock_dynamodb2
class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        # Set environment variables
        os.environ['TABLE_NAME'] = 'test_table'
        os.environ['RESUME_ID'] = '1'

        # Create a mock DynamoDB table
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.create_table(
            TableName=os.getenv('TABLE_NAME'),
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        self.table.wait_until_exists()

        # Add a mock item to the table
        self.table.put_item(Item={'id': '1', 'name': 'John Doe', 'email': 'johndoe@example.com'})

    def tearDown(self):
        self.table.delete()
        self.dynamodb = None

    def test_lambda_handler_success(self):
        event = {}
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], '1')
        self.assertEqual(body['name'], 'John Doe')
        self.assertEqual(body['email'], 'johndoe@example.com')

    def test_lambda_handler_not_found(self):
        os.environ['RESUME_ID'] = '2'
        event = {}
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 404)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Resume not found')

    @patch('api.table.get_item')
    def test_lambda_handler_dynamodb_client_error(self, mock_get_item):
        mock_get_item.side_effect = boto3.client('dynamodb').exceptions.ProvisionedThroughputExceededException(
            {'Error': {'Message': 'Throughput exceeded'}},
            'GetItem'
        )
        event = {}
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Internal server error')
        self.assertEqual(body['message'], 'Throughput exceeded')

    @patch('api.table.get_item', side_effect=Exception('Unknown error'))
    def test_lambda_handler_general_exception(self, mock_get_item):
        event = {}
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Internal server error')
        self.assertEqual(body['message'], 'Unknown error')

if __name__ == '__main__':
    unittest.main()
