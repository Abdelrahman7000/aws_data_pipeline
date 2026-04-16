from pyspark.sql.functions import col, explode, sha2, concat_ws
def build_customer_dim(df):

    df= df.filter(col("customer_id").isNotNull())
    return df.dropDuplicates(["customer_id"])
