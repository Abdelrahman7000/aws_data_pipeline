from pyspark.sql.functions import col, when

def build_order_fact(order_details_df, shipping_df, order_df, location_dim, profile_dim, returned_orders_df):

    df = order_details_df.join(shipping_df, "order_id") \
        .join(order_df, "order_id")
    
    returned_orders_df=returned_orders_df.withColumnRenamed("order_id", "returned_order_id")
    df = df.join(returned_orders_df, df['order_id']==returned_orders_df['returned_order_id'], "left")
    df = df.withColumn("returned", when(col("returned_order_id").isNotNull(), 1).otherwise(0))
    df = df.drop("returned_order_id")

    df = df.join(
        location_dim,
        on=["city", "state", "country", "region"]
    )

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