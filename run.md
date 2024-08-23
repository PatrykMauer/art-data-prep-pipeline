# Data Processing Pipeline Instructions

This document outlines the steps for activating the virtual environment and processing data in our project.

## Activating Virtual Environment

For Windows users, activate the local virtual environment by running the following command in the root folder:


For Windows users, activate the local virtual environment by running the following command in the root folder:
```bash
.\.venv\Scripts\activate
```

## Processing Data

Follow these steps in sequence to process your data:

### 1. Process Data

Run the following command to process the raw data:
```bash
python src\data\process_data.py  data\raw\results_2024_03_04.xlsx data\interim\results_2024_03.04.xlsx
```

### 2. Filter Data

Filter the processed data using this command:
```bash
python src\data\filter_data.py  data\interim\results_2024_03.04.xlsx data\interim\filtered_results_2024_03.04.xlsx
```

### 2.1 (Optionally) - filter by date
python script_name.py input_file.xlsx output_file.xlsx 2024-04-03
python src\data\filter_by_date.py data\interim\filtered_results_2024_05.11.xlsx data\interim\filtered_results_2024_05.11.xlsx 2024-04-03

### 3. Encode Data

Encode the filtered data with the following command:
```bash
python src\data\encode_data_const.py data\interim\filtered_results_2024_03.04.xlsx data\processed\encoded_results_2024_03.04.xlsx
```

### 4. Encode Data for All Combinations

To encode data for all combinations, use:
```bash
python src\data\encode_data.py data\interim\filtered_results_2024_03.04.xlsx --output_folder data\processed
```

### 5. Split Data for Training and Test Sets

Split the data into training and test sets with this command:
```bash
python src\data\split_data.py data\processed\filtered_results_2024_03.04_OrdinalOrdinalOneHotOneHot.xlsx --output_folder data\processed
```

### 6. Scale the Train and Test Sets

Finally, scale the train and test sets and save the scalar to the references folder using:
```bash
python src\features\feature_scaling.py filtered_results_2024_03.04_OrdinalOrdinalOneHotOneHot --output_folder data\processed --columns ARTIST TECHNIQUE "TOTAL DIMENSIONS" YEAR
```

### 7. Create features for the CNN

Connect the scaled Train and Test set with CNN features to ensure that there is no data leakage.
Connect them by ImageName.

python create_feature_price_datasets.py <train_file_path> <test_file_path> <features_file_path>

```bash
python src\features\create_feature_price_datasets.py data\processed\filtered_results_2024_03.04_OrdinalOrdinalOneHotOneHot_train_scaled.xlsx data\processed\filtered_results_2024_03.04_OrdinalOrdinalOneHotOneHot_test_scaled.xlsx data\interim\features.csv
```

### 8. Equalize rows in Test Sets

The created dataset with CNN features has lower number of rows comparing to the Test set from tabular data approach.
Equalize the number of rows by removing the one which were not used for merging.

python equalize_rows_number.py <to_remove_from_file_path> <to_compare_file_path>

```bash
python src\data\equalize_rows_number.py data\processed\filtered_results_2024_03.04_OrdinalOrdinalOneHotOneHot_test_scaled.xlsx data\processed\test_features_price.csv

python src\data\equalize_rows_number.py data\processed\filtered_results_2024_03.04_OrdinalOrdinalOneHotOneHot_train_scaled.xlsx data\processed\train_features_price.csv
```