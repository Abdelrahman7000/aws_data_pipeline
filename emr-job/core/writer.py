from delta.tables import DeltaTable

def write_delta_scd1(df, path, key):

    df = df.dropDuplicates([key])

    if DeltaTable.isDeltaTable(df.sparkSession, path):

        delta_table = DeltaTable.forPath(df.sparkSession, path)

        delta_table.alias("tgt").merge(
            df.alias("src"),
            f"tgt.{key} = src.{key}"
        ).whenMatchedUpdateAll() \
         .whenNotMatchedInsertAll() \
         .execute()

    else:
        df.write.format("delta").mode("overwrite").save(path)


def write_fact_table(df, path, key):

    if DeltaTable.isDeltaTable(df.sparkSession, path):
        delta_table = DeltaTable.forPath(df.sparkSession, path)

        delta_table.alias("tgt").merge(
            df.alias("src"),
            f"tgt.{key} = src.{key}"
        ).whenMatchedUpdateAll() \
         .whenNotMatchedInsertAll() \
         .execute()

    else:
        df.write.format("delta").mode("overwrite").save(path)