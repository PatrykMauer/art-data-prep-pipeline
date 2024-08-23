"""Pandas module."""
import argparse
import pandas as pd


def sort_data(input_file, output_file):
    """Function sorting data by AUCTION DATE."""
    df = pd.read_excel(input_file)

    df['AUCTION DATE'] = pd.to_datetime(df['AUCTION DATE'], format='%d-%m-%Y', errors='coerce')

    df = df.sort_values(by='AUCTION DATE')

    df.to_csv(output_file, index=False)

def main():
    """Function accepting arguments"""
    parser = argparse.ArgumentParser(description='Process and sort auction data.')
    parser.add_argument('input_file', type=str, help='Path to the input Excel file.')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file.')

    args = parser.parse_args()

    sort_data(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
