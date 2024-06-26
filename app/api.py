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

# Fetch table name and resume ID from environment variables
table_name = os.getenv('TABLE_NAME')
resume_id = os.getenv('RESUME_ID', '1')

if not table_name:
    logger.error("TABLE_NAME environment variable is not set.")
    raise ValueError("TABLE_NAME environment variable is required")

table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    logger.info(f"Get resume request with event data: {json.dumps(event)}")

    try:
        # Fetch the item from DynamoDB
        response = table.get_item(Key={'id': resume_id})

        if 'Item' in response:
            logger.info(f"Resume found for id: {resume_id}")
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'], indent=2),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            logger.warning(f"No resume found for id: {resume_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Resume not found'}, indent=2),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    except ClientError as e:
        error_message = e.response['Error']['Message']
        logger.error(f"DynamoDB ClientError: {error_message}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'message': error_message}, indent=2),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'message': str(e)}, indent=2),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
