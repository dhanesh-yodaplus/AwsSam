# get_lambda/app.py

import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    try:
        obj = s3.get_object(Bucket='my-sam-bucket', Key='get.txt')
        data = obj['Body'].read().decode('utf-8')
        return {
            'statusCode': 200,
            'body': f'Read from S3: {data}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
