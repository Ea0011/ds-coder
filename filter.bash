#!/bin/bash

# Run filtering scripts
python3 preprocessing/filtering.py --dataset_name="code-instructions-122k-alpaca-style" --regex_filters_path="./preprocessing/regex_patterns/python_ds.json" --tag=python --tag_col=lang --save_name="python-code-instructions-122k-alpaca-style.parquet" --
python3 preprocessing/filtering.py --dataset_name="evol-codealpaca-v1" --regex_filters_path="./preprocessing/regex_patterns/python_ds.json" --tag=python --tag_col=lang --save_name="python-evol-codealpaca-v1.parquet"
python3 preprocessing/filtering.py --dataset_name="magicoder-python-instruct" --regex_filters_path="./preprocessing/regex_patterns/python_ds.json" --tag=python --tag_col=lang --save_name="python-magicoder-instruct.parquet"
python3 preprocessing/filtering.py --dataset_name="evol-instruct-code-80k-v1" --regex_filters_path="./preprocessing/regex_patterns/python_ds.json" --tag=python --tag_col=lang --save_name="python-evol-instruct-code-80k-v1.parquet"
python3 preprocessing/filtering.py --dataset_name="python-code-instructions-18k-alpaca" --regex_filters_path="./preprocessing/regex_patterns/python_ds.json" --tag=python --tag_col=lang --save_name="python-code-instructions-18k-alpaca.parquet"