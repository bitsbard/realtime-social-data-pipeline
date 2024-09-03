import json
import base64
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SocialMediaSentiments')

def lambda_handler(event, context):
    for record in event['Records']:
        # Decode and load the Kinesis data
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        
        # Generate a unique ID for the DynamoDB item
        data['Id'] = str(uuid.uuid4())
        
        # Write the item to DynamoDB
        table.put_item(Item=data)
        
        print(f"Processed and stored record: {json.dumps(data)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
