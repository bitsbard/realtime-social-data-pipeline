import boto3
import json
import random
import time

def generate_data():
    platforms = ['Twitter', 'Facebook', 'Instagram']
    sentiments = ['positive', 'negative', 'neutral']
    return {
        'platform': random.choice(platforms),
        'user_id': f'user_{random.randint(1, 1000)}',
        'message': f'This is a test message {random.randint(1, 1000)}',
        'sentiment': random.choice(sentiments),
        'timestamp': int(time.time())
    }

def lambda_handler(event, context):
    kinesis = boto3.client('kinesis')
    
    try:
        data = generate_data()
        response = kinesis.put_record(
            StreamName='social-media-stream',
            Data=json.dumps(data),
            PartitionKey=str(data['user_id'])
        )
        print(f"Put record in stream: {response['SequenceNumber']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data sent to Kinesis successfully'),
            'kinesisResponse': response
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending data to Kinesis: {str(e)}')
        }

# For testing locally
if __name__ == "__main__":
    while True:
        lambda_handler({}, None)
        time.sleep(1)
