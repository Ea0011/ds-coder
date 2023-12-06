from dataclasses import dataclass, field
from typing import List


@dataclass
class FilteringArgs:
    dataset_name: str = field(
        metadata={"help": "Name of the parquet file in the raw folder"}
    )

    regex_filters_path: str = field(
        default="./preprocessing/regex_filters.json",
        metadata={"help": "Path to a json file with regex patterns for filtering"},
    )

    save_path: str = field(
        default="./data/filtered/",
        metadata={"help": "Where to save the filtered dataset file"},
    )

    log_file: str = field(
        default="./filtering.log", metadata={"help": "Path to the log file"}
    )
