from pathlib import Path

import pandas as pd


def data_analysis(sales_dataset: pd.DataFrame) -> None:
    '''
    Function to perform data analysis on the sales dataset.
    It prints the first five rows of the dataset and the number of missing values per column.'''
    print("First five rows:")
    print(sales_dataset.head())

    print("\nMissing values per column:")
    print(sales_dataset.isna().sum())


def main() -> None:
    dataset_path = Path(__file__).resolve().parent.parent / "datasets" / "sales.csv"
    sales_dataset = pd.read_csv(dataset_path)
    data_analysis(sales_dataset)


if __name__ == "__main__":
    main()
