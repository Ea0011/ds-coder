from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FilteringArgs:
    tag_col: Optional[str] = field(
        metadata={"help": "The name of the column to add the tag to"},
    )

    tag: Optional[str] = field(
        metadata={"help": "Tag to attach to filtered dataset"},
    )

    dataset_name: str = field(
        metadata={"help": "Name of the parquet file in the raw folder"}
    )

    regex_filters_path: Optional[str] = field(
        default="./preprocessing/regex_filters.json",
        metadata={"help": "Path to a json file with regex patterns for filtering"},
    )

    save_name: Optional[str] = field(
        default="filtered",
        metadata={"help": "Name of the saved file in filtered folder"},
    )

    log_file: Optional[str] = field(
        default="./filtering.log", metadata={"help": "Path to the log file"}
    )

    line_max: Optional[int] = field(
        default=1000,
        metadata={"help": "Max line length allowed"},
    )

    line_mean: Optional[int] = field(
        default=100,
        metadata={"help": "Mean line length allowed"},
    )

    alpha_frac: Optional[float] = field(
        default=0.25,
        metadata={"help": "Minimum fraction of alphanumeric characters allowed."},
    )

    min_size: Optional[int] = field(
        default=100,
        metadata={"help": "Minimum content size."},
    )

    max_size: Optional[int] = field(
        default=5000,
        metadata={"help": "Maximum content size."},
    )

    min_inst_size: Optional[int] = field(
        default=5,
        metadata={"help": "Minimum instruction size in words."},
    )

    max_inst_size: Optional[int] = field(
        default=1000,
        metadata={"help": "Maximum instruction size in words."},
    )

    max_threshold_comments: Optional[float] = field(
        default=0.8,
        metadata={"help": "Maximum threshold for comment to code ratio."},
    )

    min_threshold_comments: Optional[float] = field(
        default=0.01,
        metadata={"help": "Minimum threshold for comment to code ratio."},
    )

    output_col_name: Optional[str] = field(
        default="output",
        metadata={"help": "The name of the column to predict with the model"},
    )

    input_col_name: Optional[str] = field(
        default="instruction",
        metadata={"help": "The name of the column to prompt the model with"},
    )


@dataclass
class ProcessingArgs:
    na_strings_path: Optional[str] = field(
        metadata={"help": "Path to a JSON array with values regarded as NA"}
    )

    dedup_columns: Optional[str] = field(
        default="", metadata={"help": "Which cols to use for deduplication"}
    )

    replace_na: Optional[str] = field(
        default="", metadata={"help": "Value to replace NAs with"}
    )

    save_name: Optional[str] = field(
        default="processed",
        metadata={"help": "Name of the saved file in processed folder"},
    )

    log_file: Optional[str] = field(
        default="./preprocessing.log", metadata={"help": "Path to the log file"}
    )
