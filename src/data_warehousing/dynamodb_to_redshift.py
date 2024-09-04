import boto3
import os
import json
import time

def lambda_handler(event, context):
    try:
        # Connect to DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('SocialMediaSentiments')

        # Scan DynamoDB table
        response = table.scan()
        items = response['Items']
        print(f"Found {len(items)} items in DynamoDB")

        # Connect to Redshift Data API
        redshift_data = boto3.client('redshift-data')

        # Prepare batch insert SQL
        batch_size = 100
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]
            values = []
            for item in batch:
                values.append(f"('{item['Id']}', '{item['platform']}', '{item['user_id']}', '{item['message']}', '{item['sentiment']}', {item['timestamp']})")
            
            sql = f"""
            INSERT INTO social_media_sentiments (id, platform, user_id, message, sentiment, timestamp)
            VALUES {','.join(values)}
            """
            
            response = redshift_data.execute_statement(
                ClusterIdentifier=os.environ['REDSHIFT_CLUSTER_ID'],
                Database=os.environ['REDSHIFT_DB_NAME'],
                DbUser=os.environ['REDSHIFT_USERNAME'],
                Sql=sql
            )

            # Wait for the query to complete
            query_id = response['Id']
            while True:
                status = redshift_data.describe_statement(Id=query_id)['Status']
                if status in ['FINISHED', 'FAILED', 'ABORTED']:
                    break
                time.sleep(0.5)

            if status != 'FINISHED':
                raise Exception(f"Query failed with status: {status}")

            print(f"Inserted batch of {len(batch)} items into Redshift")

        print(f"Inserted all {len(items)} items into Redshift")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully inserted {len(items)} items into Redshift')
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }
