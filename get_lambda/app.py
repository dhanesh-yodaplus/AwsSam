import boto3
import os

import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
    response = s3.get_object(Bucket='my-sam-bucket', Key='get.txt')

    raw_bytes = response['Body'].read()

    try:
        content = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        content = raw_bytes.decode('utf-8', errors='replace')  # replaces bad characters with �

    print("File content:")
    print(content)
    return content


# LOCAL TEST
if __name__ == "__main__":
    test_event = {
        "bucket": "my-sam-bucket",
        "key": "get.txt"
    }
    result = lambda_handler(test_event, None)
    print("Returned:", result)
