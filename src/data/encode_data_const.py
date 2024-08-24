from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
import pandas as pd
import argparse
import columns_structure


def encode_data(input_file, output_file):
    """
    Encode data based on the config
    """
    df = pd.read_excel(input_file)

    df = df[columns_structure.columns_to_select]

    # Artist - OrdinalEncoder
    ordinal_encoder = OrdinalEncoder()
    df['ARTIST'] = ordinal_encoder.fit_transform(df[['ARTIST']])

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

    # Convert all columns to numeric except 'AUCTION DATE', 'URL', 'ImageName'
    df[df.columns.difference(['AUCTION DATE', 'URL', 'ImageName'])] = df[df.columns.difference(
        ['AUCTION DATE', 'URL', 'ImageName'])].apply(pd.to_numeric, errors='coerce')

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
