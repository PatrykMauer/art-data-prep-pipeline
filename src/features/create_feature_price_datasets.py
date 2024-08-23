import argparse
import pandas as pd


def create_feature_price_datasets(train_file, test_file, features_file):
    # Read datasets (assuming train and test are Excel files)
    try:
        train_df = pd.read_excel(train_file)
    except Exception as e:
        raise IOError(f"Error reading {train_file}") from e

    try:
        test_df = pd.read_excel(test_file)
    except Exception as e:
        raise IOError(f"Error reading {test_file}") from e

    # Reading features file (assuming it is a CSV without headers)
    try:
        features_df = pd.read_csv(features_file, header=None)
        features_df.columns = [
            'ImageName'] + [f'Feature_{i}' for i in range(1, len(features_df.columns))]
    except Exception as e:
        raise IOError(f"Error reading {features_file}") from e

    # Merging the PRICE column from train and test datasets into the features dataset
    features_train = pd.merge(
        features_df, train_df[['ImageName', 'PRICE']],
        on='ImageName', how='inner')
    features_test = pd.merge(
        features_df, test_df[['ImageName', 'PRICE']],
        on='ImageName', how='inner')

    return features_train, features_test


def main():
    parser = argparse.ArgumentParser(
        description='Create feature and PRICE datasets matched by ImageName.')
    parser.add_argument('train_file', type=str,
                        help='File path for the training dataset.')
    parser.add_argument('test_file', type=str,
                        help='File path for the testing dataset.')
    parser.add_argument('features_file', type=str,
                        help='File path for the features dataset.')

    args = parser.parse_args()

    features_train, features_test = create_feature_price_datasets(
        args.train_file, args.test_file, args.features_file)

    # Saving new datasets
    features_train.to_csv(
        'data/processed/train_features_price.csv', index=False)
    features_test.to_csv(
        'data/processed/test_features_price.csv', index=False)

    print("New train and test datasets with features and PRICE have been saved.")


if __name__ == '__main__':
    main()
