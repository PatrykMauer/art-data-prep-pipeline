import json
import pandas as pd
import itertools
import argparse
import os
from pathlib import Path
from sklearn.feature_extraction import FeatureHasher
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
# pylint: disable=E0401
import columns_structure


def get_all_configurations():
    """
    Define the possible encodings for each column.
    """
    # Hash for ARTIST worked worse than Ordinal
    # OneHot encoding for SIGNATURE and CONDITION worked a tiny bit better
    encodings = {
        'ARTIST': ['Hash', 'Ordinal'],
        'TECHNIQUE': ['Ordinal'],
        'SIGNATURE': ['Ordinal', 'OneHot'],
        'CONDITION': ['Ordinal', 'OneHot']
    }
    # Generate all combinations
    all_combinations = list(itertools.product(*encodings.values()))
    return [dict(zip(encodings.keys(), combo)) for combo in all_combinations]


def hash_encode_column(df, column, n_features):
    """Uses Hash Encoder"""
    hasher = FeatureHasher(n_features=n_features, input_type='dict')
    hashed_data = hasher.transform(df[[column]].to_dict(orient='records'))
    hashed_df = pd.DataFrame(hashed_data.toarray(),
                             columns=[f'{column}_hash_{i}'
                                      for i in range(n_features)])
    df = df.drop(column, axis=1)
    df = pd.concat([hashed_df, df], axis=1)
    return df


def ordinal_encode_column(df, column, artist_price_order=None):
    """Uses Ordinal Encoder"""
    if artist_price_order is not None and column == 'ARTIST':
        ordinal_encoder = OrdinalEncoder(
            categories=[artist_price_order],
            handle_unknown='use_encoded_value', unknown_value=-1)
        df[column] = ordinal_encoder.fit_transform(df[[column]])
    else:
        ordinal_encoder = OrdinalEncoder(
            handle_unknown='use_encoded_value', unknown_value=-1)
        df[column] = ordinal_encoder.fit_transform(df[[column]])
    return df


def onehot_encode_column(df, column):
    """Uses OneHot Encoder"""
    onehot_encoder = OneHotEncoder()
    onehot_encoded = onehot_encoder.fit_transform(df[[column]])
    onehot_df = pd.DataFrame(onehot_encoded.toarray(),
                             columns=[f"{column}_{cat}"
                                      for cat in onehot_encoder.categories_
                                      [0]])
    df = df.drop(column, axis=1)
    df = pd.concat([onehot_df, df], axis=1)
    return df


def prepare_artist_ordinal_encoding(df):
    """Prepare ordinal encoding for the 'ARTIST' column based on average 'PRICE'."""
    if 'ARTIST' in df.columns and 'PRICE' in df.columns:
        df['PRICE'] = pd.to_numeric(
            df['PRICE'].replace(',', '', regex=True),
            errors='coerce')
        average_prices = df.groupby('ARTIST')['PRICE'].mean()
        return average_prices.sort_values().index.tolist()
    return None


def apply_artist_ordinal_encoding(df, artist_order):
    if 'ARTIST' in df.columns:
        artist_ranking = {artist: rank for rank,
                          artist in enumerate(artist_order)}
        df['ARTIST'] = df['ARTIST'].map(artist_ranking)


def save_artist_order_to_json(artist_price_order, file_path):
    """
    Save the artist_price_order list to a JSON file.

    Parameters:
        artist_price_order (list): List of dictionaries containing artist names and prices.
        file_path (str): Path to the JSON file to be saved.
    """
    with open(file_path, "w", encoding='utf8') as json_file:
        json.dump(artist_price_order, json_file, indent=4)

    print(f"JSON data has been saved to {file_path}")


def encode_data(input_file, encoding_config):
    """
    Creates multiple encoded DateFrames. 
    One per each combination in encoding_config
    """
    df = pd.read_excel(input_file)
    df = df[columns_structure.columns_to_select]

    for column, encoder_type in encoding_config.items():
        if encoder_type == 'Hash':
            df = hash_encode_column(df, column, n_features=3)

        elif encoder_type == 'Ordinal':
            if column == 'ARTIST':
                # Split to avoid data leakage the encoding to both the training and test datasets
                train_df, test_df = train_test_split(
                    df, test_size=0.2, random_state=42)
                artist_order = prepare_artist_ordinal_encoding(train_df)
                # Apply the encoding to both the training and test datasets
                apply_artist_ordinal_encoding(train_df, artist_order)
                apply_artist_ordinal_encoding(test_df, artist_order)
                save_artist_order_to_json(
                    artist_order, "artist_order.json")
                df = ordinal_encode_column(df, column, artist_order)
            else:
                df = ordinal_encode_column(df, column)

        elif encoder_type == 'OneHot':
            df = onehot_encode_column(df, column)

    return df


def main():
    """
    Function accepting arguments.
    Generates multiple files.
    One per each combination in configurations.
    """
    configurations = get_all_configurations()

    parser = argparse.ArgumentParser(description='Process and auction data.')
    parser.add_argument('input_file', type=str,
                        help='Path to the input Excel file.')
    parser.add_argument(
        '--output_folder', type=str, default='data/processed',
        help='Path to the output folder')
    args = parser.parse_args()

    # Extract the base name of the input file
    input_file_name = os.path.splitext(os.path.basename(args.input_file))[0]

    for config in configurations:
        # Create a descriptive file name based on the configuration
        output_file = Path(
            args.output_folder) / f"{input_file_name}_{''.join(config.values())}.xlsx"

        encoded_df = encode_data(args.input_file, config)

        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save to Excel
        encoded_df.to_excel(output_file, index=False)


if __name__ == '__main__':
    main()
