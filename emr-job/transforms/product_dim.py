def build_product_dim(df):

    return df.select(
        "product_id",
        "product_name",
        "category",
        "sub_category"
    ).dropDuplicates(["product_id"])