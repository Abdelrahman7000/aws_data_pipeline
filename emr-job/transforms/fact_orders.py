from pyspark.sql.functions import col, when

def build_order_fact(order_details_df, shipping_df, order_df, location_dim, profile_dim, returned_orders_df):
    '''
    Args:
    - order_details_df: DataFrame containing order details 
    - shipping_df: DataFrame containing shipping information
    - order_df: DataFrame containing order information
    - location_dim: DataFrame containing location dimension
    - profile_dim: DataFrame containing profile dimension
    - returned_orders_df: DataFrame containing returned orders
    
    '''

    # Join order details with shipping and order data to get all necessary information for the fact table
    df = order_details_df.join(shipping_df, "order_id") \
        .join(order_df, "order_id")
    
    # Add a column to indicate if the order was returned
    returned_orders_df=returned_orders_df.withColumnRenamed("order_id", "returned_order_id")
    df = df.join(returned_orders_df, df['order_id']==returned_orders_df['returned_order_id'], "left")
    df = df.withColumn("returned", when(col("returned_order_id").isNotNull(), 1).otherwise(0))
    df = df.drop("returned_order_id")

    # Join with dimension tables to get the keys
    df = df.join(
        location_dim,
        on=["city", "state", "country", "region"]
    )
    # Join with profile_dim to get the profile_key
    df = df.join(
        profile_dim,
        on=["order_priority", "market", "ship_mode"]
    )

    return df.select(
        "row_id",
        "order_id",
        "product_id",
        "customer_id",
        "location_key",
        "profile_key",
        "ship_date",
        "order_date",
        "profit",
        "quantity",
        "sales",
        "discount",
        "shipping_cost",
        "returned"
    )