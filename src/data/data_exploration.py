import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def load_dataset(file_path, X_range):
    """Loads a dataset and splits it into features and target.

    Parameters:
    file_path (str): The path to the dataset file.
    X_range (slice): The slicing object to select columns for features.

    Returns:
    tuple: Tuple containing the features (X) and the target (y).

    Raises:
    FileNotFoundError: If the file does not exist.
    ValueError: If the file format is not supported.
    Exception: For other unforeseen errors.
    """
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    # Determine the file format
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        # Read the file based on its format
        if file_extension == '.xlsx':
            df = pd.read_excel(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Select features using X_range
        X = df.iloc[:, X_range].values.astype('float32')
        # Last column as the target
        y = df.iloc[:, -1].values.astype('float32')

        return X, y
    except Exception as e:
        # Handle other unforeseen errors
        raise Exception(f"An error occurred while processing the file: {e}")


def missing_data(data):
    total = data.isnull().sum()
    percent = (data.isnull().sum()/data.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return (np.transpose(tt))


def value_counts(data):
    total = data.nunique()  # Count of unique non-null values
    # Percentage of unique non-null values
    percent = round((data.nunique() / data.count() * 100), 2)
    tt = pd.concat([total, percent], axis=1, keys=[
                   'Unique Values', 'Unique Values/Total Count (%)'])

    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)

    tt['Types'] = types
    return np.transpose(tt)


def value_counts_for_article(data):
    total = data.nunique()  # Count of unique non-null values
    # Percentage of unique non-null values
    percent = round((data.nunique() / data.count() * 100), 2)
    tt = pd.concat([total, percent], axis=1, keys=[
                   'Unikatowe wartości', 'Stosunek do wszystkich (%)'])

    return np.transpose(tt)


def plot_distribution(df, col_name, bins_no=50):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col_name], bins=bins_no, kde=True)
    plt.title(f'Distribution of {col_name}')
    plt.xlabel(col_name)
    plt.ylabel('Frequency')
    plt.show()


def plot_categorical_distribution(df, col_name, head_length=20):
    distribution = df[col_name].value_counts()
    top_values = distribution.head(head_length)
    if len(top_values) < head_length:
        head_length = len(top_values)
    plt.figure(figsize=(10, 8))
    sns.barplot(y=top_values.index, x=top_values.values,
                palette="viridis", hue=top_values.index, legend=False)
    plt.title(f'Distribution of Artworks by Top {head_length} {col_name}s')
    plt.xlabel(f'Number of {col_name}s')
    plt.ylabel(col_name)
    plt.show()


def plot_categorical_distribution_for_article(df, col_name, head_length=20):
    distribution = df[col_name].value_counts()
    top_values = distribution.head(head_length)
    if len(top_values) < head_length:
        head_length = len(top_values)
    plt.figure(figsize=(10, 4))
    sns.barplot(y=top_values.index, x=top_values.values,
                palette="viridis", hue=top_values.index, legend=False)
    plt.title(f'Dystrybucja dzieł sztuki według {col_name}s')
    plt.xlabel(f'Liczba dzieł')
    plt.ylabel('Artysta')
    plt.show()
