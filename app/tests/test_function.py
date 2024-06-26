import unittest
from unittest.mock import patch, MagicMock
import json
from app.api import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    @patch.dict(lambda_handler.os.environ, {'TABLE_NAME': 'test-table', 'RESUME_ID': '1'})
    @patch('boto3.resource')
    def test_lambda_handler_success(self, mock_dynamodb_resource):
        # Mock the DynamoDB Table and its get_item method
        mock_table = MagicMock()
        mock_table.get_item.return_value = {
            'Item': {'id': '1', 'name': 'Test Resume'}}
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Mock event and context
        event = {}
        context = {}

        # Call the lambda_handler function
        response = lambda_handler.lambda_handler(event, context)

        # Validate the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {
                         'id': '1', 'name': 'Test Resume'})

    @patch.dict(lambda_handler.os.environ, {'TABLE_NAME': 'test-table', 'RESUME_ID': '1'})
    @patch('boto3.resource')
    def test_lambda_handler_resume_not_found(self, mock_dynamodb_resource):
        # Mock the DynamoDB Table and its get_item method
        mock_table = MagicMock()
        mock_table.get_item.return_value = {}
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Mock event and context
        event = {}
        context = {}

        # Call the lambda_handler function
        response = lambda_handler.lambda_handler(event, context)

        # Validate the response
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(json.loads(response['body']), {
                         'error': 'Resume not found'})

    @patch.dict(lambda_handler.os.environ, {'TABLE_NAME': 'test-table', 'RESUME_ID': '1'})
    @patch('boto3.resource')
    def test_lambda_handler_internal_server_error(self, mock_dynamodb_resource):
        # Mock the DynamoDB Table to raise an exception
        mock_table = MagicMock()
        mock_table.get_item.side_effect = Exception("Test exception")
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Mock event and context
        event = {}
        context = {}

        # Call the lambda_handler function
        response = lambda_handler.lambda_handler(event, context)

        # Validate the response
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', json.loads(response['body']))
        self.assertIn('message', json.loads(response['body']))


if __name__ == '__main__':
    unittest.main()
