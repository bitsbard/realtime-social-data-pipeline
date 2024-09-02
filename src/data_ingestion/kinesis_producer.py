import boto3
import json
import random
import time

# Initialize Kinesis client
kinesis = boto3.client('kinesis')

# Function to generate mock social media data
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

# Main loop to continuously produce data
while True:
    data = generate_data()
    response = kinesis.put_record(
        StreamName='social-media-stream',
        Data=json.dumps(data),
        PartitionKey=str(data['user_id'])
    )
    print(f"Put record in stream: {response['SequenceNumber']}")
    time.sleep(1)  # Wait for 1 second before sending the next record
