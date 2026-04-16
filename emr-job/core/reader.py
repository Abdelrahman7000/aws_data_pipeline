from pyspark.sql.functions import explode
from core.cleaner import clean_column_names

def read_json_entity(spark, path, entity_name):
    df = spark.read.option("multiLine", "true").json(path)
    
    df = df.select(explode("data").alias(entity_name))
    df = df.select(f"{entity_name}.*")
    
    df = clean_column_names(df)
    
    return df