from abc import ABC, abstractmethod
import pandas as pd


class BaseLoader(ABC):
    """
    Classe abstraite definissant l'interface commune a tous les chargeurs de donnees.
    Chaque sous-classe doit implementer la methode `to_dataframe`.
    """

    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        """
        Charge les donnees et retourne un objet pandas.DataFrame.
        """
        pass
