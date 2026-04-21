import os

from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict
from contextlib import asynccontextmanager
import pyodbc
from dotenv import load_dotenv


# Load variables from a .env file
load_dotenv()


app = FastAPI()
DATABASE_URL = os.getenv("DB_CONNECTION_STRING")

def get_db_connection():
    """
    Dependency that handles connection lifecycle.
    
    """
    conn = None
    try:
        conn = pyodbc.connect(DATABASE_URL)
        yield conn
    except Exception as e:
        # In production, log this error to a file/service
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if conn:
            conn.close()

def run_query(conn, query: str) -> List[Dict]:
    """
    Helper to execute and format results.
    Args:
    - conn: Active database connection
    - query: SQL query string
    Returns:
    - List of dictionaries representing rows
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@app.get("/customers")
def get_customers(db=Depends(get_db_connection)):
    # Use explicit columns instead of SELECT * for better performance/security
    data = run_query(db, "SELECT * FROM customer")
    return {"data": data}



@app.get("/orders")
def get_orders(db=Depends(get_db_connection)):
    data = run_query(db, "SELECT * FROM [order]")
    return {"data": data}

@app.get("/order_details")
def get_order_details(db=Depends(get_db_connection)):
    data = run_query(db, "SELECT * FROM order_detail")
    return {"data": data}

@app.get("/products")
def get_products(db=Depends(get_db_connection)):
    data = run_query(db, "SELECT * FROM product")
    return {"data": data}

@app.get("/returned")
def get_returned_orders(db=Depends(get_db_connection)):
    data = run_query(db, "SELECT * FROM returned")
    return {"data": data}

@app.get("/shipping")
def get_shipping_info(db=Depends(get_db_connection)):
    data = run_query(db, "SELECT * FROM shipping")
    return {"data": data}



