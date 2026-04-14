from pathlib import Path

from loaders.json_loader import JsonLoader
from loaders.csv_loader import CSVLoader


class LoaderFactory:
    """
    Fabrique permettant de selectionner dynamiquement le chargeur approprie.
    """

    @classmethod
    def create(cls, path: str, pattern: str = None):
        p = Path(path)

        # --- Cas 1 : chemin vers un fichier ---
        if p.is_file():
            ext = p.suffix.lower()
            if ext == ".json":
                return JsonLoader(p.parent, pattern=p.name)
            if ext == ".csv":
                return CSVLoader(p.parent, pattern=p.name)
            raise ValueError(f"Extension non supportee : {ext}")

        # --- Cas 2 : chemin vers un dossier ---
        if p.is_dir():
            json_files = list(p.glob("*.json"))
            csv_files = list(p.glob("*.csv"))

            if pattern:
                if pattern.endswith(".json"):
                    return JsonLoader(p, pattern)
                if pattern.endswith(".csv"):
                    return CSVLoader(p, pattern)
                raise ValueError(f"Motif non supporte : {pattern}")

            if json_files and not csv_files:
                return JsonLoader(p)
            if csv_files and not json_files:
                return CSVLoader(p)

            raise ValueError(
                "Impossible de choisir automatiquement : "
                "le dossier contient plusieurs types de fichiers."
            )

        raise FileNotFoundError(f"Chemin introuvable : {path}")
