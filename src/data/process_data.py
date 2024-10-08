"""Regex module."""
import re
import argparse
import numpy as np
import pandas as pd
from unidecode import unidecode
# pylint: disable=E0401
import columns_structure
import metrics


def remove_accents(text):
    """Changes letters with accents to their corresponding base letters."""
    return unidecode(text)


def normalize_and_sort_letters(name):
    """Returns artist name sorted to handle the order of name and surname"""
    name = name.lower()
    # Remove spaces and special characters
    name = re.sub(r'\W+', '', name)
    # Sort the letters alphabetically
    name = ''.join(sorted(name))
    return name


def apply_replacements(text):
    """
    Ensures consistency in artists names by replacing noisy chars.
    Takes care of "after" prefix location.
    """
    replacements = [
        # Removes parentheses
        (r'[\(\)]', ''),

        # Matches various formats of year ranges and individual years, replaces with empty string
        (
            r'\d{4}-\d{4}|\d{4} - \d{4}|\d{4} -\d{4}|\d{4}- \d{4}|'
            r'\d{4}-|\d{4}–\d{4}|\d{4} – \d{4}|\d{4} –\d{4}|'
            r'\d{4}– \d{4}|\d{4}–|\d{4}|\d{4}/\d{2}-\d{4}/\d{2}|'
            r'\b[MDCLXVI]+\b-\b[MDCLXVI]+\b|\b[MDCLXVI]+\b|'
            r'\b[MDCLXVI]e+\b| - | – |Fl\.|fl\.|fl |,|c\.|\.|\*|'
            r'/-|/|\?|&amp|;|:', ''
        ),

        # Matches various forms of 'after', in different languages, replaces with 'after'
        (
            r'd\'apres|d\'apre|\'apres|after|afte|After|nach|naar|dopo',
            'after'
        ),
    ]
    for pattern, replacement in replacements:
        # Use the text variable to apply the replacements
        text = text.str.replace(pattern, replacement, regex=True)

    text = text.str.strip()
    text = text.str.replace(r'  ', ' ')

    # Additional operation for handling "after" prefixes
    text = text.apply(lambda x: x if not x.startswith(
        "after ") else x.lstrip("after ") + " after")

    return text


def extract_first_desired_text(text, data, default_return):
    """
    Ensures the consistency in the columns of the dataset by accepting a list of tuples 
    that contain the possible values for the column and possible words that suggest that 
    this value should be returned.

    Parameters:
    text (str or fl): The text to be searched for matching substrings.
    data (list of tuples): A list where each tuple contains a substring
    and its corresponding desired result.
    default_return (str): The default return value if no match is found or if the text is a float.

    Returns:
    str: The capitalized result corresponding
    to the first found substring or the default return value.
    """
    if isinstance(text, float):
        return default_return
    text = text.lower()
    for substring, result in data:
        if substring.lower() in text:
            return result.capitalize()
    return default_return


def ensure_dimensions_structure(row):
    """Ensures that the unit is on the last position"""
    unit = row.iloc[-1] if pd.notna(row.iloc[-1]) else ''
    dimensions = [str(dim) for dim in row[:-1] if pd.notna(dim)]

    return '×'.join(dimensions) + (' ' + unit if unit else '')


def retrieve_year(text):
    """ Retrieve year from DESCRIPTION column"""
    for period, year in columns_structure.periods_to_year:
        if text == period:
            return year
    return None


def convert_to_int_or_nan(value):
    """Converts a given value to an integer, or returns NaN if conversion fails."""
    try:
        return int(value)
    except ValueError:
        return float('nan')


def remove_columns(df, columns_to_remove):
    """Removes specified columns from a DataFrame."""
    columns_to_keep = [i for i in range(
        len(df.columns)) if i not in columns_to_remove]
    df = df.iloc[:, columns_to_keep]
    return df


def process_data(input_file, output_file):
    """Function sorting data by AUCTION DATE."""

    df = pd.read_excel(input_file)
    df = remove_columns(df, columns_structure.columns_to_remove)

    df['AUCTION DATE'] = pd.to_datetime(df['AUCTION DATE'], errors='coerce')

    df = df.dropna(subset=['AUCTION DATE'])
    print(df['AUCTION DATE'].dtype)
    assert df['AUCTION DATE'].dtype == 'datetime64[ns]', "AUCTION DATE column is not all datetime objects"

    df = df.sort_values(by='AUCTION DATE')

    df['OBJECT'].replace("", np.nan, inplace=True)
    df['OBJECT'].fillna("Print", inplace=True)
    df = df[df['OBJECT'].str.contains("Print", na=False)]

    df = df[~df['ARTIST'].str.strip().eq("")]
    df = df.dropna(subset=['ARTIST'])

    # Deacreasing the number of Artists - Unification of text
    df.loc[:, "ARTIST"] = df.loc[:, "ARTIST"].apply(remove_accents)
    df['ARTIST'] = apply_replacements(df['ARTIST'])

    # Remove rows containing 'attr' or 'Attr'
    df = df[~df['ARTIST'].str.contains('attr|Attr')]
    df = df[~df['ARTIST'].str.contains('print|Print')]

    # Standardize and normalize Artists names (make the order of name and surname insignificant)
    df.loc[:, "ARTIST"] = df.loc[:, "ARTIST"].apply(normalize_and_sort_letters)

    # Third Column Preprocessing (Period)
    mode_value = df['PERIOD'].mode()[0]
    df['PERIOD'] = df['PERIOD'].replace('', mode_value)
    df['PERIOD'] = df['PERIOD'].str.split(',').str[0]

    # Fourth Column Preprocessing (Technique)
    df['TECHNIQUE'].fillna("", inplace=True)
    df['TECHNIQUE'] = df['TECHNIQUE'].apply(
        extract_first_desired_text,
        args=(columns_structure.techniques, "Unknown"))
    df = df[df['TECHNIQUE'].isin(columns_structure.techniques_to_keep)]
    # Remove posters
    regex = r'poster|plakat'
    df = df[~df['DESCRIPTION'].str.contains(regex, case=False, na=False)]

    # Fifth Column Preprocessing (Signature)
    df['SIGNATURE'].fillna("", inplace=True)
    df['SIGNATURE'] = df['SIGNATURE'].apply(
        extract_first_desired_text,
        args=(columns_structure.signatures, "Not signed"))

    # Seventh Column Preprocessing (Condition)
    df['CONDITION'].fillna("", inplace=True)
    df['CONDITION'] = df['CONDITION'].apply(extract_first_desired_text, args=(
        columns_structure.conditions, "Good condition"))

    # Eighth Column Preprocessing (Total Dimensions)
    # Extract missing values from the Description Column

    mask = (df['TOTAL DIMENSIONS'] == '') | df['TOTAL DIMENSIONS'].isna()
    extracted_data = df.loc[mask, 'DESCRIPTION'].str.extract(
        metrics.REGEX_DIMENSIONS)

    # Apply the function to each row of the extracted data
    df.loc[mask, 'TOTAL DIMENSIONS'] = extracted_data.apply(
        ensure_dimensions_structure, axis=1)

    # Convert all units to centimeters and calculate the area
    df['TOTAL DIMENSIONS'] = df['TOTAL DIMENSIONS'].apply(
        metrics.multiply_largest_dimensions)

    # Remove rows where exception occured and where dimensions provided where equal 0
    df = df[pd.notna(df['TOTAL DIMENSIONS']) & (df['TOTAL DIMENSIONS'] != '')]

    # Ninth Column Preprocessing (Price)
    df = df[df['PRICE'] != '']
    df['PRICE'] = pd.to_numeric(df['PRICE'].replace(
        ',', '', regex=True), errors='coerce')
    df.dropna(subset=['PRICE'], inplace=True)

    # Tenth Column Preprocessing (Year)
    # Handle missing values in the YEAR column
    mask = (df['YEAR'] == "") | df['YEAR'].isna()
    extracted_data = df.loc[mask, 'PERIOD']
    df.loc[mask, 'YEAR'] = extracted_data.apply(retrieve_year)

    # Convert the 'YEAR' column to string to avoid issues with .str accessor
    df['YEAR'] = df['YEAR'].astype(str)

    # Ensure the column contains only four numbers using regex
    matches = df['YEAR'].str.contains(metrics.REGEX_YEAR, na=False)

    # Extract the valid years using the regex pattern
    df.loc[matches, 'YEAR'] = df.loc[matches, 'YEAR'].str.extract(
        metrics.REGEX_YEAR, expand=False)

    # Remove rows where the year could not be resolved (NaN or empty)
    df = df[pd.notna(df['YEAR']) & (df['YEAR'] != '')]

    # Convert the 'YEAR' column back to integers (or NaN for invalid values)
    df['YEAR'] = df['YEAR'].apply(convert_to_int_or_nan)

    # Drop any remaining rows where the year is missing or invalid
    df.dropna(subset=['YEAR'], inplace=True)

    # Drop columns used for retrievel of missing information
    df.drop('PERIOD', axis=1, inplace=True)
    df.drop('DESCRIPTION', axis=1, inplace=True)

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

    process_data(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
