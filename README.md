
# Data Processing Pipeline Instructions

This document outlines the steps for running the data processing pipeline.

## Clone the project
```
https://github.com/PatrykMauer/art-data-prep-pipeline.git
```    

## Run the pipeline with docker
```
docker build -t art-data-prep-pipeline .
```
Change 'results_2024_05_11' to reflect your filename. For the time being only .xlsx is supported.
```
docker run -it --rm -v .:/app -w /app art-data-prep-pipeline /bin/bash ./data_processing.sh results_2024_05_11.xlsx
```

# Local steps

If you prefer not to use docker, follow the steps below.
## Activating Virtual Environment

For Windows users, activate the local virtual environment by running the following command in the root folder:
```bash
.\.venv\Scripts\activate
```

## Processing Data

Follow these steps in sequence to process your data:

### 1. Process Data

Run the following command to process the raw data:
```bash
python src\data\process_data.py  data\raw\results_2024_05_11.xlsx data\interim\results_2024_05_11.xlsx
```

### 2. Filter Data

Filter the processed data using this command:
```bash
python src\data\filter_data.py  data\interim\results_2024_05_11.xlsx data\interim\filtered_results_2024_05_11.xlsx
```

### 2.1 (Optionally) - filter by date
python script_name.py input_file.xlsx output_file.xlsx 2024-04-03
python src\data\filter_by_date.py data\interim\filtered_results_2024_05.11.xlsx data\interim\filtered_results_2024_05.11.xlsx 2024-04-03

### 3. Encode Data

Encode the filtered data with the following command:
```bash
python src\data\encode_data_const.py data\interim\filtered_results_2024_05_11.xlsx data\processed\encoded_results_2024_05_11.xlsx
```

### 4. Encode Data for All Combinations

To encode data for all combinations, use:
```bash
python src\data\encode_data.py data\interim\filtered_results_2024_05_11.xlsx --output_folder data\processed
```

### 5. Split Data for Training and Test Sets

Split the data into training and test sets with this command:
```bash
python src\data\split_data.py data\processed\filtered_results_2024_05_11_OrdinalOrdinalOneHotOneHot.xlsx --output_folder data\processed
```

### 6. Scale the Train and Test Sets

Finally, scale the train and test sets and save the scalar to the references folder using:
```bash
python src\features\feature_scaling.py filtered_results_2024_05_11_OrdinalOrdinalOneHotOneHot --output_folder data\processed --columns ARTIST TECHNIQUE "TOTAL DIMENSIONS" YEAR
```

### 7. Create features for the CNN

Connect the scaled Train and Test set with CNN features to ensure that there is no data leakage.
Connect them by ImageName.

python create_feature_price_datasets.py <train_file_path> <test_file_path> <features_file_path>

```bash
python src\features\create_feature_price_datasets.py data\processed\filtered_results_2024_05_11_OrdinalOrdinalOneHotOneHot_train_scaled.xlsx data\processed\filtered_results_2024_05_11_OrdinalOrdinalOneHotOneHot_test_scaled.xlsx data\interim\features.csv
```

### 8. Equalize rows in Test Sets

The created dataset with CNN features has lower number of rows comparing to the Test set from tabular data approach.
Equalize the number of rows by removing the one which were not used for merging.

python equalize_rows_number.py <to_remove_from_file_path> <to_compare_file_path>

```bash
python src\data\equalize_rows_number.py data\processed\filtered_results_2024_05_11_OrdinalOrdinalOneHotOneHot_test_scaled.xlsx data\processed\test_features_price.csv

python src\data\equalize_rows_number.py data\processed\filtered_results_2024_05_11_OrdinalOrdinalOneHotOneHot_train_scaled.xlsx data\processed\train_features_price.csv
```


==============================

A predictive model for art auction results.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


