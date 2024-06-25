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


def lambda_handler(event, context):
    try:
        # Get the resume id from the query parameters
        resume_id = event.get('queryStringParameters', {}).get('id')

        if not resume_id or not isinstance(resume_id, str):
            raise ValueError("Invalid id parameter")

        # Fetch the item from DynamoDB
        response = table.get_item(Key={'id': resume_id})

        logger.info(f"Get resume request with event data: {
                    event}")  # Log the event data

        if 'Item' in response:
            logger.info(f"Resume found for id: {resume_id}")
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item']),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            logger.warning(f"No resume found for id: {resume_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Resume not found'}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except ClientError as e:
        # Add specific exception handling here if needed
        logger.error(f"ClientError: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
