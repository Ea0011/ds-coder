# Filtering and processing scripts for ds-coder-instruct dataset

ds-coder-instruct dataset [HuggingFace](https://huggingface.co/datasets/ed001/ds-coder-instruct-v1) was constructed by filtering data science code from publically available datasets on HuggingFace. For more detaisl, please visit the HuggingFace page linked above.

## filtering.py Documentation

`filtering.py` is a script designed to filter datasets based on specified criteria. Below is a guide on how to use this script, along with the available arguments:

## Usage

```bash
python filtering.py [OPTIONS]

Replace [OPTIONS] with the desired arguments.

Available Arguments

--tag_col [str]
Description: The name of the column to add the tag to.
Example: --tag_col "category"

--tag [str]
Description: Tag to attach to the filtered dataset.
Example: --tag "filtered"

--dataset_name [str]
Description: Name of the Parquet file in the raw folder.
Example: --dataset_name "my_dataset.parquet"

--regex_filters_path [str]
Description: Path to a JSON file with regex patterns for filtering.
Example: --regex_filters_path "./preprocessing/custom_filters.json"

--save_name [str]
Description: Name of the saved file in the filtered folder.
Example: --save_name "filtered_dataset.json"

--log_file [str]
Description: Path to the log file.
Example: --log_file "./logs/filtering.log"

--output_col_name [str]
Description: The name of the column to predict with the model.
Example: --output_col_name "output"

--input_col_name [str]
Description: The name of the column to prompt the model with.
Example: --input_col_name "instruction"

--line_max [int]
Description: Set the maximum allowed length for a line of code.
Example: --line_max 1000

--line_mean [int]
Description: Set the mean allowed length for a line of code.
Example: --line_mean 100

--alpha_frac [float]
Description: Set the minimum fraction of alphanumeric characters allowed.
Example: --alpha_frac 0.25

--min_size [int]
Description: Set the minimum size for an instruction (in words).
Example: --min_inst_size 5

--max_inst_size [int]
Description: Set the maximum size for an instruction (in words).
Example: --max_inst_size 1000

--max_threshold_comments [float]
Description: Set the maximum threshold for the comment to code ratio.
Example: --max_threshold_comments 0.8

--min_threshold_comments [float]
Description: Set the minimum threshold for the comment to code ratio.
Example: --min_threshold_comments 0.01
```

Filtering is performed using regex on the columns specified in JSON file in `regex_filters_path`. For example:
```json
{
  "output": [
    "import (matplotlib|pandas|sklearn|scipy|numpy|nltk|seaborn|xgboost|lightgbm|catboost)",
    "df\\[",
    "pd\\.",
    "plt\\.plot",
    "plt\\.show",
    "plt\\.subplots",
    "from sklearn",
    "model\\.fit\\(",
    "fig\\.show()",
    "import torch",
    "nn\\.Module",
    "import tensorflow",
    "import keras"
  ],

  "instruction": []
}
```

This will filter code in the `output` column to match any of the given regex patterns. You can create different JSON files with desired filters and run the script.