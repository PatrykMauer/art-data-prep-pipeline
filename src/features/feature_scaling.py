import argparse
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import dump, load


def save_scaler(scaler, scaler_file_name):
    """Saves the scaler object in the 'references' folder."""
    scaler_path = Path('references') / scaler_file_name
    # Create the directory if it doesn't exist
    scaler_path.parent.mkdir(exist_ok=True)
    dump(scaler, scaler_path)


def load_or_fit_scaler(train_df, columns, scaler_file_name):
    """Loads the scaler if exists in 'references', otherwise fits a new scaler."""
    scaler_path = Path('references') / scaler_file_name
    if scaler_path.exists():
        print(f'Loading existing scaler from {scaler_path}')
        scaler = load(scaler_path)
    else:
        print(f'Fitting a new scaler')
        scaler = StandardScaler()
        scaler.fit(train_df[columns])
        save_scaler(scaler, scaler_file_name)
    return scaler


def scale_and_save_datasets(base_file_name, output_folder, columns):
    """Loads train and test datasets, scales them, and saves the scaled datasets."""
    # Constructing file paths
    train_file_path = Path(output_folder) / (base_file_name + '_train.xlsx')
    test_file_path = Path(output_folder) / (base_file_name + '_test.xlsx')

    # Loading datasets
    train_df = pd.read_excel(train_file_path)
    test_df = pd.read_excel(test_file_path)

    # Loading or fitting StandardScaler
    scaler_file_name = base_file_name + '_scaler.joblib'
    scaler = load_or_fit_scaler(train_df, columns, scaler_file_name)

    # Applying the scaler to the datasets
    train_df[columns] = scaler.transform(train_df[columns])
    test_df[columns] = scaler.transform(test_df[columns])

    # Saving the scaled datasets
    scaled_train_file_path = Path(
        output_folder) / (base_file_name + '_train_scaled.xlsx')
    scaled_test_file_path = Path(
        output_folder) / (base_file_name + '_test_scaled.xlsx')

    train_df.to_excel(scaled_train_file_path, index=False)
    test_df.to_excel(scaled_test_file_path, index=False)

    print(f'Scaled training data saved to {scaled_train_file_path}')
    print(f'Scaled test data saved to {scaled_test_file_path}')


def main():
    """Function for accepting arguments."""
    parser = argparse.ArgumentParser(
        description='Scale specified columns in train and test datasets.')
    parser.add_argument(
        'base_file_name', type=str,
        help='Base name of the Excel files to be scaled (without _train or _test suffix).')
    parser.add_argument(
        '--output_folder', type=str, default='.',
        help='Path to the folder where the scaled Excel files should be saved.')
    parser.add_argument('--columns', nargs='+',
                        help='List of columns to scale.')

    args = parser.parse_args()

    scale_and_save_datasets(args.base_file_name,
                            args.output_folder, args.columns)


if __name__ == '__main__':
    main()
