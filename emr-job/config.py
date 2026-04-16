RAW_BASE_PATH = "s3://my-etl-bucket-4312345/raw_data"

SILVER_BASE_PATH = "s3://my-etl-bucket-4312345/silver_tables"

TABLE_PATHS = {
    "customer": f"{SILVER_BASE_PATH}/dim_customer",
    "product": f"{SILVER_BASE_PATH}/dim_product",
    "location": f"{SILVER_BASE_PATH}/dim_location",
    "order_profile": f"{SILVER_BASE_PATH}/dim_order_profile",
    "fact_orders": f"{SILVER_BASE_PATH}/fact_orders"
}