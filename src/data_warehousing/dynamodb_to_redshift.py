import boto3
import psycopg2
import os

def lambda_handler(event, context):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SocialMediaSentiments')

    # Scan DynamoDB table
    response = table.scan()
    items = response['Items']

    # Connect to Redshift
    conn = psycopg2.connect(
        dbname=os.environ['REDSHIFT_DB_NAME'],
        user=os.environ['REDSHIFT_USERNAME'],
        password=os.environ['REDSHIFT_PASSWORD'],
        host=os.environ['REDSHIFT_HOST'],
        port=os.environ['REDSHIFT_PORT']
    )
    cur = conn.cursor()

    # Insert items into Redshift
    for item in items:
        cur.execute("""
            INSERT INTO social_media_sentiments (id, platform, user_id, message, sentiment, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (item['Id'], item['platform'], item['user_id'], item['message'], item['sentiment'], item['timestamp']))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': f'Inserted {len(items)} items into Redshift'
    }
