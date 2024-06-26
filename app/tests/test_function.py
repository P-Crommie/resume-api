import os
import pytest
from unittest.mock import patch, MagicMock
import json
from api import lambda_handler


@pytest.fixture
def mock_environment():
    with patch.dict(os.environ, {
        'TABLE_NAME': 'test-table',
        'RESUME_ID': '1',
        'AWS_DEFAULT_REGION': 'eu-west-1'  # Set your desired AWS region
    }):
        yield


@pytest.fixture
def mock_boto3_session():
    with patch('boto3.Session') as MockSession:
        MockSession.return_value.get_credentials.return_value.access_key = 'fake_access_key'
        MockSession.return_value.get_credentials.return_value.secret_key = 'fake_secret_key'
        MockSession.return_value.get_credentials.return_value.token = None
        yield MockSession


@patch('boto3.resource')
def test_lambda_handler_success(mock_boto3_resource, mock_environment, mock_boto3_session):
    # Mock DynamoDB Table and its get_item method
    mock_table = MagicMock()
    mock_table.get_item.return_value = {
        'Item': {'id': '1', 'name': 'Test Resume'}
    }
    mock_boto3_resource.return_value.Table.return_value = mock_table

    # Mock event and context
    event = {}
    context = {}

    # Call the lambda_handler function
    response = lambda_handler(event, context)

    # Validate the response
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'id': '1', 'name': 'Test Resume'}


@patch('boto3.resource')
def test_lambda_handler_resume_not_found(mock_boto3_resource, mock_environment, mock_boto3_session):
    # Mock DynamoDB Table and its get_item method to return no item
    mock_table = MagicMock()
    mock_table.get_item.return_value = {}
    mock_boto3_resource.return_value.Table.return_value = mock_table

    # Mock event and context
    event = {}
    context = {}

    # Call the lambda_handler function
    response = lambda_handler(event, context)

    # Validate the response
    assert response['statusCode'] == 404
    assert json.loads(response['body']) == {'error': 'Resume not found'}


@patch('boto3.resource')
def test_lambda_handler_internal_server_error(mock_boto3_resource, mock_environment, mock_boto3_session):
    # Mock DynamoDB Table to raise an exception
    mock_table = MagicMock()
    mock_table.get_item.side_effect = Exception("Test exception")
    mock_boto3_resource.return_value.Table.return_value = mock_table

    # Mock event and context
    event = {}
    context = {}

    # Call the lambda_handler function
    response = lambda_handler(event, context)

    # Validate the response
    assert response['statusCode'] == 500
    assert 'error' in json.loads(response['body'])
    assert 'message' in json.loads(response['body'])
