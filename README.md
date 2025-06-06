Lambda + S3 Integration (LocalStack + AWS SAM)

This project demonstrates the use of AWS SAM with LocalStack to simulate two Lambda functions:

GetOnlyFunction: Reads an object from S3.

GetPutFunction: Writes to and then reads from S3.

📁 Project Structure

sam/
├── get_lambda/
│   └── app.py              # Lambda that reads `get.txt` from S3
├── put_get_lambda/
│   └── app.py              # Lambda that writes and reads `putget.txt`
├── get.txt                 # File used to simulate reading
├── template.yaml           # SAM template for both functions and S3

⚙️ Setup

1. Create virtual environment & install boto3

python -m venv .venv
.venv\Scripts\activate
pip install boto3

2. Write Lambda logic

get_lambda/app.py reads get.txt from S3.

put_get_lambda/app.py writes putget.txt and reads it back.

3. Define SAM Template (template.yaml)

Includes:

S3 Bucket

Two Lambda functions

IAM permissions (read-only for one, get/put for another)

4. Package & Deploy with LocalStack

Ensure LocalStack is running and configured:

$env:AWS_ACCESS_KEY_ID="test"
$env:AWS_SECRET_ACCESS_KEY="test"
$env:AWS_DEFAULT_REGION="us-east-1"
$env:AWS_ENDPOINT_URL_S3="http://localhost:4566"

a. Create & upload deployment artifacts

Compress-Archive -Path .\get_lambda\* -DestinationPath get-lambda.zip
Compress-Archive -Path .\put_get_lambda\* -DestinationPath put-get-lambda.zip

aws --endpoint-url=http://localhost:4566 s3 mb s3://my-sam-bucket
aws --endpoint-url=http://localhost:4566 s3 cp get-lambda.zip s3://my-sam-bucket/
aws --endpoint-url=http://localhost:4566 s3 cp put-get-lambda.zip s3://my-sam-bucket/

b. Update template.yaml CodeUri to point to S3 ZIPs

CodeUri: s3://my-sam-bucket/get-lambda.zip
# and
CodeUri: s3://my-sam-bucket/put-get-lambda.zip

c. Deploy the stack

aws --endpoint-url=http://localhost:4566 cloudformation deploy \
  --template-file template.yaml \
  --stack-name lambda-s3-demo \
  --capabilities CAPABILITY_IAM \
  --region us-east-1

🧪 Test the Lambdas Locally

Upload test data for GetOnlyFunction

echo "This is test data for GetOnlyFunction" > get.txt
aws --endpoint-url=http://localhost:4566 s3 cp get.txt s3://my-sam-bucket/get.txt

Invoke GetOnly Lambda

aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name GetOnlyFunction \
  response-get.json

type response-get.json

Invoke GetPut Lambda

aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name GetPutFunction \
  response-putget.json

type response-putget.json

✅ Output Example

PutGet Lambda Output:

{
  "statusCode": 200,
  "body": "[GetPut Lambda] Wrote and read: Hello from GetPut Lambda!"
}

GetOnly Lambda Output:

{
  "statusCode": 200,
  "body": "Read from S3: This is test data for GetOnlyFunction"
}
