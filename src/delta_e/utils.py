"""Utility Functions. """

import pandas as pd
from pathlib import Path
from typing import Union

class FileReader:
    """Reads in raw data."""

    def __init__(self, filepath: Union[str,Path]) -> None:
        """Parses filepath and extension.
        
        Args:
            filepath: Union[str,Path]
                Location of file to read in. 
        """
        if type(filepath) == str:
            self.file_path = Path(filepath)
        else:
            self.file_path = filepath
        self.ext = filepath.suffix
    
    def get_data(self) -> pd.DataFrame:
        """Reads data to a dataframe
        """
        
        # check if file has been locally downloaded 
        try:
            if self.ext == '.csv':
                data = pd.read_csv(Path(
                    Path(__file__).parent,
                    "resources",
                    str(self.file_path))
                )
            else: 
                raise NotImplementedError(
                    f"Extension {self.ext} can not be read."
                )
        except FileNotFoundError:
            raise NotImplementedError(
                f"Add functionality to download file data from http"
            )

        return data

