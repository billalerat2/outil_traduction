import os
from pathlib import Path

from config import DATA_DIR, OUTPUT_DIR
from loaders.loader_factory import LoaderFactory
from processors.data_processor import DataProcessor
from translators.translator import Translator
from evaluators.evaluator import Evaluator


class Orchestrator:
    """
    Orchestrateur principal du pipeline de traduction.
    """

    def __init__(
        self, data_path: str, output_dir: str, translation_model: str, metric: str
    ):
        self.input_path = os.path.join(DATA_DIR, data_path)
        self.output_dir = Path(output_dir)
        self.model_name = translation_model
        self.metric = metric

        if not os.path.isfile(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        if not os.path.isdir(self.output_dir):
            raise RuntimeError(f"Output directory does not exist: {self.output_dir}")

    def run(self):
        # --- 1. Load ---
        loader = LoaderFactory.create(self.input_path)
        df = loader.to_dataframe()
        df.to_csv(self.output_dir / "01_loaded.csv", index=False)

        # --- 2. Clean ---
        processor = DataProcessor(df)
        df = processor.clean()
        df.to_csv(self.output_dir / "02_cleaned.csv", index=False)

        # --- 3. Translate ---
        translator = Translator(self.model_name)
        df = translator.translate(df, column="source", new_column="translation")
        df.to_csv(self.output_dir / "03_translated.csv", index=False)

        # --- 4. Evaluate ---
        evaluator = Evaluator(df)
        scores = evaluator.evaluate()

        print("\nTranslation quality metrics:")
        for metric, value in scores.items():
            print(f"  {metric}: {value:.2f}")

        print("\nPipeline completed.")


if __name__ == "__main__":
    orch = Orchestrator(
        data_path="sample02.json",
        output_dir="output",
        translation_model="Helsinki-NLP/opus-mt-fr-en",
        metric="bleu",
    )
    orch.run()
