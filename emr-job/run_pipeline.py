import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
# Core utilities
from core.reader import read_json_data
from core.writer import write_delta_scd1, write_fact_table

# Dimension builders
from transforms.product_dim import build_product_dim
from transforms.location_dim import build_location_dim
from transforms.order_profile_dim import build_order_profile_dim
from transforms.fact_orders import build_order_fact
from transforms.customer_dim import build_customer_dim

from config import TABLE_PATHS, RAW_BASE_PATH, SILVER_BASE_PATH

logging.basicConfig(level=logging.INFO)

# initialize Spark session
spark = SparkSession.builder \
    .appName("etl_pipeline") \
    .getOrCreate()

# accept date argument
if len(sys.argv) < 2:
    logging.error("ERROR: Missing date argument!")
    print("ERROR: Missing date argument!")
    sys.exit(1)

job_date = sys.argv[1]
logging.info(f"Running for date: {job_date}")
y, m, d = job_date.split("-")


# initialize paths

orders_path = f"{RAW_BASE_PATH}/orders/year={y}/month={m}/day={d}"
shipping_path = f"{RAW_BASE_PATH}/shipping/year={y}/month={m}/day={d}"
products_path = f"{RAW_BASE_PATH}/products/year={y}/month={m}/day={d}"
order_details_path = f"{RAW_BASE_PATH}/order_details/year={y}/month={m}/day={d}"
returned_orders_path = f"{RAW_BASE_PATH}/returned/year={y}/month={m}/day={d}"
customers_path = f"{RAW_BASE_PATH}/customers/year={y}/month={m}/day={d}"


# read raw data into DataFrames using our core reader utility
orders_df = read_json_data(spark, orders_path, "order")
shipping_df = read_json_data(spark, shipping_path, "shipping")
products_df = read_json_data(spark, products_path, "product")
order_details_df = read_json_data(spark, order_details_path, "order_details")
returned_orders_df = read_json_data(spark, returned_orders_path, "returned")
customer_df = read_json_data(spark, customers_path, "customer")

# build dimensions using our transform functions
product_dim = build_product_dim(products_df)
location_dim = build_location_dim(shipping_df)
order_profile_dim = build_order_profile_dim(orders_df, shipping_df)
customer_dim= build_customer_dim(customer_df)


# build fact table using our transform function
fact_orders = build_order_fact(
    order_details_df,
    shipping_df,
    orders_df,
    location_dim,
    order_profile_dim,
    returned_orders_df
)


# write dimensions and fact table to Delta Lake using the writer function 
logging.info("Writing product_dim...")
write_delta_scd1(product_dim, TABLE_PATHS["product"], "product_id")

logging.info("Writing location_dim...")
write_delta_scd1(location_dim, TABLE_PATHS["location"], "location_key")

logging.info("Writing order_profile_dim...")
write_delta_scd1(order_profile_dim, TABLE_PATHS["order_profile"], "profile_key")

logging.info("Writing customer_dim...")
write_delta_scd1(customer_dim, TABLE_PATHS["customer"], "customer_id")

logging.info("Writing fact_orders...")
write_fact_table(fact_orders, TABLE_PATHS["fact_orders"], "row_id")

logging.info("Pipeline completed successfully.")

