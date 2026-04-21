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
    failed=[]
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
            failed.append(table)
    
    # If any table failed, raise an exception
    if failed:
        raise Exception(f"Data extraction failed for tables: {', '.join(failed)}")
    
    return {
        "status": "completed",
        "timestamp": now.isoformat(),
        "details": results
    }