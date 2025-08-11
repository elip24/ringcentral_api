from datetime import datetime
from typing import List
import polars as pl
from src.config.settings import json_file
from src.transformation.variables import schema
from datetime import datetime, timezone
from src.transformation.transform_mode import get_every_call_file
from src.transformation.variables import record_of_from_columns_name,record_of_to_columns_name,column_to_use,record_of_extension_columns_name,record_from_device_column_name

def ingest_in_polars_and_remove_duplicates(file) -> pl.LazyFrame:
    df=pl.read_parquet(source=file,schema=schema).lazy()
    df=df.unique(subset=["id","telephonySessionId"],keep="last")
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

def rest_of_transformations(df: pl.LazyFrame) -> pl.LazyFrame:
    df = df.with_columns([
        pl.col("startTime").cast(pl.Utf8).alias("startTime"),
        pl.col("startTime").cast(pl.Utf8).str.slice(0, 10).alias("startDate"),
        pl.col("lastModifiedTime").cast(pl.Utf8).alias("lastModifiedTime"),
        pl.col("duration").cast(pl.Utf8).alias("duration[sec]"),
    ])
    return df

def transformation():
    parquet_files=get_every_call_file('.parquet')
    all_lazyframes=[]
    for file in parquet_files:
        df = ingest_in_polars_and_remove_duplicates(file=file)
        df = unnest_columns(df, "from", record_of_from_columns_name)
        df = unnest_columns(df, "to", record_of_to_columns_name)
        df = unnest_columns(df, "extension", record_of_extension_columns_name)
        df = unnest_columns(df, "from_device", record_of_extension_columns_name)
        df = rest_of_transformations(df)
        if not df.limit(1).collect().is_empty():
            all_lazyframes.append(df)
    final_df=pl.concat(all_lazyframes,how='diagonal_relaxed').collect()
    final_df=final_df.select(pl.col(column_to_use))
    final_df.write_parquet('ringcentral.parquet')

df=transformation()