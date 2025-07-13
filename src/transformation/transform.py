from typing import List

import polars as pl


def ingest_in_polars_and_remove_duplicates(variable_list: list[dict]) -> pl.lazyDataFrame:
    df=pl.DataFrame(variable_list).lazy()
    df=df.unique(subset=["id","telephonySessionId"],keep="last")
    df.select(pl.col())
    return df

def unnest_columns(df: pl.lazyDataFrame,original_column:str, desired_fields:List[str])->pl.DataFrame:
    existing_fields=df.select(pl.col(original_column)).schema[original_column].fields
    existing_fields_name={f.name for f in existing_fields}

    expr = [
        pl.col(original_column).struct.field(field).alias(f"{original_column}_{field}")
        if field in existing_fields_name
        else pl.lit(None).alias(f"{original_column}_{field}")
        for field in desired_fields
    ]
    return df.with_columns(expr)

def rest_of_transformations(df:pl.lazyDataFrame)->pl.lazyDataFrame:

    df=df.with_columns([
        pl.col("startTime").str.to_datetime(strict=False).alias("startTime")],
        pl.col("lastModifiedTime").str.to_datetime(strict=False).alias("lastModifiedTime"),
        pl.col("duration").alias("duration[sec]")
    )

    return df



