import json
import base64

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        
        # Simple processing: Convert sentiment to uppercase
        data['sentiment'] = data['sentiment'].upper()
        
        print(f"Processed record: {json.dumps(data)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
