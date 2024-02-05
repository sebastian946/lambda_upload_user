import os
import boto3
import json
from botocore.exceptions import NoCredentialsError

s3_bucket = 'pruebatecnica123'

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No data provided'})
            }

        event_body = event['body']
        data = json.loads(event_body)

        video_content_base64 = data.get('video_content', '')
        
        if not video_content_base64:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No video content provided'})
            }

        video_content = video_content_base64.decode('base64')

        video_id = generate_unique_id()

        s3 = boto3.client('s3')

        s3_key = f'videos/{video_id}.mp4'
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=video_content)

        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'video_id': video_id})
        }

    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'AWS credentials not available'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_unique_id():
    import uuid
    return str(uuid.uuid4())
