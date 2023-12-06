import logging
import time
from preprocessing.args import FilteringArgs
from simple_parsing import parse
import json
import pandas as pd


def parse_args():
    return parse(FilteringArgs)


def get_regex_patterns(patterns_path: str) -> list[str]:
    with open(file=patterns_path) as f:
        filters = json.load(f)

    return filters


def filter_regex_patterns(df: pd.DataFrame, regex_filters: list[str]) -> pd.DataFrame:
    column, regex = list(regex_filters.keys())[0], "|".join(
        list(regex_filters.values())[0]
    )
    filtered = df[column].str.contains(regex, regex=True)

    return df[filtered]


def load_dataset_df(dataset_name: str) -> pd.DataFrame:
    df = pd.read_parquet(f"./data/raw/{dataset_name}.parquet")

    return df


if __name__ == "__main__":
    args: FilteringArgs = parse_args()

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

    filters = get_regex_patterns(args.regex_filters_path)

    logger.info(f"** Loaded filters are: {filters}")

    df = load_dataset_df(args.dataset_name)
    regex_filtered = filter_regex_patterns(df, filters)

    logger.info(
        f"** Regex filtered with filters {filters}\n \
      Remaining rows: {regex_filtered.count(axis=0)}"
    )
