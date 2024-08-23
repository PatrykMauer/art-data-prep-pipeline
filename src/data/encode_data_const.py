from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import FeatureHasher
import pandas as pd
import argparse
# pylint: disable=E0401
import columns_structure


def encode_data(input_file, output_file):
    """
    Encode data based on the config
    """
    df = pd.read_excel(input_file)

    df = df[columns_structure.columns_to_select]

    # Artist - HashEncoder
    data_for_hashing = [{'artist': artist} for artist in df['ARTIST']]
    N_FEATURES = 6

    hasher = FeatureHasher(n_features=N_FEATURES, input_type='dict')
    hashed_features = hasher.transform(data_for_hashing)
    hashed_features_df = pd.DataFrame(hashed_features.toarray())

    new_columns = [f'artist_hashed_{i}' for i in range(
        hashed_features_df.shape[1])]
    hashed_features_df.columns = new_columns

    if 'ARTIST' in df.columns:
        df = df.drop('ARTIST', axis=1)

    hashed_features_df = hashed_features_df.reset_index(drop=True)
    df = df.reset_index(drop=True)
    df = pd.concat([hashed_features_df, df], axis=1)
    df.head()

    # Technique - OrdinalEncoder - map first three to 0, and the rest to following numbers
    ordinal_encoder = OrdinalEncoder(
        categories=[columns_structure.techniques_order])
    df['TECHNIQUE'] = ordinal_encoder.fit_transform(df[['TECHNIQUE']])

    # Signature - OrdinalEncoding
    ordinal_encoder = OrdinalEncoder(
        categories=[columns_structure.signature_order])
    df['SIGNATURE'] = ordinal_encoder.fit_transform(df[['SIGNATURE']])

    # Condition - OrdinalEncoding
    ordinal_encoder = OrdinalEncoder(
        categories=[columns_structure.condition_order])
    df['CONDITION'] = ordinal_encoder.fit_transform(df[['CONDITION']])

    # Convert 'PRICE' to numeric, setting non-numeric values to NaN
    df['PRICE'] = pd.to_numeric(
        df['PRICE'].replace(',', '', regex=True),
        errors='coerce')

    # Convert all columns to numeric except 'AUCTION DATE' and 'URL'
    df[df.columns.difference(['AUCTION DATE', 'URL'])] = df[df.columns.difference(
        ['AUCTION DATE', 'URL'])].apply(pd.to_numeric, errors='coerce')

    df.to_excel(output_file, index=False)


def main():
    """Function accepting arguments"""
    parser = argparse.ArgumentParser(
        description='Process and auction data.')
    parser.add_argument('input_file', type=str,
                        help='Path to the input Excel file.')
    parser.add_argument('output_file', type=str,
                        help='Path to the output Excel file.')

    args = parser.parse_args()

    encode_data(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
