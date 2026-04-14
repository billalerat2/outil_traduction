from pathlib import Path
from typing import Union, List

import pandas as pd

from loaders.base_loader import BaseLoader


class CSVLoader(BaseLoader):
    """
    Charge un ou plusieurs fichiers CSV depuis un repertoire
    et les combine en un DataFrame unique.
    """

    def __init__(self, directory: Union[str, Path], pattern: str = "*.csv"):
        self.directory = Path(directory)
        self.pattern = pattern

    def _list_csv_files(self) -> List[Path]:
        return list(self.directory.glob(self.pattern))

    def to_dataframe(self) -> pd.DataFrame:
        files = self._list_csv_files()

        if not files:
            raise FileNotFoundError(
                f"Aucun fichier CSV trouve dans {self.directory} avec le motif {self.pattern}"
            )

        dataframes = []

        for file in files:
            df = pd.read_csv(file)
            df["filename"] = file.name
            dataframes.append(df)

        return pd.concat(dataframes, ignore_index=True)
