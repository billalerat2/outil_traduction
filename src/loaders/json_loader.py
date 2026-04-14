import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from loaders.base_loader import BaseLoader


class JsonLoader(BaseLoader):
    """
    Charge des fichiers JSON depuis un repertoire et les convertit en DataFrame.
    Gere aussi bien les objets JSON uniques que les listes d'objets.
    """

    def __init__(self, directory, pattern="*.json"):
        self.directory = Path(directory)
        self.pattern = pattern

    def load_json_files(self) -> List[Path]:
        return list(self.directory.glob(self.pattern))

    def _flatten(
        self, obj: Any, prefix: str = "", out: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        if out is None:
            out = {}

        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}.{key}" if prefix else key
                self._flatten(value, new_key, out)

        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                new_key = f"{prefix}[{index}]"
                self._flatten(item, new_key, out)

        else:
            out[prefix] = obj

        return out

    def to_dataframe(self) -> pd.DataFrame:
        rows = []

        for file in self.load_json_files():
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    flat = self._flatten(item)
                    flat["filename"] = file.name
                    rows.append(flat)

            elif isinstance(data, dict):
                flat = self._flatten(data)
                flat["filename"] = file.name
                rows.append(flat)

        return pd.DataFrame(rows)
