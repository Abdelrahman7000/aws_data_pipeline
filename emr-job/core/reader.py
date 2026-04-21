from pyspark.sql.functions import explode
import re


def clean_column_names(df):
    '''
    Args:
        df: A Spark DataFrame with column names to be cleaned.
    '''
    def normalize(c):
        c = c.lower()
        c = re.sub(r'[^a-z0-9]+', '_', c)
        return c.strip('_')

    return df.toDF(*[normalize(c) for c in df.columns])



def read_json_data(spark, path, entity_name):
    '''
    Args:
        spark: A SparkSession object.
        path: The path to the JSON file to be read.
        entity_name: The name of the table to be extracted from the JSON data.
    '''
    df = spark.read.option("multiLine", "true").json(path)
    
    df = df.select(explode("data").alias(entity_name))
    df = df.select(f"{entity_name}.*")
    
    df = clean_column_names(df)
    
    return df