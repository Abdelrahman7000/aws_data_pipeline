from pyspark.sql.functions import monotonically_increasing_id

def build_order_profile_dim(order_df, shipping_df):
    '''
    Args:
        order_df: DataFrame containing order data 
        shipping_df: DataFrame containing shipping data
    '''

    df = order_df.join(shipping_df, "order_id") \
        .select("order_priority", "market", "ship_mode") \
        .dropDuplicates()

    return df.withColumn("profile_key", monotonically_increasing_id())