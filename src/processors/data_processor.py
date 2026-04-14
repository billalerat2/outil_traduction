import pandas as pd


class DataProcessor:
    """
    Effectue des operations de nettoyage et de pretraitement sur les donnees.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def clean(self) -> pd.DataFrame:
        """
        Nettoie les colonnes principales :
        - suppression des lignes incompletes
        - suppression des espaces superflus
        """
        df = self.df.copy()
        df = df.dropna(subset=["source", "reference"])
        df["source"] = df["source"].str.strip()
        df["reference"] = df["reference"].str.strip()
        return df
