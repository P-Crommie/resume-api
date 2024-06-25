import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource outside the handler to reuse it
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('TABLE_NAME')
table = dynamodb.Table(table_name)

RESUME_ID = "1"


def lambda_handler(event, context):
    try:
        # Fetch the item from DynamoDB
        response = table.get_item(Key={'id': RESUME_ID})

        logger.info(f"Get resume request with event data: {
                    event}")  # Log the event data

        if 'Item' in response:
            logger.info(f"Resume found for id: {RESUME_ID}")
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'], indent=2),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            logger.warning(f"No resume found for id: {RESUME_ID}")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Resume not found'}, indent=2),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    except ClientError as e:
        # Add specific exception handling here if needed
        logger.error(f"ClientError: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'}, indent=2),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'}, indent=2),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
