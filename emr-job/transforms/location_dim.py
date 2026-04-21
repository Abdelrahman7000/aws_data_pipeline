from pyspark.sql.functions import monotonically_increasing_id

def build_location_dim(df):
    '''
    Args:
        df: A Spark DataFrame containing the raw data
    '''
    # Select distinct location attributes and create a surrogate key
    return df.select(
        "city",
        "state",
        "country",
        "region"
    ).dropDuplicates() \
     .withColumn("location_key", monotonically_increasing_id())