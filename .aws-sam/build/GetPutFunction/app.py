import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    try:
        # Put new content
        s3.put_object(Bucket='my-sam-bucket', Key='putget.txt', Body='Hello from GetPut Lambda!')

        # Read it back
        obj = s3.get_object(Bucket='my-sam-bucket', Key='putget.txt')
        data = obj['Body'].read().decode('utf-8')

        return {
            'statusCode': 200,
            'body': f'[GetPut Lambda] Wrote and read: {data}'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
