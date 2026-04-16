from pyspark.sql.functions import monotonically_increasing_id

def build_location_dim(df):

    return df.select(
        "city",
        "state",
        "country",
        "region"
    ).dropDuplicates() \
     .withColumn("location_key", monotonically_increasing_id())