import re

def clean_column_names(df):
    def normalize(c):
        c = c.lower()
        c = re.sub(r'[^a-z0-9]+', '_', c)
        return c.strip('_')

    return df.toDF(*[normalize(c) for c in df.columns])