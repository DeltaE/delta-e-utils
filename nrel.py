"""
NREL Annual Technology Baseline
===============================

Description
-----------
Each year, the NREL ATB data are presented in an Excel workbook that contains detailed cost and performance data (both current and projected) for renewable and conventional technologies. The workbook contains a spreadsheet with data and calculations for each technology.

Tags
----
``Operational cost``  ``capital cost`` ``variable cost`` ``capacity factor thermal`` ``efficiency thermal``  :literal:`blue text`
This is a paragraph with some :literal:`red text`, and some :literal:`blue text`.


.. role:: redtext
    :class: redtext

This is a paragraph with some :redtext:`red text`.


"""

import os
import pandas as pd
from typing import Tuple, List


class NREL:
    """
    Class to handle NREL data.
    """
    
    def __init__(self) -> None:
        self.data = None
        self.years_data = {}
        self.years = []

    def download_data_by_year(self, year: int) -> None:
        """
        Downloads data for a given year.

        The function uses a dictionary to determine the URL to download data from,
        based on the year parameter. The data is then downloaded as a CSV and saved
        to the current working directory.

        Args:
            year (int): The year for which data should be downloaded. Must be between 2019 and 2022.

        Returns:
            None

        Raises:
            ValueError: If the year parameter is outside the range of 2019 to 2022.
        """
        # Dictionary mapping year to URL
        year_url = {
            2019: "https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2019/ATBe.csv",
            2020: "https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2020/ATBe.csv",
            2021: "https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2021/ATBe.csv",
            2022: "https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2022/ATBe.csv"
        }

        # Check if year is in range
        if year not in year_url:
            raise ValueError(f"Year must be between 2019 and 2022. Got {year}")

        # Get URL for year
        url = year_url[year]

        # Create directory if it does not exist
        if not os.path.exists("data/NREL"):
            os.makedirs("data/NREL")

        # Download data
        df = pd.read_csv(url)
        df.to_csv(f"data/NREL/atb_electricity_{year}.csv", index=False)

        # Store data in NREL object
        self.years.append((year, df))

    def download_data_for_multiple_years(self, years: List[int]) -> pd.DataFrame:
        """
        Downloads data for multiple years and returns a combined DataFrame.

        Args:
            years (List[int]): The years for which data should be downloaded. Each year must be between 2019 and 2022.

        Returns:
            pd.DataFrame: The combined data for all years.

        Raises:
            ValueError: If any of the years in the years parameter are outside the range of 2019 to 2022.
        """
        for year in years:
            self.download_data_by_year(year)

        # Combine data from all years
        df = pd.concat([df for _, df in self.years], axis=0, ignore_index=True)

        return df

    def get_data(self, filepath: str) -> pd.DataFrame:
        """
        Get the data from a file and return it as a pandas DataFrame.

        Args:
            filepath (str): The file path of the data.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data.
        """
        data = pd.read_csv(filepath)
        self.data = data
        return data


    def get_features(self, data: pd.DataFrame = None) -> pd.DataFrame:
        """Get the features from the data and return them as a pandas DataFrame.

        Args:
            data: A pandas DataFrame containing the data. If not provided, the class data attribute will be used.

        Returns:
            A pandas DataFrame containing the features.
        """
        if data is None:
            data = self.data
        features = data.drop(columns=['target'])
        return features


    def get_target(self, data: pd.DataFrame = None) -> pd.Series:
        """Get the target from the data and return it as a pandas Series.

        Args:
            data: A pandas DataFrame containing the data. If not provided, the class data attribute will be used.

        Returns:
            A pandas Series containing the target.
        """
        if data is None:
            data = self.data
        target = data['target']
        return target


    def split_data(self, test_size: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split the data into training and testing sets and return them as a tuple of pandas DataFrames.

        Args:
            test_size: The proportion of the data to use for testing.

        Returns:
            A tuple of pandas DataFrames (training data, testing data).
        """
        self.training_data, self.testing_data = train_test_split(self.data, test_size=test_size)
        return self.training_data, self.testing_data



