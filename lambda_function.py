# import requests
# import boto3
# import os
# import json
# import io
# import csv 
# import json


# def lambda_handler(event, context):
#     s3 = boto3.client('s3')
#     base_url = os.environ['BASE_API_URL']
#     # Define your endpoints here
#     tables = ["products", "customers", "orders","order_details","returned","shipping"]
#     bucket = os.environ['BUCKET_NAME']
    
#     results = []

#     for table in tables:
#         try:
#             # 1. Request data for specific table
#             response = requests.get(f"{base_url}/{table}", timeout=30)
#             response.raise_for_status()
#             data = response.json()
            

#              # Ensure data is a list of dictionaries
#             if not isinstance(data, dict) or len(data) == 0:
#                 raise ValueError("API did not return a list of records")


#             #2. Upload to S3 using the table name in the path
#             s3.put_object(
#                 Bucket=bucket,
#                 Key=f'raw_data/{table}/{table}_extract.json',
#                 Body=json.dumps(data)
#             )

#             results.append(f"Successfully processed {table}")
            
#         except Exception as e:
#             results.append(f"Failed {table}: {str(e)}")
    
#     return {
#         "status": "completed",
#         "details": results
#     }

import requests
import boto3
import os
import json
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    base_url = os.environ['BASE_API_URL']
    bucket = os.environ['BUCKET_NAME']
    
    tables = ["products", "customers", "orders", "order_details", "returned", "shipping"]
    
    # Get current timestamp for partitioning
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    ts = now.strftime('%H%M%S')

    results = []

    for table in tables:
        try:
            
            with requests.get(f"{base_url}/{table}", stream=True, timeout=60) as r:
                r.raise_for_status()
                
                s3_key = f"raw_data/{table}/year={year}/month={month}/day={day}/{table}_{ts}.json"
                
                s3.put_object(
                    Bucket=bucket,
                    Key=s3_key,
                    Body=r.content 
                )
                
            results.append(f"Successfully saved {table} to {s3_key}")
            
        except Exception as e:
            results.append(f"Failed {table}: {str(e)}")
    
    return {
        "status": "completed",
        "timestamp": now.isoformat(),
        "details": results
    }