"""Filter the dataset by date."""
import pandas as pd
import argparse


def filter_by_date(input_file, output_file, cutoff_date_str):
    """
    Filter data based on the given cutoff date.
    By this, ensure that the dataset does not contain data past the cutoff date."
    """
    df = pd.read_excel(input_file)

    # Convert string date to timestamp
    cutoff_date = pd.Timestamp(cutoff_date_str)
    df = df[df['AUCTION DATE'] > cutoff_date]

    df.to_excel(output_file, index=False)


def main():
    """Function accepting arguments"""
    parser = argparse.ArgumentParser(
        description='Process auction data.')
    parser.add_argument('input_file', type=str,
                        help='Path to the input Excel file.')
    parser.add_argument('output_file', type=str,
                        help='Path to the output Excel file.')
    parser.add_argument('cutoff_date', type=str,
                        help='Cutoff date for filtering in YYYY-MM-DD format.')

    args = parser.parse_args()

    filter_by_date(args.input_file, args.output_file, args.cutoff_date)


if __name__ == '__main__':
    main()
