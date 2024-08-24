#!/bin/bash

# Check if at least one argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_filename.xlsx> [filter_date]"
    exit 1
fi

# Set variables based on the input filename and optional filter date
INPUT_FILENAME="$1"
BASENAME=$(basename "$INPUT_FILENAME" .xlsx)
INTERIM_FILENAME="data/interim/${BASENAME}.xlsx"
FILTERED_FILENAME="data/interim/filtered_${BASENAME}.xlsx"
ENCODED_FILENAME="data/processed/encoded_${BASENAME}.xlsx"
FILTER_DATE="${2:-}"

# Step 1: Process Data
echo "Processing data..."
python src/data/process_data.py "data/raw/${INPUT_FILENAME}" "$INTERIM_FILENAME"

# Step 2: Filter Data
echo "Filtering data..."
python src/data/filter_data.py "$INTERIM_FILENAME" "$FILTERED_FILENAME"

# Step 2.1: Optionally filter by date
if [ -n "$FILTER_DATE" ]; then
    echo "Filtering data by date: $FILTER_DATE..."
    python src/data/filter_by_date.py "$FILTERED_FILENAME" "$FILTERED_FILENAME" "$FILTER_DATE"
fi

# Step 3: Encode Data
echo "Encoding data..."
python src/data/encode_data_const.py "$FILTERED_FILENAME" "$ENCODED_FILENAME"

echo "Data processing completed successfully."
