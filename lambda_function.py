import requests
import boto3
import os
import json
import io
import csv 
import json


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    base_url = os.environ['BASE_API_URL']
    # Define your endpoints here
    tables = ["products", "customers", "orders","order_details","returned","shipping"]
    bucket = os.environ['BUCKET_NAME']
    
    results = []

    for table in tables:
        try:
            # 1. Request data for specific table
            response = requests.get(f"{base_url}/{table}", timeout=30)
            response.raise_for_status()
            data = response.json()
            

             # Ensure data is a list of dictionaries
            if not isinstance(data, dict) or len(data) == 0:
                raise ValueError("API did not return a list of records")

            # # Convert JSON to CSV
            # output = io.StringIO()
            # writer = csv.DictWriter(output, fieldnames=data[0].keys())
            # writer.writeheader()
            # writer.writerows(data)


            #2. Upload to S3 using the table name in the path
            s3.put_object(
                Bucket=bucket,
                Key=f'raw_data/{table}/{table}_extract.json',
                Body=json.dumps(data)
            )
            # Upload CSV to S3
            # s3.put_object(
            #     Bucket=bucket,
            #     Key=f'raw_data/{table}/{table}_extract.csv',
            #     Body=output.getvalue(),
            #     ContentType='text/csv'
            # )

            results.append(f"Successfully processed {table}")
            
        except Exception as e:
            results.append(f"Failed {table}: {str(e)}")
    
    return {
        "status": "completed",
        "details": results
    }