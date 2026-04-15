from fastapi import FastAPI
import pyodbc

app = FastAPI()

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-NJ4MVFB;"
    "DATABASE=raw_data;"
    "UID=sa;"
    "PWD=333255533327777;"
)

def fetch_data(query):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    result = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return result

@app.get("/customers")
def get_customers():
    return {"data": fetch_data("SELECT * FROM customer")}

@app.get("/orders")
def get_orders():
    return {"data": fetch_data("SELECT * FROM [order]")}

@app.get("/order_details")
def get_order_details():
    return {"data": fetch_data("SELECT * FROM order_detail")}

@app.get("/products")
def get_products():
    return {"data": fetch_data("SELECT * FROM product")}

@app.get("/returned")
def get_returned_orders():
    return {"data": fetch_data("SELECT * FROM returned")}

@app.get("/shipping")
def get_shipping_info():
    return {"data": fetch_data("SELECT * FROM shipping")}