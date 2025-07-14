from typing import List

import polars as pl
"Remove the next from after visualize"
from src.config.settings import json_file
from variables import record_of_from_columns_name,record_of_to_columns_name,column_to_use,record_of_extension_columns_name

def ingest_in_polars_and_remove_duplicates() -> pl.LazyFrame:
    df=pl.read_json(source=json_file).lazy()
    df=df.unique(subset=["id","telephonySessionId"],keep="last")
    #df.select(pl.col(*))
    return df

def unnest_columns(df: pl.LazyFrame,original_column:str, desired_fields:List[str])->pl.LazyFrame:
    existing_fields=df.select(pl.col(original_column)).schema[original_column].fields
    existing_fields_name={f.name for f in existing_fields}

    expr = [
        pl.col(original_column).struct.field(field).alias(f"{original_column}_{field}")
        if field in existing_fields_name
        else pl.lit(None).alias(f"{original_column}_{field}")
        for field in desired_fields
    ]
    return df.with_columns(expr)

def rest_of_transformations(df:pl.LazyFrame)->pl.LazyFrame:

    df=df.with_columns([
        pl.col("startTime").str.to_datetime(strict=False).alias("startTime"),
        pl.col("lastModifiedTime").str.to_datetime(strict=False).alias("lastModifiedTime"),
        pl.col("duration").alias("duration[sec]")
    ])

    return df

"""Activarlo para visualizacion""
"""
import pandas as pd

pd.set_option("display.max_columns", None)  # show all columns
pd.set_option("display.width", None)        # disable line wrapping
pd.set_option("display.max_colwidth", None) # show full column content
""
df=ingest_in_polars_and_remove_duplicates()

df=unnest_columns(df,"extension",record_of_extension_columns_name)
df=unnest_columns(df,"to",record_of_to_columns_name)
df=unnest_columns(df,"from",record_of_from_columns_name)
df=rest_of_transformations(df)
df=df.select(pl.col(column_to_use))
print(df.collect().to_pandas())
