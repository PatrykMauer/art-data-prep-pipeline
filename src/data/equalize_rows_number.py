import argparse
import pandas as pd
import os


def read_dataset(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError(
            "Unsupported file format. Please use CSV or Excel files.")


def equalize_datasets(file1, file2):
    # Read the datasets
    df1 = read_dataset(file1)
    df2 = read_dataset(file2)

    # Finding common ImageNames
    common_images = pd.merge(
        df1[['ImageName']],
        df2[['ImageName']],
        on='ImageName')

    # Filtering both datasets for only common ImageNames
    df1_equalized = df1[df1['ImageName'].isin(common_images['ImageName'])]
    df2_equalized = df2[df2['ImageName'].isin(common_images['ImageName'])]

    # Filtering both datasets for only common ImageNames
    file1_name, file1_extension = os.path.splitext(file1)
    file2_name, file2_extension = os.path.splitext(file2)
    equalized_file1 = file1_name + '_equalized' + file1_extension
    equalized_file2 = file2_name + '_equalized' + file2_extension

    # Save the equalized datasets
    df1_equalized.to_excel(equalized_file1, index=False)
    df2_equalized.to_csv(equalized_file2, index=False)

    print(f"Datasets equalized and saved as {file1} and {file2}")


def main():
    parser = argparse.ArgumentParser(
        description='Equalize rows of two datasets based on ImageName.')
    parser.add_argument('file1', type=str,
                        help='File path for the first dataset.')
    parser.add_argument('file2', type=str,
                        help='File path for the second dataset.')

    args = parser.parse_args()

    equalize_datasets(args.file1, args.file2)


if __name__ == '__main__':
    main()
