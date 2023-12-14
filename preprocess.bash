#!/bin/bash

# Run preprocessing script
python3 preprocessing/preprocess.py --replace_na="" --dedup_columns=instruction,output --na_strings_path="./preprocessing/regex_patterns/nas.json" --save_name=processed.parquet