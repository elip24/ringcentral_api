import polars as pl
import os
from pathlib import Path


def get_every_call_file(file_ext:str) -> list[str]:
    path = Path.cwd()
    json_files = [str(p) for p in path.rglob(f"*{file_ext}")]
    return json_files