"""Pandas module."""
import pandas as pd
import argparse


def filter_data(input_file, output_file):
    """
    Filter data based on the constant values.
    By this, ensure that the dataset does not contain outliers."
    """

    df = pd.read_excel(input_file)

    # Remove TOTAL DIMENSIONS outliers
    df = df[(df['TOTAL DIMENSIONS'] >= 10.00) &
            (df['TOTAL DIMENSIONS'] <= 10000.00)]

    # Remove PRICE outliers
    df = df[df['PRICE'] <= 10000]

    # Remove artworks created earlier than 1900 YEAR
    df = df[df['YEAR'] >= 1900]

    # Remove artists that have less than 10 occurances in the df
    df = df.loc[df['ARTIST'].map(df.loc[:, "ARTIST"].value_counts()) >= 10]

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

    filter_data(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
