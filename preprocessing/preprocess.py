import logging
from preprocessing.args import ProcessingArgs
from simple_parsing import parse
import json
import pandas as pd
from functools import reduce
from preprocessing.utils import get_nl_ratio
import re
import os
from pathlib import Path


def parse_args() -> ProcessingArgs:
    return parse(ProcessingArgs)


def get_na_strs() -> list[str]:
    with open(file=args.na_strings_path) as f:
        na_str = json.load(f)

    return na_str
  
def exact_dedup(df: pd.DataFrame) -> pd.DataFrame:
  dedup_cols = args.dedup_columns.split(",")

  for col in dedup_cols:
    df = df.drop_duplicates(subset=[col], keep="first") 
    
  return df


def replace_nas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna(args.replace_na)
    if args.na_strings_path is not None:
        na_strs = get_na_strs()
        df = df.replace(na_strs, args.replace_na)
        
    return df


def save_processed_data(df: pd.DataFrame) -> None:
    assert args.save_name is not None, "save file name should be set"
    filename, file_extension = os.path.splitext(args.save_name)

    assert file_extension in [".csv", ".parquet", ".json"], "please spacify one of the compatible save formats"
    
    save_path = os.path.join(f"./data/processed/{args.save_name}")
    save_func = getattr(df, f"to_{file_extension[1:]}")
    
    df.reset_index(inplace=True, drop=True)
    
    if file_extension == ".json":
        save_func(save_path + "l", lines=True, orient="records")
    else:
        save_func(save_path)
      
  
if __name__ == "__main__":
    args: ProcessingArgs = parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
        handlers=[logging.FileHandler(args.log_file), logging.StreamHandler()],
    )
    logger.info(
        f"** The job is running with the following arguments: **\n{args}\n **** "
    )
    
    datadir = Path(os.path.join("./data/filtered/"))
    full_df = pd.concat(
      pd.read_parquet(parquet_file)
      for parquet_file in datadir.glob('*.parquet')
    )
    
    if args.dedup_columns is not None:
        full_df = exact_dedup(full_df)
      
    if args.replace_na is not None:
        full_df = replace_nas(full_df)
        
    save_processed_data(full_df)
      
