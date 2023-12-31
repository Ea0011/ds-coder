import logging
from preprocessing.args import FilteringArgs
from simple_parsing import parse
import json
import pandas as pd
from functools import reduce
from preprocessing.utils import get_nl_ratio
import re
import os


def parse_args() -> FilteringArgs:
    return parse(FilteringArgs)


def get_regex_patterns() -> list[str]:
    with open(file=args.regex_filters_path) as f:
        filters = json.load(f)

    return filters


def filter_regex_patterns(df: pd.DataFrame, regex_filters: list[str]) -> pd.DataFrame:
    filtered_idx = []
    for col_name, regex in regex_filters.items():
        if len(regex) != 0:
            filtered = df[col_name].str.contains("|".join(regex), regex=True)
            filtered_idx.append(filtered)

    union_of_filters = reduce(lambda a, b: a | b, filtered_idx)

    return df[union_of_filters]


def filter_long_and_short_instructions(df: pd.DataFrame) -> pd.DataFrame:
    len_filter_idx = df[args.input_col_name].apply(
        lambda s: (len(s.split(" ")) < args.max_inst_size)
        and (len(s.split(" ")) > args.min_inst_size)
    )
    return df[len_filter_idx]


def filter_line_length(df: pd.DataFrame) -> pd.DataFrame:
    max_len_filter = lambda s: len(max(s.split("\n"), key=len)) <= args.line_max
    mean_len_filter = (
        lambda s: sum(map(len, s.split("\n"))) / len(s.split("\n")) <= args.line_mean
    )

    line_len_filter_max_idx = df[args.output_col_name].apply(max_len_filter)
    line_len_filter_mean_idx = df[args.output_col_name].apply(mean_len_filter)

    return df[line_len_filter_mean_idx & line_len_filter_max_idx]


def filter_alphanum_ratio(df: pd.DataFrame) -> pd.DataFrame:
    alphanum_ratio_filter = (
        lambda s: sum(map(len, re.findall("\w+", s))) / len(s) >= args.alpha_frac
    )

    return df[df[args.output_col_name].apply(alphanum_ratio_filter)]


def filter_comment_ratio(df: pd.DataFrame) -> pd.DataFrame:
    comment_ratio_filter = lambda s: (
        get_nl_ratio(s, "python") < args.max_threshold_comments
    ) and (get_nl_ratio(s, "python") > args.min_threshold_comments)

    return df[df[args.output_col_name].apply(comment_ratio_filter)]


def load_dataset_df() -> pd.DataFrame:
    df = pd.read_parquet(os.path.join(f"./data/raw/{args.dataset_name}.parquet"))

    return df


def add_tags(df: pd.DataFrame) -> pd.DataFrame:
    df[args.tag_col] = args.tag

    return df


def save_filtered_data(df: pd.DataFrame) -> None:
    assert args.save_name is not None, "save file name should be set"

    df["dataset"] = args.dataset_name
    filename, file_extension = os.path.splitext(args.save_name)

    assert file_extension in [
        ".csv",
        ".parquet",
        ".json",
    ], "please spacify one of the compatible save formats"

    save_path = os.path.join(f"./data/filtered/{args.save_name}")
    save_func = getattr(df, f"to_{file_extension[1:]}")

    df.reset_index(inplace=True, drop=True)

    if file_extension == ".json":
        save_func(save_path + "l", lines=True, orient="records")
    else:
        save_func(save_path)


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

    filters = get_regex_patterns()

    logger.info(f"** Loaded filters are: {filters}")

    df = load_dataset_df()
    regex_filtered = filter_regex_patterns(df, filters)

    logger.info(
        f"** Regex filtered with filters {filters}\n \
        Remaining rows: {regex_filtered.count(axis=0)}"
    )

    length_filtered = filter_long_and_short_instructions(regex_filtered)

    logger.info(
        f"** Filtered with max inst len {args.max_inst_size}, and min inst len {args.min_inst_size} \n \
        Remaining rows: {length_filtered.count(axis=0)}"
    )

    line_len_filtered = filter_line_length(length_filtered)

    logger.info(
        f"** Filtered line len with mean {args.line_mean} and max len {args.line_max} \n \
        Remaining rows: {line_len_filtered.count(axis=0)}"
    )

    alphanum_filtered = filter_alphanum_ratio(line_len_filtered)

    logger.info(
        f"** Filtered alphanumeric ratio with min ratio of {args.alpha_frac} \n \
        Remaining rows: {alphanum_filtered.count(axis=0)}"
    )

    comment_ratio_filtered = filter_comment_ratio(alphanum_filtered)

    logger.info(
        f"** Filtered comment to code ratio with max ratio of {args.max_threshold_comments} \n \
        Remaining rows: {comment_ratio_filtered.count(axis=0)}"
    )

    if args.tag_col is not None:
        assert args.tag is not None, "The tag should not be empty if tag_col is set"
        comment_ratio_filtered = add_tags(comment_ratio_filtered)

        logger.info(f"** Added tag {args.tag} to the column {args.tag_col} \n")

    save_filtered_data(comment_ratio_filtered)
